import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import tensorflow as tf

# Add app title
st.title('Is this Recyclable?')
st.write("Upload any image and we will tell you if it is recyclable or not")

uploaded_file = st.file_uploader("Please upload an image using this image uploader")

#loaded_model = tf.keras.models.load_model('drive/MyDrive/Colab Notebooks/models/model_2_augmented.h5')
def is_recyclable(uploaded_file):
    return True

# If we get a picture uploaded, lets do stuff to it!
if uploaded_file is not None:
    #src_image = load_image(uploaded_file)
    image = Image.open(uploaded_file)	
	
    st.image(uploaded_file, caption='Input Image', use_column_width=True)
    #st.write(os.listdir())

    # create a function that returns the answer
    if is_recyclable(uploaded_file):
        st.write('This looks recyclable! Please make sure recycle it.', use_column_width=True) 	
    elif not is_recyclable(uploaded_file):
        st.write('This doesn\'t look recyclable. Bummer', use_column_width=True) 	
    else:
        st.write('Looks like we have a problem with processing this image...')
    
