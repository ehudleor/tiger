# import libs
import streamlit as st
import cv2
import numpy as np
import skimage.io as io
#import matplotlib.pyplot as plt

# check versions
#np.__version__

################################# function to segment using k-means

# vars
DEMO_IMAGE = 'demo.png' # a demo image for the segmentation page, if none is uploaded
favicon = 'favicon.png'
