# -*- coding: utf-8 -*-

import streamlit as st
from PIL import Image,  ImageEnhance
import requests
import pandas as pd
from numpy import asarray, uint8, random
import matplotlib.pyplot as plt
from matplotlib import cm
from skimage import data,  color
import skimage.segmentation as seg
from skimage.future import graph
import json
import subprocess


def image_generator(image, brightness, contrast, sharpness, compactness, n_segments, threshold):
     # Apply image enhancement
     enhancer_br = ImageEnhance.Brightness(image)
     adjusted_br = enhancer_br.enhance(brightness)
     enhancer_contr = ImageEnhance.Contrast(adjusted_br)
     adjusted_br_contr = enhancer_contr.enhance(contrast)
     enhancer_shar = ImageEnhance.Sharpness(adjusted_br_contr)
     adjusted_br_contr_shar = enhancer_shar.enhance(sharpness)
     adjusted_ar = asarray(adjusted_br_contr_shar)

     # Apply image segementation to the enhanced image
     labels_adjust = seg.slic(adjusted_ar, compactness=10**compactness, n_segments=n_segments, start_label=1)
     g_adjust = graph.rag_mean_color(adjusted_ar, labels_adjust)
     labels_graph_cutoff_adjust = graph.cut_threshold(labels_adjust, g_adjust, thresh=threshold)
     out_rag_adjust = color.label2rgb(labels_graph_cutoff_adjust, adjusted_ar, kind='avg', bg_label=0)
     return out_rag_adjust


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



     # Generate Random parameters
     random_nums_brightness = random.normal(loc=0.0, scale=0.4, size=3)
     random_nums_contrast = random.normal(loc=0.0, scale=0.4, size=3)
     random_nums_sharpness = random.normal(loc=0.0, scale=0.4, size=3)
     random_nums_compactness = random.normal(loc=0.0, scale=0.8, size=3)
     random_nums_threshold = random.normal(loc=0, scale=8, size=3)

     # Generate image with random parameters
     new_images = []
     for i in range(len(random_nums_contrast)):

         new_img = image_generator(image=uploaded_im, brightness=brightness+random_nums_brightness[i],
                                   contrast=contrast+random_nums_contrast[i],
                                   sharpness=sharpness+random_nums_sharpness[i],
                                   compactness=compactness+random_nums_compactness,
                                   n_segments=n_segments,
                                   threshold=threshold+random_nums_threshold[i],)
         new_images.append(new_img)





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

     ax1.imshow(out_rag_adjust)
     ax1.axis('off')
     ax1.set_title('Merged Enhanced Image')
     ax2.imshow(new_images[0])
     ax2.axis('off')
     ax2.set_title('REM 1')
     ax3.imshow(new_images[1])
     ax3.axis('off')
     ax3.set_title('REM 2')
     ax4.imshow(adjusted_ar)
     ax4.axis('off')
     ax4.set_title('Enhanced Image')
     ax5.imshow(uploaded_ar)
     ax5.axis('off')
     ax5.set_title('Original Image')
     ax6.imshow(new_images[2])
     ax6.axis('off')
     ax6.set_title('REM 3')

     st.pyplot(fig)




     # Prepare for R-Brickr: Save Merged Enhanced Image, save parameters for brickr
     im = Image.fromarray(out_rag_adjust)
     im.save("MEI.png")

     params = {'data_path': 'path/to/image.png',
               'img_size': (64,out_rag_adjust.shape[0]*64//out_rag_adjust.shape[1]),
               'color_palette': ['universal', "generic", "special"],
               'method': 'cie94',
               'use_bricks': ['6x4', '6x2', '4x2', '3x2', '2x2', '4x1','3x1', '2x1', '1x1']}
     with open('params.json', 'w') as f:
          json.dump(params, f)

     # running R code
     subprocess.run(["Rscript", "RCode_brickr.R"])

     # Load mosaic image from disk and display
     mosaic_im = Image.open('MEI_Mosaic.png')
     # Load table of lego pieces
     pieces = pd.read_csv('MEI_pieces.csv')

     # Display 1.legofied image 2. lego pieces in column
     col1, col2 = st.columns(2)
     with col1:
          st.subheader('Your Legofied Image')
          st.image(mosaic_im, caption='Mosaic Image')

     with col2:
          st.subheader('The Lego Pieces You  Need')
          st.dataframe(pieces, height=500)
          #st.table(pieces)

