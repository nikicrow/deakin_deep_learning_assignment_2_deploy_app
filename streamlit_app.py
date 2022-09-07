import streamlit as st
import pandas as pd
import numpy as np
from matplotlib import image
import tensorflow as tf
import boto3

# Add app title
st.title('Is this Recyclable?')
st.write("Upload any image and we will tell you if it is recyclable or not")

# Add image uploader
uploaded_file = st.file_uploader("Please upload an image using this image uploader",type=['png', 'jpg'])

# image preprocessor
def preprocess_image(image):
    image_size = 200
    if image.shape[-1] == 3:
        image = tf.image.convert_image_dtype(image, tf.float32) 
        image = tf.image.resize(image, (image_size, image_size))
    # remove alpha channel for images with them
    elif image.shape[-1] == 4:
        image_without_alpha = image[:,:,:3]
        image = tf.image.convert_image_dtype(image_without_alpha, tf.float32) 
        image = tf.image.resize(image, (image_size, image_size))
    return image

def is_recyclable(uploaded_file):
    # preprocess image
    current_image = image.imread(uploaded_file)
    img_array = np.asarray(current_image)
    preprocessed_image = preprocess_image(img_array)

    # get secrets for getting model
    AWS_KEY = st.secrets["AWS_KEY"]
    AWS_SECRET_KEY = st.secrets["AWS_SECRET_KEY"]
    BUCKET = st.secrets["BUCKET"]
    KEY = st.secrets["KEY"]

    # set up the s3 resource with all our secrets
    s3_resource = boto3.resource('s3', 
                                aws_access_key_id = AWS_KEY,
                                aws_secret_access_key = AWS_SECRET_KEY, 
                                region_name='ap-southeast-2')

    # load the model
    loaded_model = s3_resource.Bucket(BUCKET).Object(KEY).get()['Body'].read()

    # make prediction
    prediction = loaded_model.predict(np.expand_dims(preprocessed_image, axis=0))
    # return outcome and prediction
    if prediction >= 0.5:
        return True, round(prediction*100,2)
    else:
        return False, round(prediction*100,2)


# If we get a picture uploaded, lets do stuff to it!
if uploaded_file is not None:
    # show uploaded file
    st.image(uploaded_file, caption='Input Image', use_column_width=True)
    # get outcome and prediction
    outcome, prediction = is_recyclable(uploaded_file)
    # create a function that returns the answer
    if outcome == True:
        st.write(f'This looks recyclable! To be precise, there is a {prediction}% chance it is recyclable. Please make sure recycle it.', use_column_width=True) 	
    elif outcome == False:
        st.write(f'This doesn\'t look recyclable. To be precise, there is a {prediction}% chance it is recyclable. Can you reuse it instead?', use_column_width=True) 	
    else:
        st.write('Looks like there\'s a problem with processing this image...')
    
