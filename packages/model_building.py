import keras
from keras.layers import Dense, Dropout, Flatten
from keras.layers.convolutional import Conv2D, MaxPooling2D
from keras.models import Sequential, Model
from keras import callbacks

#-----------------------------------------------------------
# PROJET NEBULA
# Datascientest DS continu oct. 2020
# Librairie : model_building
#             Création de modèle de classification
# Auteurs : Cathy Baynaud Samson
#           José Castro
#           Yann Bernery
#           Ludovic Changeon
#-----------------------------------------------------------


def builClassifdModel():
    '''
        Fonction de création de l'architecture du modèle de classification
            "NebulaClassificationPhase2"
        Paramètre
        ----------
        None

        Retour
        ----------
        tf.keras.Model
    '''
    # Model sequentiel
    model = Sequential()
    # Première couche de convolution / maxpooling
    conv11 = Conv2D(filters = 30, kernel_size = (5,5), input_shape = (tx, ty, 1),
                    activation = 'relu', padding = 'valid')
    pool1 = MaxPooling2D(pool_size = (5,5))
    # Deuxième couche de convolution / maxpooling
    conv21 = Conv2D(filters = 8, kernel_size = (5,5), activation = 'relu', padding = 'valid')
    pool2 = MaxPooling2D(pool_size = (5,5))
    # Interface avec les couches de neurones
    drop = Dropout(rate = 0.2)
    flat = Flatten()
    # Couches de neurones
    dense1 = Dense(units = 128, activation = 'relu')
    drop2 = Dropout(rate = 0.2)
    dense2 = Dense(units = 4, activation = 'sigmoid')
    # Ajout de toutes les couches dans le modèle
    listeLayers = [conv11, pool1, conv21, pool2, drop, flat, dense1, drop2, dense2]
    for layer in listeLayers :
        model.add(layer)
    return model

def cb_earlyStopping(patience=6, monitor='val_loss'):
    '''
        Création d'un callback EarlyStopping pré-paramétré
        Paramètre
        ----------
        Cf. documentation Keras

        Retour
        ----------
        tensorflow.keras.callbacks
    '''
    return callbacks.EarlyStopping(monitor=monitor, patience=patience)

def cb_modelCheckPoint(filename, weights_only = True, monitor='val_loss'):
    '''
        Création d'un callback ModelCheckpoint pré-paramétré
        Paramètre
        ----------
        Cf. documentation Keras

        Retour
        ----------
        tensorflow.keras.callbacks
    '''
    return callbacks.ModelCheckpoint(filepath = filename,
                                       monitor = monitor,
                                       save_best_only = True,
                                       save_weights_only = weights_only,
                                       mode = 'min',
                                       save_freq = 'epoch')

def cb_reduceLr(patience=3, factor=0.08, monitor='val_loss'):
    '''
        Création d'un callback ReduceLROnPlateau pré-paramétré
        Paramètre
        ----------
        Cf. documentation Keras

        Retour
        ----------
        tensorflow.keras.callbacks
    '''
    return callbacks.ReduceLROnPlateau(monitor = monitor,
                                         patience=patience,
                                         factor=factor,
                                         verbose=2,
                                         mode='min')

class NebulaClassifModel(Model):
  '''
      Création d'un modèle de classification selon architecture et poids :
        "nebula_phase2_multiClassification"
      Si l'on charge les poids, inutile de réentraîner le modèle

      Utilisation
      ----------
      model = ClassifModel(autoInit = True)
      model.compile()
      model.fit(generator,
                epochs, batch_size)
      pred = model.predict(testGen,
                          filter = True,
                          threshold = 0.5)
      Méthodes
      ----------
      __init__(autoInit, initWeights)
          autoInit : pour charger les poids pré-entraînés
          initWeights : chemin vers le fichier de poids pré-entraînés
      compile(optimizer, loss, metrics)
          optimizer : keras.optimizers.Optimizer ou str (par ex. 'adam')
          loss : keras.losses.Loss ou str (par ex. 'binary_crossentropy')
          metrics : keras.metric.Metric ou str (par ex. 'categorical_accuracy')
          learning_rate : 0.001
      predict(x, filter, threshold)
          x : générateur ou np.ndarray renvoyant :
              X : [batchSize, X-dim, Y-dim, 1]
              y : [batchsize, 4]
          filter : True pour filtrer les prédictions
          threshold : si y > threshold: 1, sinon 0
      fit(...)
          Voir documentation Keras.
          Par défaut, callbacks=[EarlyStopping(),
                     ModelCheckpoint(filename = 'ckptSave'),
                     ReduceLROnPlateau()]

      Retour
      ----------
      En fonction des méthods...
  '''
  def __init__(self, autoInit: bool = True,
               initWeights: str = 'chkpt_classif/checkpoint3'):
    super().__init__()
    self.autoInit = autoInit
    self.initWeights = initWeights
    self.model = builClassifdModel()
    if self.autoInit:
      self.model.load_weights(self.initWeights)

  def call(self, inputs, training: bool = False):
    return self.model(inputs)

  def compile(self,
              optimizer: tf.keras.optimizers.Optimizer = tf.keras.optimizers.Adam,
              loss: tf.keras.losses.Loss = 'binary_crossentropy',
              metrics: tf.keras.metrics.Metric = 'categorical_accuracy',
              learning_rate: float=0.001, *args, **kwargs):
    if type(optimizer) == str:
      self.model.compile(optimizer = optimizer,
                loss = loss,
                metrics = metrics, *args, **kwargs)
    else:
      self.model.compile(optimizer = optimizer(learning_rate=learning_rate),
                      loss = loss,
                      metrics = metrics, *args, **kwargs)
    return self.model

  def predict(self, x,
              filter: bool = False,
              threshold: float = 0.5):
    if not filter:
      return super().predict(x)
    else:
      return np.where(super().predict(x)>=threshold, 0, 1)

  def fit(self, x = None, y = None, batch_size=32,
          epochs=1, verbose=1, validation_data = None,
          steps_per_epoch =None, validation_steps =None,
          callbacks=[cb_earlyStopping(),
                     cb_modelCheckPoint(filename = 'ckptSave'),
                     cb_reduceLr()],
          class_weight = {0: 1., 1: 1., 2: 1., 3: 1.},
          *args, **kwargs):
    training = self.model.fit(x = x, y = y, batch_size = batch_size,
                epochs=epochs, verbose=verbose,
                callbacks = callbacks,
                class_weight = class_weight,
                validation_data = validation_data,
                steps_per_epoch = steps_per_epoch,
                validation_steps = validation_steps,
                *args, **kwargs)
    return training
