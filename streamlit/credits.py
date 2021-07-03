import streamlit as st 
import os
import base64
import streamlit.components.v1 as components
import os                      #+Deployment
import inspect                 #+Deployment

@st.cache(allow_output_mutation=True)
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

@st.cache(allow_output_mutation=True)
def get_img_with_href(local_img_path, target_url, size=50):
    img_format = os.path.splitext(local_img_path)[-1].replace('.', '')
    bin_str = get_base64_of_bin_file(local_img_path)
    html_code = f'''
        <a href="{target_url}">
            <img src="data:image/{img_format};base64,{bin_str}" height={size}px/>
        </a>'''
    return html_code


def app():

    currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) 
    logo_dataScientest = get_img_with_href(os.path.join(currentdir, 'ressources/datascientestLogo.png'), 'https://datascientest.com/')
    logo_nebulaText = get_img_with_href(os.path.join(currentdir, 'ressources/nebulaText.png'), 'https://github.com/DataScientest/nebula')

    c1, c2 = st.beta_columns([0.5, 2])
    c1.markdown(logo_dataScientest, unsafe_allow_html=True) 
    c2.markdown(f'''The project Nebula was carried out as part of a Data Scientist training course at the DataScientest institute. (<a href="https://datascientest.com">datascientest.com</a>)''', unsafe_allow_html=True)
    st.write("")
    c1, c2, c3  = st.beta_columns([0.5, 1, 1])
    with c1:
        st.markdown(f'''<u>Project members</u> :''', unsafe_allow_html=True)  
    with c2:
        logo_linkedin = get_img_with_href(os.path.join(currentdir, 'ressources/linkedin.png'), 'https://www.linkedin.com/in/yann-bernery-772a58112/', 20)
        st.markdown(f'''<a href="https://www.linkedin.com/in/yann-bernery-772a58112/" style="text-decoration: none;color:white">Yann BERNERY</a> {logo_linkedin}''', unsafe_allow_html=True) 
    with c3:
        logo_linkedin = get_img_with_href(os.path.join(currentdir, 'ressources/linkedin.png'), 'https://www.linkedin.com/in/cathy-baynaud-samson-b2637817/', 20)
        st.markdown(f'''<a href="https://www.linkedin.com/in/cathy-baynaud-samson-b2637817/" style="text-decoration: none;color:white">Cathy BAYNAUD SAMSON</a> {logo_linkedin}''', unsafe_allow_html=True)       
  
    c1, c2, c3  = st.beta_columns([0.5, 1, 1])
    with c2:
        logo_linkedin = get_img_with_href(os.path.join(currentdir, 'ressources/linkedin.png'), 'https://www.linkedin.com/in/jos%C3%A9-castro-7b62697b/', 20)
        st.markdown(f'''<a href="https://www.linkedin.com/in/jos%C3%A9-castro-7b62697b/" style="text-decoration: none;color:white">Jos&eacute; CASTRO</a> {logo_linkedin}''', unsafe_allow_html=True) 
    with c3:
        logo_linkedin = get_img_with_href(os.path.join(currentdir, 'ressources/linkedin.png'), 'https://www.linkedin.com/in/ludovic-changeon-9047141b1/', 20)
        st.markdown(f'''<a href="https://www.linkedin.com/in/ludovic-changeon-9047141b1/" style="text-decoration: none;color:white">Ludovic CHANGEON</a> {logo_linkedin}''', unsafe_allow_html=True) 


    c1, c2 = st.beta_columns([0.5, 2])
    c1.markdown(f'''<u>Project mentor</u> :''', unsafe_allow_html=True)  
    c2.markdown(f'''Paul DECHORGNAT (DataScientest)''', unsafe_allow_html=True)    

    c1, c2 = st.beta_columns([0.5, 2])
    c1.markdown(f'''<u>Github</u> :''', unsafe_allow_html=True)  
    c2.markdown(f'''<a href="https://github.com/DataScientest/nebula">Nebula project</a>''', unsafe_allow_html=True) 

    c1, c2 = st.beta_columns([0.5, 2])
    c1.markdown(f'''<u>Training data</u> :''', unsafe_allow_html=True)  
    c2.markdown(f'''<a href="https://www.kaggle.com/c/understanding_cloud_organization/">Collected from "Understanding cloud organization" Kaggle competition</a>''', unsafe_allow_html=True) 

    c1, c2 = st.beta_columns([0.5, 2])
    c1.markdown(f'''<u>Demo data</u> :''', unsafe_allow_html=True)  
    c2.markdown(f'''<a href="https://worldview.earthdata.nasa.gov/">Downloaded from EOSDIS Worldview imagery collection</a>''', unsafe_allow_html=True)    
