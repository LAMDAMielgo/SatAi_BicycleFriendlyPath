"""
##############################################################################

This file contains all the functions related to:
    - open
    - parse
    - join
    - transform 

The data fetched from the GoogleStreetViewer in order to have the images and 
their corresponding metadata on a single dataframe.

##############################################################################
"""

# ----------------------------------------------------------------------------

import json
import geopandas  as gpd
import matplotlib.pyplot as plt
import matplotlib.image  as mpimg
import numpy  as np
import pandas as pd

from glob import glob
from os  import path, listdir
from re  import findall
from PIL import Image
from pprint import pprint
from typing import Generator, List
from shapely import wkt

# ----------------------------------------------------------------------------
# functions for opening files and making a joined datafame

def get_files_from_dir(input_dir:str, fext:str='.json') -> Generator:
    """ Given a input directory and a target file extension,
    parses all the files and yields their content

    Args:
        input_dir (str): directory where the files to files 
            are stored.
        fext (str): file extension to parse. JSON expected 

    Yields:
        parsed data
    """ 

    def parses_json(fname, input_dir):
        """ When the input file is a JSON, it opens it and loads
        it as a dictionary
        """
        fpath = path.join(input_dir, fname)

        with open(fpath, 'r') as fjson:
            return json.load(fjson)
    
    def pases_jpg(fname, input_dir):
        """ When the input file is a JPG, open the Image and loads
        it as an array
        """
        return np.asarray(Image.open(fname))

    # if the dash is not in the input str:
    input_dir += '/' if not input_dir.endswith('/') else ''

    fext_mapper = {
        '.json': parses_json,
        '.jpg': pases_jpg
    }

    for fname in glob(f"{input_dir}*{fext}"):
        
        output_name = fname.split('/')[-1]
        parsing_function = fext_mapper.get(fext)

        if parsing_function: 
            output = parsing_function(fname, input_dir)
            yield output_name, output
    # end



def tuplegen_to_dict(tgen:Generator) -> dict:
    """ Takes a generator of an iterator of tuples to a dict
            [(k,v) .. (k,v)] -> {k:v}
    """ 
    return {t[0]: t[1] for t in list(tgen)} 



def rename_key(key:str):
    """ The keys of a dictionary are given with a full path.
    This functions shricks the name to only the filename.
        
        {prefix}{x} {y}{filext} -> {x}_{y}

    Args:
        key: filename as dictionary as key
    
    Returns:
        rename key
    """

    listk = findall(
        "(?<=_)(.*)(?=.json|.jpg)", 
        key
    )

    return "_".join(listk).replace(' ', '_')



def format_metadata(data:Generator, headers:list) -> List[dict]:
    """ There are two types of data stored in the folder:
      - Header data
      - Meta   data

    They have different keys(), therefore we need to separated 
    them to concat them when making a dataframe.

    Args:
        data (generator): dictionary like generator that has the
            data parsed.
    
    Returns:
        tuple with two dictionaries, header and meta information
    """
    d_files = tuplegen_to_dict(data)  # [(k,v) .. (k,v)] -> {k:v}

    for item in headers:
        yield {
            rename_key(k):v 
            for k, v in d_files.items() 
            if k.startswith(item)
        }
    # end 



def format_imgs(data:Generator):
    """ The dict generator of the images dataset needs to be with an
    index keys in order to be used with pd.DF.from_dict().

    Changes the tuples from a format of : 
        (filename, value) -> {xy, filename, value}

    Args:
        data (generator): dictionary like generator that has the images
        pased 
    """
    d_files = tuplegen_to_dict(data)  # [(k,v) .. (k,v)] -> {k:v}    
    d_files = [(rename_key(k), k, v) for k, v in d_files.items()]

    return d_files



    
# ----------------------------------------------------------------------------
# cleaning the dataframe:

def drop_columns_with_one_val(frame):
    """ If there is only one unique value in a columns, that columns is 
    drop since it doens't add any information of data.

    It also takes the cases where all the values a none, so it purges
    the dataframe in the axis = 1.

    Args:
        df: initial dataframe
    
    Returns:
        df: purged dataframe
    """
    cols_to_drop = []

    try:
        for col in frame.columns:
            if frame[col].nunique() == 1:
                cols_to_drop.append(col)
                
    except TypeError:
        # if unhashable type, then pass
        pass

    frame.drop(columns=cols_to_drop, inplace=True)
    return frame


def get_latlon(cell):
    """ In the metadata, the lat lon is given a a dictionary such as:

        'location' -> {'lat': ...., 'lng': ...... }

    This function takes the lat lon of the dictionary, creates Well 
    known Text representation of the geometry and return its parsing 
    into a geometry obj.

    WKT info: 
       https://en.wikipedia.org/wiki/Well-known_text_representation_of_geometry
       https://geopandas.org/en/stable/docs/reference/api/geopandas.GeoSeries.from_wkt.html

    Args:
        ser: pandas series -> df[col]
    
    Returns:
        tuple of two series, one for lat(Y) and the other for long (X)
    """
    if isinstance(cell, dict):
        lat =  cell['lat']
        lon =  cell['lng']
    else:
        raise TypeError

    # conversion to WKT
    wkt_geom = f"POINT ({lon} {lat})"
    return wkt.loads(wkt_geom)



# ----------------------------------------------------------------------------
# puting everything together

def get_gsv_data(gsv_path: str):
    """ THis function is the main function of this process.
    It opens the JSON data and the images data and joins them into a singles
    dataframe. 

    There are a lot of columns that do not add any new information, so before
    returning the merged dataframe, single value columns are dropped.

    Args:
        gsv_path: string path where all the data is stored
    
    Returns:
        pd.DataFrame
    """
    # get all the files by extention
    json_files = get_files_from_dir(input_dir=gsv_path, fext='.json')
    imgs_files = get_files_from_dir(input_dir=gsv_path, fext='.jpg')

    # parsing the files into separate dataframes
    meta = pd.concat(
        [   pd.DataFrame.from_dict(d, orient='index') 
            for d in list(format_metadata(json_files, ["header", "meta"]))
        ], axis = 1
    )
    imgs = pd.DataFrame.from_records(
        imgs, ['coords', 'image_fname', 'image_arr']
    )

    # merging the dataframes
    metadata = pd.merge(meta, imgs, right_on='coords', left_index=True)

    metadata = drop_columns_with_one_val(metadata) 
    metadata.set_index(['image_fname'], inplace=True)

    return metadata


# ----------------------------------------------------------------------------
# opening geographic dataframe

def clean_geo_data(df, img_path_col):
    """ This function makes all the transformation to the dataframe in order
    to return a clean dataframe:
        - Drops all duplicates
        - Drops all rows without images from the the GSV process
    """
    initial_shape = df.shape

    df.drop_duplicates(keep='first', inplace=True)
    df = df[df[img_path_col].notnull()].copy(deep=True)
    df.set_index([img_path_col], inplace=True)

    final_shape = df.shape
    print(f"CLEANED DF: before shape {initial_shape}, after shape {final_shape}")

    return df


def get_geographic_data(geodf_path: str, geodf_name: str):
    """ This function opens and cleans the dataframe that contains the points
    and its relation to the images path from the google street viewer

    Args:
        geodf_path: folder where the csv is located
        geodf_name: name of the csv file
    
    Returns:
        pd.DataFrame
    """
    cols_to_take = ['date', 'copyright', 'image_arr', 'geometry', 'cyclist_type']

    df = pd.read_csv(f'{geodf_path}/{geodf_name}.csv')
    print(f"Initial shape: {df.shape}")

    # in the initial dataset, latitude and longitude are swapped
    # let's fix that
    df.rename(
        columns={'lat':'x_coord_long', 'lon': 'y_coord_lat'}, 
        inplace=True
    )

    # clean the dataframe
    df = clean_geo_data(df, img_path_col='img_fname')
    df = df[cols_to_take].copy(deep=True)

    return df

# ----------------------------------------------------------------------------
# end