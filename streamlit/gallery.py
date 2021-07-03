import streamlit as st 
import json
import os                      #+Deployment
import inspect                 #+Deployment

def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def app():

    currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) 
    st.subheader("NEBULA GALLERY")

    gallery_content = open(os.path.join(currentdir, 'ressources/gallery.json'))
    data  = json.load(gallery_content)

    for images_row in chunks(data['gallery']['images'], 3):
        c1, c2, c3 = st.beta_columns([1, 1, 1])
        if len(images_row)>=1: c1.image(images_row[0]['image-link'], caption=images_row[0]['image-desc'], use_column_width='always') 
        if len(images_row)>=2: c2.image(images_row[1]['image-link'], caption=images_row[1]['image-desc'], use_column_width='always') 
        if len(images_row)==3: c3.image(images_row[2]['image-link'], caption=images_row[2]['image-desc'], use_column_width='always')
