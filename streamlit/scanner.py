import streamlit as st 
import streamlit.components.v1 as components
import matplotlib.pyplot as plt
from PIL import Image
import gdown
import os                      #+Deployment
import sys                     #+Deployment
import inspect                 #+Deployment
import cv2
import requests
import ast
from datetime import datetime, timedelta, date
import numpy as np
import moviepy.video.io.ImageSequenceClip
import segmentation_models as sm
from streamlit.report_thread import get_report_ctx
import SessionState
import base64
import time

sm.set_framework('tf.keras')

#+Deployment
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))  
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 

import packages

_nebulaMap = components.declare_component(
    "nebulaMap",
    #url="https://brave-mouse-60.loca.lt",
    path = os.path.join(currentdir, 'nebulaMap')
)

def nebulaMap(lat=0, long=0, key=None):
    nebulaMap_value = _nebulaMap(lat=lat, long=long, key=key, default=0)
    return nebulaMap_value

#===============================================================================
# Chargement des styles
#===============================================================================
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

#===============================================================================
# Chargement de la carte principale (mise en cache)
#===============================================================================
@st.cache
def load_image():
    return plt.imread(os.path.join(currentdir, 'ressources/mapScan2.jpg'))

#===============================================================================
# Chargement du logo (mise en cache)
#===============================================================================
@st.cache
def load_logo():
    return plt.imread(os.path.join(currentdir, 'ressources/inprocess.jpg'))

#===============================================================================
# Chargement du logo anime (mise en cache)
#===============================================================================
@st.cache
def load_gif():
    file_ = open(os.path.join(currentdir, "ressources/inprocess.gif"), "rb")
    contents = file_.read()
    data_url = base64.b64encode(contents).decode("utf-8")
    file_.close()
    return data_url

#===============================================================================
# Chargement de la legende (mise en cache)
#===============================================================================
@st.cache
def load_legend():
     return plt.imread(os.path.join(currentdir, 'ressources/legend.png'))

#===============================================================================
# Chargement du model (mise en cache)
#===============================================================================
@st.cache(allow_output_mutation=True)
def load_model():

    target_size = (320, 480)
    nb_classes = 4
    nb_canaux = 3

    if not os.path.isfile('efficientnetb1n.index'):
        with st.spinner("Downloading model... this may take a while! \n Don't stop it!"):
            gdown.download('https://drive.google.com/uc?id=1DzUDrmMHZ-Z69P2k5gmB3l6ls_lFa4k4', 'efficientnetb1n.index', quiet=False)
            gdown.download('https://drive.google.com/uc?id=14bk-9aDeQ8RbQGI1CN8UpuHTLe2NdQEb', 'efficientnetb1n.data-00000-of-00001', quiet=False)

    segmArch = packages.buildSegmentationModel2(sm, nb_classes, target_size, nb_canaux)
    modelS = packages.NebulaWrapper(segmArch, autoInit=False)
    modelS.load_weights('efficientnetb1n')
    return modelS

#===============================================================================
# Récupération d'une photo satellite depuis l'appli worldview de la NASA
#===============================================================================
def get_earthdataView(coord, image_date, image_heure='08:00:00', target_size=(320, 480)):
    if isinstance(coord, str):
        coord = ast.literal_eval(coord)
    coords = [str(coord[0]-6), str(coord[1]-9), str(coord[0]+6), str(coord[1]+9)]

    url = "https://wvs.earthdata.nasa.gov/api/v1/snapshot?REQUEST=GetSnapshot&TIME="+image_date+"T"+image_heure+"Z&BBOX="+coords[0]+","+coords[1]+","+coords[2]+","+coords[3]+"&CRS=EPSG:4326&LAYERS=MODIS_Aqua_CorrectedReflectance_TrueColor,Coastlines_15m&WRAP=day,x&FORMAT=image/jpeg&WIDTH=480&HEIGHT=320&ts=1619077410459"
    im = Image.open(requests.get(url, stream=True).raw)
    im = im.resize((target_size[1], target_size[0]), Image.ANTIALIAS) 
    return im

#===============================================================================
# Extarction des frames de la video (periode de 10 jours)
#===============================================================================
def getVideoFrames(coord, image_date) :
    periode = 10            #Nombre de jours
    frames = []

    #Recuperation des images
    for i in range(periode): 
        image_date += timedelta(days=1)
        im = get_earthdataView(coord, image_date.strftime("%Y-%m-%d"))
        frames.append(np.array(im))

    return frames

#===============================================================================
# Generation de la video 
#===============================================================================
def makeVideo(frames):
    fps = 1                 #Frames par seconde  
    clip = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(frames, fps=fps)
    clip.write_videofile('my_video.mp4')
    video_file = open('my_video.mp4', 'rb')
    video_bytes = video_file.read()    
    return video_bytes

#===============================================================================
# 
#===============================================================================
def postTraitements(pred_mask, seuil, surface):

    #Activation des pixels sur la base d'un seuil spécifique
    pred_mask = cv2.threshold(pred_mask, seuil, 1, cv2.THRESH_BINARY)[1]

    #on vérifie la superficie qui en résulte ...
    # ... la taille minimale est atteinte, on retient ce masque
    if pred_mask.sum() >= surface:
        return pred_mask
    
    # ... la taille minimale n'est pas atteinte, on fait un reset du masque
    return  np.zeros(pred_mask.shape, np.float32) 

#===============================================================================
# 
#===============================================================================
def processSegmentation(model, im, couleurs, seg_option, maskSeuils, surfaces, doClassif):
    im_tensor = packages.imageToTensor(im) 
    preds_nasa= model.predict(im_tensor, verbose=0)
    
    preds_classes = [0] * 4       #Init predictions array for classif results

    im = np.array(im)
    for k in range(4):
        
        preds_classes[k] = np.max(preds_nasa[0,:,:,k])      #Compute classification
        mask = postTraitements(preds_nasa[0,:,:,k], maskSeuils[k], surfaces[k])
        if mask.sum() == 0:
            preds_classes[k] = 0 

        if seg_option == 'Boxes':
            packages.trace_boundingBox(im, mask, color=couleurs[k], width=3, smin=surfaces[k])
        elif seg_option == 'Coloring':
            mask = mask.astype(np.uint8)
            im = packages.cloudInColor(im, mask, color=couleurs[k], alpha=0.85, threshold=110)          
        else:
            im = packages.maskInColor(im, mask, color=couleurs[k], alpha=0.3)
    
    if doClassif:
        return im, preds_classes
    else:
        return im

#===============================================================================
# 
#===============================================================================
def iterateSegmentation(model, frames, couleurs, seg_option, maskSeuils, surfaces):
    segmentedFrames = []
    for frame in frames:
        im = processSegmentation(model, frame, couleurs, seg_option, maskSeuils, surfaces, False)
        segmentedFrames.append(im)
    return segmentedFrames


def app():
    local_css(os.path.join(currentdir, "style.css"))

    image_heure = '08:00:00'
    couleurs=[(0,0,255), (255,0,0), (0,255,0), (255,255,0)]

    maskSeuils = [.5,  .51, .48, .45]
    surfaces = [17385, 19068, 15993, 14297]
    plot_colors = ['blue', 'red', 'green', 'yellow']
    labels = ['Fish', 'Flower', 'Gravel', 'Sugar']
    initial_coords = [18, -56]

    #Initialisation des variables de session
    # imgSession = dernier image satellite recue
    # vidSession = frames de la derniere video generee

    session_state = SessionState.get(imgSession=None, vidSession=None)

    st.subheader("NEBULA WORLD SCANNER")

    modelS = load_model()

    logo = load_logo()
    logo_gif = load_gif()
    legend = load_legend()

    with st.form('headerForm'):
        headerCol1, headerCol2, headerColInter, headerCol3, headerCol4 = st.beta_columns([0.6, 0.7, 0.1, 0.6, 0.5])

        with headerCol1:
            st.markdown('''
                 <SPAN style="font-size:13px; color:white">
                 1. Click on the map or use sliders,<BR>
                 <BR>
                  <BR>
                 </SPAN>
          ''', unsafe_allow_html=True)

        with headerCol2:
            image_date = st.date_input("2. Set the day of capture,", date(2019, 2, 20),
                                      min_value = date(2001, 1, 1),
                                      max_value = (datetime.today() - timedelta(days=20)).date())

        with headerCol3:
            st.markdown('''
                 <SPAN style="font-size:13px; color:white">
                 3. Choose Photo/Video,<BR>
                 </SPAN>
                ''', unsafe_allow_html=True)
            sel_nature = st.radio("", ('Photo', 'Video (10 days)'))

        with headerCol4:
            st.markdown('''
                 <SPAN style="font-size:13px; color:white">
                 4. Push Scan,
                 </SPAN>
                ''', unsafe_allow_html=True)
            goscan = st.form_submit_button("Scan") 

        mainCol1, mainCol2 = st.beta_columns(2)

        with mainCol1:

            coord = nebulaMap(lat=initial_coords[0], long=initial_coords[1])
            if isinstance(coord, int):
                coord = initial_coords

        with mainCol2:
            scanLocation = st.empty()

    with st.form('segForm'):
        processCol1, processCol2, processCol3 = st.beta_columns([1, 2, 2])
        with processCol1:
            st.image(legend)
        with processCol2:
            clsLocation = st.empty()
        with processCol3:
            st.markdown('''
              <SPAN style="font-size:13px; color:white">
              5. Choose display options,
              </SPAN>
              ''', unsafe_allow_html=True)
            seg_option = st.radio("", ('Clouds Masks', 'Boxes', 'Coloring'))
            st.markdown('''
              <SPAN style="font-size:13px; color:white">
              6. Then, identify clouds !
              </SPAN>
              ''', unsafe_allow_html=True)
            gosegmentation = st.form_submit_button('Identify Cloud >>')  

    video = True
    if sel_nature == 'Photo':
        video = False

    if not gosegmentation:
        if video:
            scanLocation.image(logo, use_column_width='always')
            video_frames = getVideoFrames(coord, image_date)   #Extraction des frames
            session_state.vidSession = video_frames                    #Mise en session
            video_bytes = makeVideo(video_frames)                      #Generation video
            scanLocation.video(video_bytes)                #Affichage video
            
        else:  
            scanLocation.image(logo, use_column_width='always')
            im1 = get_earthdataView(coord, image_date.strftime("%Y-%m-%d")) #Extraction image
            session_state.imgSession = im1                                          #Mise en session
            scanLocation.image(im1, use_column_width='always')                      #Affichage image
            

    if gosegmentation:
        if video:
            scanLocation.markdown(
                f'<img src="data:image/gif;base64,{logo_gif}" width=100% alt="cat gif">',
                unsafe_allow_html=True,
            )
            #scanLocation.image(logo, use_column_width='always')
            video_frames = session_state.vidSession
            video_frames = iterateSegmentation(modelS, video_frames, couleurs, seg_option, maskSeuils, surfaces)
            video_bytes = makeVideo(video_frames)                      #Generation video
            scanLocation.video(video_bytes)                #Affichage video
        else:
            scanLocation.markdown(
                f'<img src="data:image/gif;base64,{logo_gif}" width=100% alt="cat gif">',
                unsafe_allow_html=True,
            )
            #scanLocation.image(logo, use_column_width='always')
            im1 = session_state.imgSession
            im1, pred_classes = processSegmentation(modelS, im1, couleurs, seg_option, maskSeuils, surfaces, doClassif=True)
            scanLocation.image(im1, use_column_width='always') 
            if sum(pred_classes)!=0:
                fig, ax = plt.subplots(figsize=(7, 3))
                ax.bar(labels, pred_classes, color=plot_colors)  
                clsLocation.pyplot(fig)
