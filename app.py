# import libs
import streamlit as st
import cv2
import numpy as np
import skimage.io as io
from skimage.color import label2rgb, rgb2gray
from skimage import measure, io, img_as_ubyte, morphology, util, color
from skimage.filters import threshold_multiotsu
import matplotlib.pyplot as plt
import imutils

# check versions
#np.__version__

def otsu_process(file_path):
  img = io.imread(file_path)
  img_gray = io.imread(file_path, as_gray=True)
  thresholds = threshold_multiotsu(img_gray, classes=3)  #find the values of the thresholds
  regions = np.digitize(img_gray, bins=thresholds)
  plt.imshow(regions, cmap = 'Greens_r')
  return regions

# vars
DEMO_IMAGE = 'demo.png' # a demo image for the segmentation page, if none is uploaded
favicon = 'favicon.png'

# main page
st.set_page_config(page_title='Multy Ossu - Ehud Leor', page_icon = favicon, layout = 'wide', initial_sidebar_state = 'auto')
st.title('Image Segmentation using multy-otsu, by hud Leor')

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
    st.markdown('In this app we will segment images using multy-otsu')
    
    
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
                Hey, this web app is a great one to segment images using multy-otsu. \n
                There are many way. \n


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
    
    
    
    
    
     # read an image from the user
    img_file_buffer = st.sidebar.file_uploader("Upload an image", type=['jpg', 'jpeg', 'png'])

    # assign the uplodaed image from the buffer, by reading it in
    if img_file_buffer is not None:
        image = io.imread(img_file_buffer)
    else: # if no image was uploaded, then segment the demo image
        demo_image = DEMO_IMAGE
        image = io.imread(demo_image)

        
         # display on the sidebar the uploaded image
    st.sidebar.text('Original Image')
    st.sidebar.image(image)
    
    
    ############################################### call the function to segment the image
    img = otsu_process(f'{img_file_buffer}')
    #counr the green pixels
    leaf_count = np.sum((np.array(img) >0)&(np.array(img) <2))
    bg_count = np.sum((np.array(img) ==0)|(np.array(img) ==2))
    # Load Aruco detector
    parameters = cv2.aruco.DetectorParameters_create()
    aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_5X5_50)
    # Get Aruco marker
    corners, _, _ = cv2.aruco.detectMarkers(image, aruco_dict, parameters=parameters)
    # Draw polygon around the marker
    int_corners = np.int0(corners)
    cv2.polylines(image, int_corners, True, (0, 255, 0), 10)
    # Aruco Area
    aruco_area = cv2.contourArea (corners[0])
    ######print('AruCo Area:',aruco_area, 'px')
    # Pixel to cm ratio
    pixel_cm_ratio = 5*5 / aruco_area# since the AruCo is 5*5 cm, so we devide 25 cm*cm by the number of pixels
    #####print('Ratio - Each pixel is',pixel_cm_ratio, 'cm*cm')
    Area = leaf_count*pixel_cm_ratio
    ###'cm\N{SUPERSCRIPT TWO},', 'which is:',  f'{0.0001*leaf_count*pixel_cm_ratio:.3f}', 'm\N{SUPERSCRIPT TWO}')
        # Display the result on the right (main frame)
    st.subheader('Output Image')
    st.image(img, use_column_width=True)
