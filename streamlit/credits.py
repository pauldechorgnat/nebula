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
def get_img_with_href(local_img_path, target_url):
    img_format = os.path.splitext(local_img_path)[-1].replace('.', '')
    bin_str = get_base64_of_bin_file(local_img_path)
    html_code = f'''
        <a href="{target_url}">
            <img src="data:image/{img_format};base64,{bin_str}" height=80px/>
        </a>'''
    return html_code


def app():

    currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) 
    logo_dataScientest = get_img_with_href(os.path.join(currentdir, 'ressources/datascientestLogo.png'), 'https://datascientest.com/')
    logo_nebulaText = get_img_with_href(os.path.join(currentdir, 'ressources/nebulaText.png'), 'https://github.com/DataScientest/nebula')

    c1, c2, c3 = st.beta_columns([1, 1, 1])
    c1.markdown(logo_dataScientest, unsafe_allow_html=True) 
    c3.markdown(logo_nebulaText, unsafe_allow_html=True) 

    st.write("")
    st.write("The project Nebula was carried out as part of a Data Scientist training course at the DataScientest institute.")
    st.write("")
    st.markdown(f'''<u>Project members</u> : Cathy Baynaud-Samson, Yann Bernery, José Castro and Ludovic Changeon''', unsafe_allow_html=True)   
    st.markdown(f'''<u>Project mentor</u> : Paul Dechorgnat (DataScientest)''', unsafe_allow_html=True)       
    st.markdown(f'''<u>Github</u> : <a href="https://github.com/DataScientest/nebula">Nebula project</a>''', unsafe_allow_html=True)
    st.markdown(f'''<u>DataScientest</u> : <a href="https://datascientest.com">DataScientest institute</a>''', unsafe_allow_html=True)    
    st.markdown(f'''<u>Training data</u> : <a href="https://www.kaggle.com/c/understanding_cloud_organization/">Collected from "Understanding cloud organization" Kaggle competition</a>''', unsafe_allow_html=True)       
    st.markdown(f'''<u>Demo data</u> : <a href="https://worldview.earthdata.nasa.gov/">Downloaded from EOSDIS Worldview imagery collection</a>''', unsafe_allow_html=True)           
    c1, c2, c3, c4 = st.beta_columns([1, 1, 1, 1])
    with c1:
        components.html("""
             <script type="text/javascript" src="https://platform.linkedin.com/badges/js/profile.js" async defer></script>
             <div class="LI-profile-badge"  data-version="v1" data-size="medium" data-locale="en_US" data-type="horizontal" data-theme="dark" data-vanity="ludovic-changeon-9047141b1"><a class="LI-simple-link" href='https://jp.linkedin.com/in/ludovic-changeon-9047141b1/en-us?trk=profile-badge'>LUDOVIC CHANGEON</a></div>
             """, height=280)