import streamlit as st 
import os                      #+Deployment
import inspect                 #+Deployment

def app():

    currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) 
    st.image(os.path.join(currentdir, 'ressources/home.jpg'))
    st.write("The nebula project has consisted in implementing a neural network with the objective \
               to identify specifics classes of clouds from satellite photos.")
    st.write("")
    st.write("This streamlit application is the demo of nebula project's works.")