import numpy as np


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





