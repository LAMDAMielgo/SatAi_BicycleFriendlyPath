"""
##############################################################################

This file contains all the functions related to:
    - outlier filtering
    - change imges of colorspace
    - reshape arrays
    - mean of a channel from an image

This is used to filter ''outliers'' from the GoogleStreetViewer: tunnels, 
nocturnal and user-taken photos

##############################################################################
"""

# ----------------------------------------------------------------------------

import cv2
import geopandas  as gpd
import matplotlib.pyplot as plt
import matplotlib.image  as mpimg
import numpy  as np
import pandas as pd

from re  import findall
from PIL import Image
from pprint import pprint
from typing import Generator, List
from shapely import wkt


# ----------------------------------------------------------------------------
#  change of img size


def flatten_image_array(img_arr:np.ndarray) -> np.ndarray:
    """ Given an image array flatten its shape to a pixel level
    matrix: 
            (w, h, cc) -> (w*h, cc)
    """
    w,d,cc = img_arr.shape
    return img_arr.reshape((w*d, cc))


# ----------------------------------------------------------------------------
#  change of img colospace


def imagearr_to_hsv(img_arr:np.ndarray) -> np.ndarray:
    """ The array images are on a RGB colorspace, just for eda exploration
    to see if there is any difference between noctural and daily images, the
    images are set in a HSV:

        https://programmingdesignsystems.com/color/color-models-and-color-spaces/index.html
        https://pythonwife.com/color-spaces-and-channels-in-opencv/

        HSV:
            - H: hue (image)
            - S: saturation (greyness)
            - V: value (brightness)
    
    Args:
        img_arr : in RBG (as fetched)
    
    Returns:
        Tuple[np.ndarray]
    """
    img_bgr = cv2.cvtColor(img_arr, cv2.COLOR_BGR2RGB)
    img_hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)

    return np.asarray(img_hsv)


def imagearr_to_lab(img_arr:np.ndarray) -> np.ndarray:
    """ The array images are on a RGB colorspace, just for eda exploration
    to see if there is any difference between noctural and daily images, the
    images are set in a LAB colorsapce and HSV:

        https://programmingdesignsystems.com/color/color-models-and-color-spaces/index.html
        https://pythonwife.com/color-spaces-and-channels-in-opencv/

        LAB: 
            - L: luminance dimensions (intensity)
            - a: colors from green to magenta
            - b:  colors from blue to yellow   

    Args:
        img_arr : in RBG (as fetched)
    
    Returns:
        Tuple[np.ndarray]
    """
    img_bgr = cv2.cvtColor(img_arr, cv2.COLOR_BGR2RGB)
    img_lab = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2LAB)

    return np.asarray(img_lab)


# ----------------------------------------------------------------------------
#  means

def mean_rgb_blue(img_arr):
    """ Given an img_arr, extracts the mean blue value of the image
    """
    blue_channel = img_arr[:, :, 2]
    return np.mean(blue_channel)


def mean_lab_sat(img_arr):
    """ Given an img array in LAB color space, extracts the mean green
    to magenta value of the image
    """
    sat_channel = img_arr[:, :, 1]
    return np.mean(sat_channel)


def categorize_if_outlier(img_arr:np.ndarray):
    """ Given an img as an RGB array, returns if - by the analysis done - there 
    is a big change it is a noctural or a photo taken inside a tunnel, and, 
    therefore, it is a bad image to give to our model.

    """
    img_rgb = np.array(img_arr)    
    arr_hsv = imagearr_to_hsv(img_rgb)

    mean_blue  = mean_rgb_blue(img_rgb)
    mean_sat   = mean_lab_sat(arr_hsv)
    
    # NOTE: me equivoque en los canales y los nombres estan cambiados

    if mean_blue < 127 and mean_sat > 75:
        return True
    else:
        return False
        

# ----------------------------------------------------------------------------
#  viz

def print_color_histogram(img_arr: np.ndarray, figsize:tuple) -> None:
    """ Given an image, prints the image and its color distribution 
    in two separate subplots.
    
    JPG images are in the following colorspace : BGR : blue, green, red
    """  
    lab_img = imagearr_to_lab(img_arr)
    hsv_img = imagearr_to_hsv(img_arr)

    pixel_matrix_rgb = flatten_image_array(img_arr)    
    pixel_matrix_lab = flatten_image_array(lab_img)    
    pixel_matrix_hsv = flatten_image_array(hsv_img)    

    f, ax = plt.subplots(ncols = 1+3*4, figsize=figsize)
    
    ax[0].imshow(img_arr)
    ax[0].set_title('Image BRG')
    
    # Axes from [1] -> [3]
    i = 1
    zip_content = [
        (pixel_matrix_rgb, ['red', 'green', 'blue'],     'RBG', 0.05), 
        (pixel_matrix_lab, ['orange', 'green', 'blue'],  'LAB', 0.15), 
        (pixel_matrix_hsv, ['black', 'magenta', 'cyan'], 'HSV', 0.35)
    ]

    for t in zip_content:

        pm, cl, ct, ysc = t
        # pm: pixel_matrix for a color scale
        # cl: colors to print each channel
        # ct: colorspace title 
        # ysc: y dim scale

        for ic, cc in enumerate(cl):
            sns.kdeplot(
                pm[:, ic], color = cc, ax= ax[i]
            )
            ax[i].axvline(np.median(
                pm[:, ic]), color = cc,  ls= '--'
            )
            ax[i].axvline(np.mean(
                pm[:, ic]), color = cc,  ls= '-'
            )
            ax[i].set_title(f"{ct}: {cc.upper()}")

            ax[i].set_ylim(0, ysc)
            ax[i].set_xlim(10, 240)
            i += 1 

        for ic, cc in enumerate(cl):
            sns.kdeplot(
                    pm[:, ic], color = cc, ax= ax[i]
                )
            ax[i].set_title(f"{ct}")
            ax[i].set_ylim(0, ysc)
        i += 1
    plt.show()


# ----------------------------------------------------------------------------
#  end