import streamlit as st
import streamlit.components.v1 as components
import os                      #+Deployment
import inspect                 #+Deployment

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def app():
    currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))  
    local_css(os.path.join(currentdir, "style.css"))
    #Préparation de la page
    st.subheader("NEBULA DATA EXPLORATION")
    st.write("Here is an overview of the data analysed within this study: the cloud flavours and their repartition within the dataset.")
    st.write("Please have a look at the World Scanner to dive into the images (see left sidebar).")
    HtmlFile = open(os.path.join(currentdir, "exploration.html"), 'r', encoding='utf-8')
    source_code = HtmlFile.read() 
    components.html(source_code,height=900)
    return None