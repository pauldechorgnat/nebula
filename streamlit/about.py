import streamlit as st 

def app():

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
          <h2>ABOUT NEBULA</h2>
          <p>
            The present demo is part of a data science project carried out in the frame of a training course at the <a href="https://datascientest.com">DATASCIENTEST institute</a>.
          </p>
          <p>
            This project, named NEBULA, aims to detect and localize in satellite photos four specific types of cloud formations: 
            Flower, Fish, Gravel and Sugar, so named because of their characteristic pattern.
          </p>
          <p>
            The NEBULA project is based on a 2019 Kaggle competition, initiated by the Max Planck Institute. Main purpose was to 
            mobilize the data scientist community on the realization of models capable of identifying shallow cloud locations, 
            considered as potential key factors in climate’s understanding.
          </p>
          <p>
           In this frame, we developed a convolutional neural network model trained to identify and localize the above four cloud formations.
          </p>
          <p>
           The present application demonstrates our model in action. It contains two main functions.
          </p>
          <h3><b><i>NEBULA data exploration :</i></b></h3>          
          <p>This introductory deals with some statistics resulting from the exploratory analysis of the model learning data. 
           The center picture illustrates the photos submitted to the models. This photo is interesting in that it contains the four 
           classes of clouds. Each class is associated with a color (red for Flower, blue for Fish, green for Gravel and yellow for Sugar). 
           The colors result from input data and may be difficult to read for color blind people, we apologize.<br>
           Fuzzy cloud patterns made it necessary to use deep learning techniques.
          </p>
          <h3><b><i>NEBULA world scanner :</i></b></h3>          
          <p>The scanner is the demonstration of the model in action. In this part, you can use the available selections 
          (day of capture and map) to load an image, unknown to the model, from the NASA EOSDIS imagery collection. 
          It is possible to deal with photos or videos (10 photos in a row). Clicking on the “Identify clouds” button will request 
          our model to assess the presence and localization of cloud formations. Model predictions are materialized by overlays 
          of masks or color boxes.
          </p>
          ''', unsafe_allow_html=True)