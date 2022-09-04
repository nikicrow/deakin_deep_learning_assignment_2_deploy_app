import streamlit as st
import pandas as pd
import numpy as np
import tensorflow as tf

# Add app title
st.title('Is this Recyclable?')
st.write("Upload any image and we will tell you if it is recyclable or not")

uploaded_file = st.file_uploader("Please upload an image using this image uploader")


#loaded_model = tf.keras.models.load_model('drive/MyDrive/Colab Notebooks/models/model_2_augmented.h5')
