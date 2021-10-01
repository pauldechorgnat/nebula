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
          <h2>Our thought</h2>
          <p>
            This project is, of course, not intended to resolve climate change, nevertheless it offers its contribution in several ways:
            <ul>
             <li>By implementing a high-performance model with still very significant room for improvement and maybe opening some tracks 
             (all the code is open source, cf. <a href="https://github.com/DataScientest/nebula">project's Github repository</a> )</li>
             <li>By raising the awareness of visitors who will come to discover this application,</li>
             <li>By the compatibility of the modeling process with other computer vision needs,</li>
             <li>And perhaps who knows by the vocations that the project may have aroused among future data scientists.</li>
            </ul>
          </p>
          ''', unsafe_allow_html=True)