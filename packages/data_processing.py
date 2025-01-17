from shutil import copyfile, unpack_archive
import os
import pandas as pd

#-----------------------------------------------------------
# PROJET NEBULA
# Datascientest DS continu oct. 2020
# Librairie : DATA_PROCESSING
#             Chargement et pre-traitement des donnees
# Auteurs : Cathy Baynaud Samson
#           José Castro
#           Yann Bernery
#           Ludovic Changeon
#-----------------------------------------------------------


def copy_data_from_drive(from_path: str = '/content/drive/MyDrive',
                         filename: str = 'understanding_cloud_organization.zip',
                         to_path: str = '.') -> bool:
    """
     Copie des donnees compressees depuis le drive vers le repertoire courant  
  
     Paramètre  
     ----------  
     from_path : repertoire du fichier a copier  
     filename  : nom du fichier a copier  
     to_path   : repertoire de destination  
  
     Retour  
     ----------  
     booleen : True si l'operation a reussie, False dans le cas contraire  
    """

    try:
        source = os.path.join(from_path, filename)     #initilisation fichier source
        target = os.path.join(to_path, filename)       #initialisation fichier cible
        copyfile(source, target)                       #copie du fichier
        unpack_archive(target)                         #decompression de l'archive
        os.remove(target)                              #suppression de l'archive
    except FileNotFoundError:
        return False

    return True



def load_train(filename: str = 'train.csv')-> pd.DataFrame:
    """
     Chargement du repository d'entrainement  
  
     Paramètre  
     ----------  
     filename  : nom du fichier à charger  
  
     Retour  
     ----------  
     dataframe : donn-ées chargées  
    """

    train = pd.read_csv(filename)     #Lecture du fichier
    return train



def label_parsing(dataframe: pd.DataFrame, sep: str = '_', drop_na: bool = True)-> pd.DataFrame:
    """
     Le label de la classe est isolé du nom de l'image, générant ainsi  
     deux colonnes "image" et "label". La colonne "Image_Label" est  
     ensuite supprimée.  
  
     Paramètre  
     ----------  
     dataframe  : nom dataframe à traiter  
  
     Retour  
     ----------  
     dataframe : dataframe dont les labels ont été isolés  
    """

    try:
        parsed_df = dataframe
        parsed_df['image'] = parsed_df['Image_Label'].apply(lambda x: x.split(sep)[0])
        parsed_df['label'] = parsed_df['Image_Label'].apply(lambda x: x.split(sep)[1])
        parsed_df = parsed_df.drop(['Image_Label'], axis=1)
        if drop_na: parsed_df.dropna(inplace = True)
    except KeyError:
        return dataframe
    return parsed_df



def one_hot_encoding(dataframe: pd.DataFrame, reset_index: bool = True)-> pd.DataFrame:
    """
     Les classes de nuages subissent un codage disjonctif, puis les données  
     son agrégées par image. Les colonnees "label" et "EncodedPixels" sont  
     par ailleurs supprimées.  
  
     Paramètre  
     ----------  
     dataframe  : nom dataframe à traiter  
     reset_index : True -> les indexes sont réinitialisés  
                   False -> la colonne "image" reste en index  
  
     Retour  
     ----------  
     dataframe : dataframe modifié  
    """

    try:
        #On effectue une dichotomisation des classes de nuages
        encoded_dataframe = dataframe
        encoded_dataframe = encoded_dataframe.join(pd.get_dummies(encoded_dataframe['label']))

        #On supprime ensuite les colonnes "encoded Pixels" et "label", inutiles pour l'aggregation qui suit
        encoded_dataframe = encoded_dataframe.drop(['EncodedPixels', 'label'], axis=1)

        #Enfin on fait un sous-total pour ne conserver qu'une ligne par image
        encoded_dataframe = encoded_dataframe.groupby(['image']).sum()

        #Si l'option est actviee, les indexes sont reinitialises
        #sinon image reste en indexe
        if reset_index:
            encoded_dataframe = encoded_dataframe.reset_index(level=0)
    except KeyError:
        return dataframe
    return encoded_dataframe



def get_labels(values: [(int, float)],
               labels: [str] = ['Fish', 'Flower', 'Gravel', 'Sugar'],
               threshold: [float] = [0.5, 0.5, 0.5, 0.5])-> (str, None):
    """
     Génération d'un label complet correspondant aux valeurs supérieures  
     ou égales aux seuils indiqués  
  
     Paramètre  
     ----------  
     values  : valeurs des classes,  
               exemple [1, 0, 0, 1] s'il s'agit d'un one hot encoding  
                    ou [0.65, 0.34, 0.21, 0.87] s'il s'agit de probabilités  
     labels : textes des labels a concaténer  
     threshold : seuils a appliquer, tout est a 0.5 par défaut  
  
     Retour  
     ----------  
     str : label complet  
    """

    try:
        full_label = []
        for i in range(len(values)):
            if values[i]>=threshold[i]:
                full_label.append(labels[i])
    except (IndexError, TypeError):
        return None

    return ','.join(filter(None, full_label))
