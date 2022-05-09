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

im_size,uploaded_ar = None,None
upload_option = st.radio(  "Source of file is coming from"  ,("File Upload", "URL" ))
if upload_option == "File Upload":
     uploaded_file = st.file_uploader("Upload your own image", type=['gif', 'png', 'jpg', 'jpeg'])
     if uploaded_file is not None:
          uploaded_im = Image.open(uploaded_file)
          im_size = uploaded_im.size
          uploaded_ar = asarray(uploaded_im)


elif upload_option == "URL":
     url = st.text_input("Paste the URL of your image",value='https://vetstreet.brightspotcdn.com/dims4/default/e0b07c7/2147483647/thumbnail/645x380/quality/90/?url=https%3A%2F%2Fvetstreet-brightspot.s3.amazonaws.com%2F0b%2F6beb80a81011e0a0d50050568d634f%2Ffile%2FWhippet-1-645mk062911.jpg')
     if url is not None and url != '':
          #filename = url.split('/')[-1]
          #request.urlretrieve(url, filename)
          #uploaded_im = Image.open(filename)
          response = requests.get(url)
          uploaded_im =  Image.open(requests.get(url, stream=True).raw)
          im_size = uploaded_im.size
          uploaded_ar = asarray(uploaded_im)

st.write("Width: " + str(im_size[0]) + '; Height: ' + str(im_size[1]))
st.write(uploaded_ar.shape)
uploaded_grey=color.rgb2gray(uploaded_ar)
compactness = st.slider("Compactness",0,100,30)
n_segments = st.slider("Number of segments",1,500,10)
labels = seg.slic(uploaded_ar, compactness=compactness, n_segments=n_segments, start_label=1)
out_overlay = color.label2rgb(labels, uploaded_ar, kind='overlay')
out_avg = color.label2rgb(labels, uploaded_ar, kind='avg', bg_label=0)
g = graph.rag_mean_color(uploaded_ar, labels)

labels_graph_cutoff = graph.cut_threshold(labels, g, 18)
out_rag = color.label2rgb(labels_graph_cutoff, uploaded_ar, kind='avg', bg_label=0)



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
ax2.imshow(labels)
ax2.axis('off')
ax2.set_title('segmentation.slic')
ax3.imshow(out_overlay)
ax3.axis('off')
ax3.set_title('color.label2rgb: overlay')
ax4.imshow(out_avg)
ax4.axis('off')
ax4.set_title('color.label2rgb: average')
ax5.imshow(out_rag)
ax5.axis('off')
ax5.set_title('graph.rag_mean_color: average ')
ax6.imshow(uploaded_ar)
ax6.axis('off')
ax6.set_title(' ')

st.pyplot(fig)
