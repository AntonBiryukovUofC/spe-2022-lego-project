# -*- coding: utf-8 -*-

import streamlit as st
from PIL import Image,  ImageEnhance
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
          response = requests.get(url)
          uploaded_im =  Image.open(requests.get(url, stream=True).raw)


if upload_option == "File Upload" and uploaded_file is not None or upload_option == "URL" and url is not None and url != '':
     im_size = uploaded_im.size
     uploaded_ar = asarray(uploaded_im)
     st.write("Width: " + str(im_size[0]) + '; Height: ' + str(im_size[1]))
     # Slider bars of image enhancement and superpixel adjustments
     col1, col2 = st.columns(2)
     col1.subheader("Adjust Image Enhancements")
     brightness = col1.slider("Brightness", min_value=0.0, max_value=2.0, value=1.0, step=0.2)
     contrast = col1.slider("Contrast", min_value=0.0, max_value=2.0, value=1.0, step=0.2)
     sharpness = col1.slider("Sharpness", min_value=0.0, max_value=2.0, value=1.0, step=0.2)
     col2.subheader("Adjust Image Segmentation")
     compactness = col2.slider("Compactness", min_value=-2.0, max_value=2.0, value=1.0, step=0.1)
     n_segments = col2.slider("Number of segments", min_value=100, max_value=800, value=250, step=5)
     threshold = col2.slider("Threshold", 1, 40, 10)

     # Apply image enhancement
     enhancer_br = ImageEnhance.Brightness(uploaded_im)
     adjusted_br = enhancer_br.enhance(brightness)
     enhancer_contr= ImageEnhance.Contrast(adjusted_br)
     adjusted_br_contr = enhancer_contr.enhance(contrast)
     enhancer_shar = ImageEnhance.Sharpness(adjusted_br_contr)
     adjusted_br_contr_shar = enhancer_shar.enhance(sharpness)
     adjusted_ar = asarray(adjusted_br_contr_shar)

     # Apply image segementation to the original image and enhanced image
     labels_origin= seg.slic(uploaded_ar, compactness=10**compactness, n_segments=n_segments, start_label=1)
     out_avg_origin = color.label2rgb(labels_origin, uploaded_ar, kind='avg', bg_label=0)
     g_origin = graph.rag_mean_color(uploaded_ar, labels_origin)
     labels_graph_cutoff_origin = graph.cut_threshold(labels_origin, g_origin,  thresh=threshold)
     out_rag_origin = color.label2rgb(labels_graph_cutoff_origin, uploaded_ar, kind='avg', bg_label=0)

     labels_adjust = seg.slic(adjusted_ar, compactness=10 ** compactness, n_segments=n_segments, start_label=1)
     out_avg_adjust = color.label2rgb(labels_adjust, adjusted_ar, kind='avg', bg_label=0)
     g_adjust = graph.rag_mean_color(adjusted_ar, labels_adjust)
     labels_graph_cutoff_adjust = graph.cut_threshold(labels_adjust, g_adjust, thresh=threshold)
     out_rag_adjust = color.label2rgb(labels_graph_cutoff_adjust, adjusted_ar, kind='avg', bg_label=0)

     # Generate and display images
     fig = plt.figure()
     fig.set_figheight(10)
     fig.set_figwidth(10)
     ax1 = plt.subplot2grid(shape=(3, 3), loc=(0, 0), colspan=2, rowspan=2)
     ax2 = plt.subplot2grid(shape=(3, 3), loc=(2, 0))
     ax3 = plt.subplot2grid(shape=(3, 3), loc=(2, 1))
     ax4 = plt.subplot2grid(shape=(3, 3), loc=(0, 2))
     ax5 = plt.subplot2grid(shape=(3, 3), loc=(1, 2))
     ax6 = plt.subplot2grid(shape=(3, 3), loc=(2, 2))

     ax1.imshow(adjusted_ar)
     ax1.axis('off')
     ax1.set_title('Enhanced Image')
     ax2.imshow(out_avg_adjust)
     ax2.axis('off')
     ax2.set_title('Segmented Enhanced Image')
     ax3.imshow(out_rag_adjust)
     ax3.axis('off')
     ax3.set_title('Merged Enhanced Image')
     ax4.imshow(out_avg_origin)
     ax4.axis('off')
     ax4.set_title('Segmented Original Image')
     ax5.imshow(out_rag_origin)
     ax5.axis('off')
     ax5.set_title('Merged Original Image')
     ax6.imshow(uploaded_ar)
     ax6.axis('off')
     ax6.set_title('Original Image')

     st.pyplot(fig)
