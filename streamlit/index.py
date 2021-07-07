import streamlit as st 

import os                      #+Deployment
import inspect                 #+Deployment
import scanner
import help
import exploration
import gallery
import credits
import home
import about
import bilan

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

logo = os.path.join(currentdir, 'ressources/nebulaLogo_light.png')
PAGE_CONFIG = {"page_title":"Nebula.io","page_icon": logo,"layout":"wide"}
st.set_page_config(**PAGE_CONFIG)

MENU = {
    "Home" : home,
    "About Nebula" : about,
    "Nebula Data Exploration" : exploration,
    "Nebula World Scanner" : scanner,
    "Our thought" : bilan,
    "Gallery" : gallery,    
    "Help" : help,
    "Credits" : credits
}

st.sidebar.title('Menu')
selection_page = st.sidebar.radio("",list(MENU.keys()))
page = MENU[selection_page]
page.app()