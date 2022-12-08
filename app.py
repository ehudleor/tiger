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
    
    
     # side bar
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


    st.markdown('''
                ## About the app \n
                Hey, this web app is a great one to segment images using K-Means. \n
                There are many way. \n
                Enjoy! Yedidya


                ''') 
    
    
    
    # Run image
if app_mode == 'Segment an Image':
    
    st.sidebar.markdown('---') # adds a devider (a line)
    
    # side bar
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
    
    
    
    # choosing a k value (either with +- or with a slider)
    k_value = st.sidebar.number_input('Insert K value (number of clusters):', value=4, min_value = 1) # asks for input from the user
    st.sidebar.markdown('---') # adds a devider (a line)
    
    attempts_value_slider = st.sidebar.slider('Number of attempts', value = 7, min_value = 1, max_value = 10) # slider example
    st.sidebar.markdown('---') # adds a devider (a line)
    
    
     # read an image from the user
    img_file_buffer = st.sidebar.file_uploader("Upload an image", type=['jpg', 'jpeg', 'png'])

    # assign the uplodaed image from the buffer, by reading it in
    if img_file_buffer is not None:
        image = io.imread(img_file_buffer)
    else: # if no image was uploaded, then segment the demo image
        demo_image = DEMO_IMAGE
        image = io.imread(demo_image)
