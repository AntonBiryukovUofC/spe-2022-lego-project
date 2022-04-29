# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
streamlit run ~/Downloads/Legofy.py
"""



import streamlit as st
from PIL import Image
from numpy import asarray
from urllib import request
import requests
import imghdr

st.title("Legofy your favourite photo")



upload_option = st.radio(  "Source of file is coming from"  ,("File Upload", "URL" ))
if upload_option == "File Upload":
     uploaded_file = st.file_uploader("Upload your own image", type=['gif', 'png', 'jpg', 'jpeg'])
     if uploaded_file is not None:
          uploaded_im = Image.open(uploaded_file)
          im_size = uploaded_im.size
          uploaded_im = uploaded_im.save()
          uploaded_ar = asarray(uploaded_im)
          st.write("Width: " + str(im_size[0]) + '; Height: ' + str(im_size[1]))
          st.image(uploaded_file)
elif upload_option == "URL":
     url = st.text_input("Paste the URL of your image")
     if url is not None and url != '':
          filename = url.split('/')[-1]
          request.urlretrieve(url, filename)
          uploaded_im = Image.open(filename)
          im_size = uploaded_im.size
          uploaded_ar = asarray(uploaded_im)
          st.write("Width: " + str(im_size[0]) + '; Height: ' + str(im_size[1]))
          st.image(filename)









