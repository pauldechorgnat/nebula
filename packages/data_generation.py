import numpy as np
from sklearn.model_selection import train_test_split
from keras.preprocessing.image import ImageDataGenerator


#-----------------------------------------------------------
# PROJET NEBULA
# Datascientest DS continu oct. 2020
# Librairie : DATA_GENERATION
#             Split des donnees
#             DataGeneration avec ou sans augmentation
# Auteurs : Cathy Baynaud Samson
#           José Castro
#           Yann Bernery
#           Ludovic Changeon
#-----------------------------------------------------------


def splitValid(*args, randomState:int = 123, test_size:(float,int) = 0.2, shuffle:bool = True):
    """Separation d'un set en deux parties distinctes 

     Paramètre
     ----------
     X           : set a separer
     y           : variables d'interets (peut etre omise)
     randomState : graine
     test_size   : proportions des donnees entre les deux split
     shuffle     : melange ou non des donnees avant le split

     Retour
     ----------
     arrays : ensemble des sets resultants de la separation
    """
    
    if len(args)==1 :  
        split1, split2 = train_test_split(args[0], test_size = test_size, random_state = randomState, shuffle = shuffle)
        return split1, split2 

    X_split1, X_split2, y_split1, y_split2 = train_test_split(args[0], args[1], test_size = test_size, random_state = randomState, shuffle = shuffle)
    return X_split1, X_split2, y_split1, y_split2



def makeGen(X, y, folder: str = 'train_images/', 
                  augment: bool = False, 
                  batchSize: int = 32, 
                  target_size: tuple = (260, 260), 
                  nb_canaux: int = 1) -> ImageDataGenerator:
    
    """Generation des images 

     Paramètre
     ----------
     X           : set a traiter
     y           : variables d'interets
     folder      : repertoire source
     augment     : application d'une augmentation, autre que la normalisation
     batchSize   : taille des batchs de sortie
     target_size : taille cible des images
     nb_canaux   : nombre de canaux (1: nuances de gris, 3: rgb)

     Retour
     ----------
     ImageDataGenerator : generateur
    """

    if augment:
        datagen = ImageDataGenerator(rescale=1./255, 
                                 horizontal_flip=True,
                                 vertical_flip=True,
                                 fill_mode='constant',
                                 width_shift_range=0.05,
                                 height_shift_range=0.05,
                                 zoom_range=.05)
    else:
        datagen = ImageDataGenerator(rescale=1./255)

    # si X.shape[1] <> 1, alors les images ont été chargées en mémoire
    if X.shape[1]!=1:
        generator = datagen.flow(X.reshape((-1,target_size[0],target_size[1],nb_canaux)), y,  batch_size = batchSize)

    else:
        yTemp = y.copy(deep = True)
        yTemp['imageName'] = y.index
        generator = datagen.flow_from_dataframe(yTemp, 
                                                directory = folder,
                                                target_size=target_size,
                                                color_mode = ('grayscale' if nb_canaux==1 else 'rgb'), 
                                                x_col = 'imageName',
                                                class_mode = 'raw', 
                                                y_col = y.columns,
                                                batch_size = batchSize)
    return generator





