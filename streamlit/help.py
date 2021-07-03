import streamlit as st 
import matplotlib.pyplot as plt
import os                      #+Deployment
import inspect                 #+Deployment

def app():

    currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) 

    st.markdown(f"""
                <style>
                  .reportview-container .main .block-container{{
                    padding-top: 0 rem;
                    marging-top: 0 rem;
                  }}
                  .reportview-container .main{{
                    padding-top: 0 rem;
                    marging-top: 0 rem;
                  }}                  
                </style>
               """, unsafe_allow_html=True)
  
    st.markdown('''
          <h2>HELP</h2>
          <p>
            NEBULA DATA EXPLORATION enables you to get a few hints on the data analysed within the project.<br>  
            At the center: an example of the input satellite pictures.<br>
            On the left and right hand sides: a few plots summarizing high level figures about the dataset.
          </p>
          <p>
            NEBULA WORLD SCANNER is a tool which makes it possible to exploit neural networks to identify particular cloud formations. 
            There are four cloud formations: Fish, Sugar, Gravel and Flower, so named because of their specific shape.<BR> 
            The data (photos and videos) come from the NASA EOSDIS system.
          </p>
          <h3>Data selection</h3>          
          <p>The upper part of the screen contains the following selection options:</p>
          <p><b>Capture date:</b> This is the date of the day the photo was taken. It is possible to choose a date between 2001/01/01 
             and the date of current day - 20 days.</p> 
          <p><b>Photo / video:</b> The user can choose to apply the model on a photo of the area taken on the selected date, 
             or a video covering a period of 10 days from the selected date. Videos have a frequency of 1 frame per second.</p>
          <h3>Map</h3>             
          <p>The central part of the screen is composed, on the left, of a dynamic world map. The user chooses area by clicking on the map 
             or by using sliders below. On the right, a dynamic screen will show photos or videos from the selections.</p>
          ''', unsafe_allow_html=True)

    c1, c2 = st.beta_columns([1,5])
    c1.image(plt.imread(os.path.join(currentdir, 'ressources/help_sat.jpg')))
    c2.markdown('''The area covered by the satellite is materialized on the main map by a green frame illustrated with a satellite icon.''', unsafe_allow_html=True)
    st.markdown('''
          <h3>Model predictions</h3>   
          <p>The lower part of the screen allows to launch the model on the extracted photos and videos.</p>
          ''', unsafe_allow_html=True)     
    c1, c2 = st.beta_columns([1,5])
    c1.image(plt.imread(os.path.join(currentdir, 'ressources/legend.png')))
    c2.markdown('''First of all, on the left, there is a legend affecting a color to each cloud formation. This will be particularly 
               useful for easily distinguish the classes on the masks resulting from the segmentation.''', unsafe_allow_html=True)
    st.markdown('''
           <h3>Identify clouds</h3>   
           <p>On the left this is the part dealing with the segmentation of photos or videos. This means that a neural network 
              trained for this purpose will identify and locate cloud formations.</p>
           <p>3 cloud formations visualization options are available :</p>''', unsafe_allow_html=True)

    c1, c2 = st.beta_columns([1,5])
    c1.image(plt.imread(os.path.join(currentdir, 'ressources/mask_help.jpg')))
    c2.markdown('''Clouds Masks: Predictions from the segmentation model are displayed as mask with the color of the cloud formation concerned.''', unsafe_allow_html=True)

    c1, c2 = st.beta_columns([1,5])
    c1.image(plt.imread(os.path.join(currentdir, 'ressources/boxes_help.jpg')))
    c2.markdown('''Boxes : Predictions are framed.''', unsafe_allow_html=True)

    c1, c2 = st.beta_columns([1,5])
    c1.image(plt.imread(os.path.join(currentdir, 'ressources/cloud_help.jpg')))
    c2.markdown('''Coloring : Clouds are colored.''', unsafe_allow_html=True)

    st.markdown('''
           <h3>Classification</h3>   
           <p>The central part deals with classification. Classification model does not directly locate the cloud formations 
              but returns the probability that each of them belongs to the image. <br>
              It is currently not possible to do a classification on a video.</p>''', unsafe_allow_html=True)