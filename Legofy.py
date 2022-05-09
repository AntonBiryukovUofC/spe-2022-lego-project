# -*- coding: utf-8 -*-

import streamlit as st
from PIL import Image
import requests
from numpy import asarray
from urllib import request
import matplotlib.pyplot as plt
from skimage import data,  color
import skimage.segmentation as seg
from skimage.future import graph

st.title("Legofy your favourite photo")


upload_option = st.radio(  "Source of file is coming from"  ,("File Upload", "URL" ))
if upload_option == "File Upload":
     uploaded_file = st.file_uploader("Upload your own image", type=['gif', 'png', 'jpg', 'jpeg'])
     if uploaded_file is not None:
          uploaded_im = Image.open(uploaded_file)
          im_size = uploaded_im.size
          uploaded_ar = asarray(uploaded_im)
          st.write("Width: " + str(im_size[0]) + '; Height: ' + str(im_size[1]))
          st.write(uploaded_ar.shape)
          uploaded_grey=color.rgb2gray(uploaded_ar)
          uploaded_slic = seg.slic(uploaded_ar,  start_label=1)
          out1 = color.label2rgb(uploaded_slic, uploaded_ar, kind='overlay')
          out2 = color.label2rgb(uploaded_slic, uploaded_ar, kind='avg', bg_label=0)

          g = graph.rag_mean_color(uploaded_ar, uploaded_slic)
          labels2 = graph.cut_threshold(uploaded_slic, g, 10)
          out3 = color.label2rgb(labels2, uploaded_ar, kind='avg', bg_label=0)


          uploaded_slic1= seg.slic(uploaded_ar , n_segments=400)
          uploaded_slic2 = seg.slic(uploaded_ar , n_segments=300)
          uploaded_slic3 = seg.slic(uploaded_ar , n_segments=200)
          uploaded_slic4 = seg.slic(uploaded_ar , n_segments=100)

          #labels1 = segmentation.slic(uploaded_ar, compactness=30, n_segments=400, start_label=1)
          #out1 = color.label2rgb(labels1, uploaded_ar, kind='avg', bg_label=0)

          #g = graph.rag_mean_color(uploaded_ar, labels1)
          #labels2 = graph.cut_threshold(labels1, g, 29)
          #out2 = color.label2rgb(labels2, uploaded_ar, kind='avg', bg_label=0)

          #fig, ax = plt.subplots(figsize=(10, 10))
          #ax.imshow(out1)
          #ax.imshow(uploaded_slic1)
          #ax.imshow(uploaded_ar)
          #ax.imshow(color.label2rgb(uploaded_slic, uploaded_ar, kind='avg'))

          fig = plt.figure()
          fig.set_figheight(10)
          fig.set_figwidth(10)
          ax1 = plt.subplot2grid(shape=(3, 3), loc=(0, 0), colspan=2, rowspan=2)
          ax2 = plt.subplot2grid(shape=(3, 3), loc=(2, 0))
          ax3 = plt.subplot2grid(shape=(3, 3), loc=(2, 1))
          ax4 = plt.subplot2grid(shape=(3, 3), loc=(0, 2))
          ax5 = plt.subplot2grid(shape=(3, 3), loc=(1, 2))
          ax6 = plt.subplot2grid(shape=(3, 3), loc=(2, 2))


          ax1.imshow(uploaded_ar)
          ax1.axis('off')
          ax1.set_title('Original Image')
          ax2.imshow(uploaded_slic)
          ax2.axis('off')
          ax2.set_title('segmentation.slic')
          ax3.imshow(out1)
          ax3.axis('off')
          ax3.set_title('color.label2rgb: overlay')
          ax4.imshow(out2)
          ax4.axis('off')
          ax4.set_title('color.label2rgb: average')
          ax5.imshow(out3)
          ax5.axis('off')
          ax5.set_title('graph.rag_mean_color: average ')
          ax6.imshow(uploaded_ar)
          ax6.axis('off')
          ax6.set_title(' ')

          st.pyplot(fig)




elif upload_option == "URL":
     url = st.text_input("Paste the URL of your image")
     if url is not None and url != '':
          #filename = url.split('/')[-1]
          #request.urlretrieve(url, filename)
          #uploaded_im = Image.open(filename)
          response = requests.get(url)
          uploaded_im =  Image.open(requests.get(url, stream=True).raw)
          im_size = uploaded_im.size
          uploaded_ar = asarray(uploaded_im)
          st.write("Width: " + str(im_size[0]) + '; Height: ' + str(im_size[1]))
          st.image(uploaded_im)
