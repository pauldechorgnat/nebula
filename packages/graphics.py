import numpy as np
import os
import cv2
import PIL
from PIL import Image


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


def rleToMask(rle: str, shape:tuple =(2100, 1400)) -> np.ndarray:
    """Conversion d'un codage RLE en masque

     Paramètre
     ----------
     rle : encodage RLE a convertir 
     shape : format du masque de sortie

     Retour
     ----------
     np.array : masque
    """
    
    #Le code RLE est splite a chaque espace
    #puis on convertit en entier chaque chaine extraite 
    rleNumbers = [int(numstring) for numstring in rle.split(' ')]
    
    #Le tableau obtenu est redimensionner sur 2 colonnes, le nombre
    #de lignes est determine par numpy d'ou -1 
    #Sur chaque ligne nous avons le debut de la suite de pixels a 
    #passer en clair ainsi que le nombre de pixels concernes
    rlePairs = np.array(rleNumbers).reshape(-1,2)
    
    #Une instance d'image est initialisee avec uniquement
    #des zeros sur la base des dimensions passees en parametre    
    img = np.zeros(shape[0]*shape[1],
                   dtype=np.uint8)

    #Pour chaque pairs, on passe les pixels concernes en blanc
    for index,length in rlePairs:
        #index -= 1
        
        img[index:index+length] = 255
    
    #Pour finir l'inage est redimensionnee aux dimensions voulues
    img = img.reshape(shape)
    img = img.T
    
    return img



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


def imshowSuperimposed(repImage: str, nomImage: str, rle: str, classe: str, rleSize: tuple = (2100,1400))-> dict:
    """Superposition d'une image RGB et de sa segmentation RLE, colorée par classe

     Paramètre
     ----------
     repImage : nom du répertoire vers les images
     nomImage : nom de l'image à afficher
     rle : encodage RLE du masque à superposer
     classe : nom de la classe du masque, parmi {'Fish', 'Flower', 'Gravel', 'Sugar'}
     rleSize : taille du masque RLE en pixels
     
     Retour
     ----------
     dict : {'Image': image ndarray ('uint8') RGB avec sa segmentation,
             'Label': nom de l'image / classe de segmentation,
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

    #Si la taille de l(image est différente de celle du masque,
    #on met l'image à l'échelle du masque
    if img.size != rleSize :
        img = img.resize(size = rleSize, resample = PIL.Image.BILINEAR ).convert('RGB')

    #Chargement du masque à partir du codage RLE
    mask = rleToMask(rle, shape = rleSize)

    #Coloration du masque
    couleur = couleurs[classe]              # on récupère la couleur de la classe
    imgMask = np.zeros(rleSize[::-1]+(3,))  # initialisation du masque à 0
    imgMask[:,:,couleur] = np.ones(rleSize[::-1]) * mask  # modification du masque vers trois channels
    imgMask = Image.fromarray(imgMask.astype('uint8')).convert('RGB')

    #Superposition de l'image et de son masque
    #Images converties en numpy.array pour utiliser la fonction addWeighted d'OpenCV
    #Cette fonction est la plus pratique pour conserver l'alpha de l'image originale à 1
    imgOverlay = cv2.addWeighted(np.array(img), 1, np.array(imgMask), 0.5, 0.0)

    dico = {'Image' : imgOverlay,
            'Label' : nomImage + ' / ' + classe,
            'Segmentation': np.array(imgMask)}
    
    return dico



