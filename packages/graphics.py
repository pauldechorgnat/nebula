import numpy as np
import os
import cv2
import PIL
from PIL import Image
from skimage.segmentation import mark_boundaries
from skimage.measure import label, regionprops


#-----------------------------------------------------------
# PROJET NEBULA
# Datascientest DS continu oct. 2020
# Librairie : GRAPHICS
#             Traitement des images et masques RLE
# Auteurs : Cathy Baynaud Samson
#           José Castro
#           Yann Bernery
#           Ludovic Changeon
#-----------------------------------------------------------

def np_transposition(image: np.ndarray, input_shape: tuple) -> np.ndarray:
    """
    Transposition d'un np array afin d'inverser les dimensions (hauteur, largeur)
    vers (largeur, hauteur).
    Si les dimensions initiales sont différentes de (height,width), un redimensionnement est effectué.

     Paramètre
     ----------
     image : np array a transposer
     input_shape : dimensions de l'image cible

     Retour
     ----------
     np.array : image transposee
    """

    height, width = input_shape
    return cv2.resize(image, (width, height))


def rleToMask(rle: str, shape: tuple  =(1400, 2100)) -> np.ndarray:
    """
    Conversion d'un codage RLE en masque

     Paramètre
     ----------
     rle   : encodage RLE a convertir
     shape : format du masque

     Retour
     ----------
     np.array : masque
    """

    width, height = shape[:2]

    mask= np.zeros( width*height ).astype(np.uint8)

    array = np.asarray([int(x) for x in rle.split()])
    starts = array[0::2]
    lengths = array[1::2]

    current_position = 0
    for index, start in enumerate(starts):
        mask[int(start):int(start+lengths[index])] = 1
        current_position += lengths[index]

    return mask.reshape(height, width).T


def maskToRle(mask: np.ndarray) -> str:
    """
    Conversion d'un masque en encodage RLE
    La presence d'un pixel dans le masque se materialise par la valeur 1,
    autrement la valeur reste a 0

     Paramètre
     ----------
     mask : masque a encoder

     Retour
     ----------
     str : encodage RLE
    """

    valeur_pixels = mask.T.flatten()
    valeur_pixels = np.concatenate([[0], valeur_pixels, [0]])
    segment_rle = np.where(valeur_pixels[1:] != valeur_pixels[:-1])[0] + 1
    segment_rle[1::2] -= segment_rle[::2]
    return ' '.join(str(x) for x in segment_rle)


def list_rleToMask(rle_list:[str], input_shape:tuple, reshape: tuple = None)  -> np.ndarray :
    """
    Conversion d'une liste d'encodage RLE en liste de masques

     Paramètre
     ----------
     rle_list    : liste des encodage RLE a convertir
     input_shape : taille d'origine des masques
     reshape     : facultatif, taille desiree en sortie

     Retour
     ----------
      np.ndarray : liste des masques
    """

    nb_rle = len(rle_list)
    if reshape is None:
        mask_list = np.zeros((*input_shape, nb_rle))
    else:
        mask_list = np.zeros((*reshape, nb_rle))

    for i, rle in enumerate(rle_list):
        if type(rle) is str:
            if reshape is None:
                mask_list[:, :, i] = rleToMask(rle, input_shape)
            else:
                mask = rleToMask(rle, input_shape)
                reshaped_mask = np_transposition(mask, reshape)
                mask_list[:, :, i] = reshaped_mask

    return mask_list


def list_maskToRle(mask_list:np.ndarray , reshape:tuple = None) -> [str]:
    """
    Encodage d'une liste de masques en codes RLE

     Paramètre
     ----------
     mask_list   : liste des masques a encoder
     reshape     : facultatif, taille desiree des masques avant encodage

     Retour
     ----------
      liste de str : liste des codes RLE
    """

    width, height, nb_mask = mask_list.shape

    rle_list = []

    for i in range(nb_mask):
        mask = mask_list[:, :, i]

        if reshape:
            mask = mask.astype(np.float32)
            mask = np_transposition(mask, reshape).astype(np.int64)

        rle = maskToRle(mask)
        rle_list.append(rle)

    return rle_list


def surfaceFromRle(rle: str) -> int:
    """Determination de la surface (en pixels) converte par le masque correspondage
       a l'encodage RLE specifie en parametre

     Paramètre
     ----------
     rle : encodage RLE a analyser

     Retour
     ----------
     int : surface couverte en pixels
    """


    #Initialisation de la surface
    surface = 0

    rleNumbers = [int(numstring) for numstring in rle.split(' ')]
    rlePairs = np.array(rleNumbers).reshape(-1,2)

    #Pour chaque pairs, on incrémente la surface par la nouvelle
    #longueur de chaine
    for index,length in rlePairs:
        surface += length

    return surface


def imshowSuperimposed(nomImage: str, rle: str = '', classe: str = 'Fish', repImage: str = '.', rleSize: tuple = (1400,2100))-> dict:
    """Superposition d'une image RGB et de sa segmentation RLE, colorée par classe

     Paramètre
     ----------
     nomImage : nom de l'image à afficher
     repImage : nom du répertoire vers les images ('.' par défaut)
     rle : encodage RLE du masque à superposer
     classe : nom de la classe du masque, parmi {'Fish', 'Flower', 'Gravel', 'Sugar'}
     rleSize : taille du masque RLE en pixels

     Retour
     ----------
     dict : {'Superimposed': image ndarray ('uint8') RGB avec sa segmentation,
             'Label': nom de l'image / classe de segmentation,
             'Image': image originale ndarray ('uint8') RGB,
             'Segmentation': image ndarray ('uint8') RGB du masque de segmentation}
    """

    #Initialisation du dictionnaire des couleurs (sur base de RGB)
    couleurs = {'Fish':  2, #blue
                'Flower':0, #red
                'Gravel':1, #green
                'Sugar':slice(0,2,1)} #yellow

    #Chargement de l'image demandée
    path = os.path.join(repImage, nomImage)
    img = Image.open(path)

    #Si la taille de l'image est différente de celle du masque,
    #on met l'image à l'échelle du masque
    img = img.resize(size = rleSize[::-1], resample = Image.BILINEAR ).convert('RGB')

    #Chargement du masque à partir du codage RLE
    mask = np.zeros(rleSize)
    if rle != '' : mask = rleToMask(rle, shape = rleSize)

    #Coloration du masque
    couleur = couleurs[classe]                            # on récupère la couleur de la classe
    imgMask = np.zeros(rleSize+(3,))                      # initialisation du masque pour 3 channels
    imgMask[:,:,couleur] =  np.dstack([mask,mask,mask])[:,:,couleur] * 255  # modification du masque vers trois channels
    imgMask = Image.fromarray(imgMask.astype('uint8'))

    #Superposition de l'image et de son masque
    #Images converties en numpy.array pour utiliser la fonction addWeighted d'OpenCV
    #Cette fonction est la plus pratique pour conserver l'alpha de l'image originale à 1

    imgOverlay = cv2.addWeighted(np.array(img), 1, np.array(imgMask), 0.5, 0.0)

    #Si le code rle fourni était vide, on efface la classe par défaut
    if rle == '': classe = ''

    dico = {'Superimposed' : imgOverlay,
            'Label' : nomImage + ' / ' + classe,
            'Image' : np.array(img),
            'Segmentation': np.array(imgMask)}

    return dico


def trace_boundingBox(image : np.ndarray,
                      mask : np.ndarray,
                      color : tuple = (0,0,255),
                      width : int = 10):
    """
    Draw a bounding box on image

     Parameter
     ----------
     image : image on which we want to draw the box
     mask  : mask to process
     color : color we want to use to draw the box edges
     width : box edges's width

     Return
     ----------
     None
    """

    lbl = label(mask)
    props = regionprops(lbl)
    for prop in props:
        coin1 = (prop.bbox[3], prop.bbox[2])
        coin2 = (prop.bbox[1], prop.bbox[0])
        cv2.rectangle(image, coin2, coin1, color, width)
    return None


def maskInColor(image : np.ndarray,
                mask : np.ndarray,
                color : tuple = (0,0,255),
                alpha : float=0.2) -> np.ndarray:
    """
    Superposition d'un masque sur une image

     Parameter
     ----------
     image : image sur laqelle le masque doit etre superpose
     mask  : masque a superposer
     color : colour du masque
     alpha : coefficient d'opacite

     Return
     ----------
     np.array : image resultant de la superposition
    """

    image = np.array(image)
    H,W,C = image.shape
    mask    = mask.reshape(H,W,1)
    overlay = image.astype(np.float32)
    overlay =  255-(255-overlay)*(1-mask*alpha*color/255 )
    overlay = np.clip(overlay,0,255)
    overlay = overlay.astype(np.uint8)
    return overlay


def cloudInColor(image : np.ndarray,
                 mask : np.ndarray,
                 color : tuple = (0,0,255),
                 alpha : float = 0.7,
                 threshold : int = 90) -> np.ndarray:
    """
    Coloration des pixels d'une image sur la base d'un seuil

     Parameter
     ----------
     image : image a colorer
     mask  : masque de traitement
     color : couleur a appliquer
     alpha : coefficient d'opacite
     threshold : seuil

     Return
     ----------
     np.array : image coloree
    """

    imZone = cv2.bitwise_and(image, image, mask=mask)
    image_gray = cv2.cvtColor(imZone, cv2.COLOR_RGB2GRAY)
    (thresh, blackAndWhiteImage) = cv2.threshold(image_gray,
                                                 threshold,
                                                 255,
                                                 cv2.THRESH_BINARY)
    inlay = maskInColor(image, blackAndWhiteImage, color=color, alpha=alpha)
    return inlay
