# import libs
import streamlit as st
import cv2
import numpy as np
import skimage.io as io
import matplotlib.pyplot as plt

# check versions
#np.__version__

################################# function to segment using k-means

# vars
DEMO_IMAGE = 'demo.png' # a demo image for the segmentation page, if none is uploaded
favicon = 'favicon.png'

# main page
st.set_page_config(page_title='K-Means - Yedidya Harris', page_icon = favicon, layout = 'wide', initial_sidebar_state = 'auto')
st.title('Image Segmentation using K-Means, by Yedidya Harris')

st.markdown(
    """
    <style>
    [data-testid="stSidebar"][aria-expanded="true"] . div:first-child{
        width: 350px
    }
    
    [data-testid="stSidebar"][aria-expanded="false"] . div:first-child{
        width: 350px
        margin-left: -350px
    }    
    </style>
    
    """,
    unsafe_allow_html=True,


)
st.sidebar.title('Segmentation Sidebar')
st.sidebar.subheader('Site Pages')

# using st.cache so streamlit runs the following function only once, and stores in chache (until changed)
@st.cache()

# take an image, and return a resized that fits our page
def image_resize(image, width=None, height=None, inter = cv2.INTER_AREA):
    dim = None
    (h,w) = image.shape[:2]
    
    if width is None and height is None:
        return image
    
    if width is None:
        r = width/float(w)
        dim = (int(w*r),height)
    
    else:
        r = width/float(w)
        dim = (width, int(h*r))
        
    # resize the image
    resized = cv2.resize(image, dim, interpolation=inter)
    
    return resized


# add dropdown to select pages on left
app_mode = st.sidebar.selectbox('Navigate',
                                  ['About App', 'Segment an Image'])


if app_mode == 'About App':
    st.markdown('In this app we will segment images using K-Means')
