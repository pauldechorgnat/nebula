import tensorflow as tf
from tensorflow.keras import backend as K
import numpy as np


#-----------------------------------------------------------
# PROJET NEBULA
# Datascientest DS continu oct. 2020
# Librairie : model_evaluation
#             Evaluation de modèle de segmentation d'images
# Auteurs : Cathy Baynaud Samson
#           José Castro
#           Yann Bernery
#           Ludovic Changeon
#-----------------------------------------------------------

def tf_num(in1 : np.ndarray, in2 : np.ndarray):
    '''
        Fonction de support pour le calcul du coefficient de Dice
        Paramètre
        ----------
        in1, in2 : np.ndarray ou tf.Tensor, les deux ensembles à comparer

        Retour
        ----------
        tf.Tensor
    '''
    # Conversions pour éviter les incompatibilités
    a = K.cast(in1, tf.float32)
    b = K.cast(in2, tf.float32)
    # Retour de la fonction
    return K.log(1. + a * b) / K.log(2.)

def dice(in1 : np.ndarray, in2 : np.ndarray, classWeights : np.ndarray= np.ones(4)):
    '''
        Calcul du coefficient de Dice de deux ensembles
        Paramètre
        ----------
        in1, in2 : np.ndarray ou tf.Tensor de rangs 1, 2, 3 ou 4, valeurs entre 0 et 1
        classWeights : np.ndarray pondération optionnelle des 4 classes d'apprentissage
            [1., 1., 1., 1.] par défaut
            La pondération n'est utilisée que pour les tenseurs de rangs 3 et 4.
            La pndération implique : in1.shape = (...,4) et in2.shape = (...,4)
        Retour
        ----------
        m : coefficient de Dice (https://fr.wikipedia.org/wiki/Indice_de_S%C3%B8rensen-Dice)
    '''
    # Conversions pour éviter les incompatibilités
    a = K.cast(in1, tf.float32)
    b = K.cast(in2, tf.float32)
    w = K.cast(classWeights, tf.float32)
    # Calculs de la métrique de Dice pour rang de tenseurs entre 1 et 4
    if K.ndim(a) == 4:
        num = K.mean(K.sum(tf_num(a,b),(2,1)),0)
        denom = K.mean(K.sum(a,(2,1)) + K.sum(b,(2,1)),0)
        m= (2.*K.sum(num * w) + K.epsilon()) / \
        (K.sum(denom * w) + K.epsilon())
    elif K.ndim(a) == 3:
        num = K.sum(tf_num(a,b),(1,0))
        denom = K.sum(a,(1,0)) + K.sum(b,(1,0))
        m= (2.*K.sum(num * w) + K.epsilon()) / \
        (K.sum(denom * w) + K.epsilon())
    elif K.ndim(a) == 2:
        m= (2.*K.sum(tf_num(a,b),(1,0)) + K.epsilon()) / \
        (K.sum(a,(1,0)) + K.sum(b,(1,0)) + K.epsilon())
    else :
        m= (2.*K.sum(tf_num(a,b),(0)) + K.epsilon()) / \
        (K.sum(a,(0)) + K.sum(b,(0)) + K.epsilon())
    return m

class diceMetric(tf.keras.metrics.Metric):
    '''
        Classe utilisant le coefficient de Dice pour calculer la métrique d'apprentissage
        Utilisation :
            metrics = diceMetric(name = 'DiceM', classWeights = np.ones(4))
            metrics.update_state(y_true, y_pred)
            metrics.result()
        Paramètre
        ----------
        y_true : cibles
        y_pred : prédictions du modèle
        name : nom sous lequel apparaîtra la métrique
        classWeights : pondération des 4 classes de segmentation

        Retour
        ----------
        Coefficient de Dice (https://fr.wikipedia.org/wiki/Indice_de_S%C3%B8rensen-Dice)
    '''
    def __init__(self, name:str = 'diceM', classWeights : np.ndarray = np.ones(4), **kwargs):
        super().__init__(name = name , **kwargs)
        self.diceM = 0
        self.classWeights = tf.cast(classWeights,'float32')
    def update_state(self, y_true:tf.Tensor, y_pred:tf.Tensor, sample_weight=None):
        self.diceM = dice(y_true, y_pred, self.classWeights)
    def result(self):
        return self.diceM
    def reset_states(self):
        self.diceM=0.

class diceLoss(tf.keras.losses.Loss):
    '''
        Classe utilisant le coefficient de Dice pour calculer la perte d'apprentissage
        Utilisation :
            loss = diceLoss(name = 'DiceL', classWeights = np.ones(4))
            loss(y_true, y_pred)
        Paramètre
        ----------
        y_true : cibles
        y_pred : prédictions du modèle
        name : nom sous lequel apparaîtra la perte
        classWeights : pondération des 4 classes de segmentation

        Retour
        ----------
        loss = 1. - m (m : Coefficient de Dice (https://fr.wikipedia.org/wiki/Indice_de_S%C3%B8rensen-Dice))
    '''
    def __init__(self, name: str ='diceL', classWeights : np.ndarray = np.ones(4), **kwargs):
        super().__init__(name = name, **kwargs)
        self.classWeights = tf.cast(classWeights,'float32')
    def call(self, y_true : tf.Tensor, y_pred : tf.Tensor):
        perte = 1. - dice(y_true, y_pred, self.classWeights)
        return perte
