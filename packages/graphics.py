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





