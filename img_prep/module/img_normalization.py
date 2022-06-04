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
# imports

import cv2
import numpy  as np

# ----------------------------------------------------------------------------
# normalization 


def normalize_all_images(all_imgs:np.ndarray):
    """ Takes the image and normalizes their colors, so that the 
    fact that they have been taken with differnt cameras (slightly diff colors)
    cannot be memorized by the algo

    # TODO
    """
    pass


# ----------------------------------------------------------------------------
# CLAHE


def normalize_img_to_bw(img_arr:np.ndarray) -> tuple:
    """ This function transform the initial image to an normalized greyscale w
    three channels image, applying:
        * MINMAX NORMALIZATION:
            https://docs.opencv.org/3.4/d2/de8/group__core__array.html#ga87eef7ee3970f86906d69a92cbf064bd
        * CLAHE: 
            https://docs.opencv.org/4.x/d6/dc7/group__imgproc__hist.html#gad689d2607b7b3889453804f414ab1018
        * BINARY THRESHOLDING: 
            https://docs.opencv.org/4.x/d7/d1b/group__imgproc__misc.html#gae8a4a146d1ca78c626a53577199e9c57
    
    Args:
        img_arr: initial img, either real or synthetic, on a RGB colosrpace
    
    Returns:
        img_arr, clahe_img, final_image: returns three images to make a plot
    """

    img_arr = np.array(img_arr, dtype=np.uint8)     

    image_bw = cv2.cvtColor(
        img_arr, 
        cv2.COLOR_RGB2GRAY
    )  # returns a single channel matrix

    clahe = cv2.createCLAHE(
        clipLimit = 2.,     # Threshold for contrast limit, overt 10 is very dramatic
        tileGridSize=(8,8)   # Window size over the CLAHE is performed, default 8,8
    ) # Only works over one channe-
    img_clahe = clahe.apply(image_bw)


    # Since this is the Black&White version, we need to multiply its channels
    # In order to maintain compatibility with model:
    final_image = np.stack((img_clahe,)*3, axis=-1)    

    return final_image


def normalize_img_to_rgb(img_arr:np.ndarray) -> tuple:
    """ This function transform the initial image to an normalized RGB w
    three channels image, applying:
        * MINMAX NORMALIZATION:
            https://docs.opencv.org/3.4/d2/de8/group__core__array.html#ga87eef7ee3970f86906d69a92cbf064bd
        * CLAHE: 
            https://docs.opencv.org/4.x/d6/dc7/group__imgproc__hist.html#gad689d2607b7b3889453804f414ab1018
        * BINARY THRESHOLDING: 
            https://docs.opencv.org/4.x/d7/d1b/group__imgproc__misc.html#gae8a4a146d1ca78c626a53577199e9c57
    
    In this case, CLAHE is applied over the luminance channel of the LAB colorspace

    Args:
        img_arr: initial img, either real or synthetic, on a RGB colosrpace
    
    Returns:
        img_arr, clahe_img, final_image: returns three images to make a plot
    """

    """
    image_arr = cv2.normalize(
        img_arr, img_arr, 
        0, 255, cv2.NORM_MINMAX
    )
    """
    img_arr = np.array(img_arr, dtype=np.uint8)

    image_lab = cv2.cvtColor(
        img_arr, 
        cv2.COLOR_RGB2LAB
    )  # returns a single channel matrix

    lab_planes = cv2.split(image_lab)

    clahe = cv2.createCLAHE(
        clipLimit = 2.,     # Threshold for contrast limit, overt 10 is very dramatic
        tileGridSize=(8,8)   # Window size over the CLAHE is performed, default 8,8
    ) # Only works over one channe-

    lab_planes[0] = clahe.apply(lab_planes[0])
    lab = cv2.merge(lab_planes)

    final_img = cv2.cvtColor(lab, cv2.COLOR_LAB2RGB)
    return final_img


# ----------------------------------------------------------------------------
# end