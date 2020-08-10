import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import keras
from keras.preprocessing.image import ImageDataGenerator
from keras.applications import InceptionV3
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.manifold import TSNE
import os
import cv2
from utils import *

IMG_PATH_MEN = "Pics - Copy/Men/"
IMG_PATH_WOMEN = "Pics - Copy/Women/"
IMG_CLUSTER_MEN = "Clusters/Men/"
IMG_CLUSTER_WOMEN = "Clusters/Women/"

def img_mappings():
    """
    Create Image-Index Mapping
    Returns Two dictionaries(Men, Women) which maps index to one image
    """

    idx2img_men = {}
    idx2img_women = {}
    for i, img in enumerate(os.listdir(IMG_PATH_MEN)):
        idx2img_men[i] = img
    for i, img in enumerate(os.listdir(IMG_PATH_WOMEN)):
        idx2img_women[i] = img

    return idx2img_men, idx2img_women

def extract_features(extractor, mapping, path):
    """
    Extract Image Features from trained model
    extractor: Extractor Model
    mapping: Index - Image mapping 
    path: Image Directory
    """
    features = []
    for i, img in mapping.items():
        img_path = path + img

        image = plt.imread(img_path)
        image = cv2.resize(image, (224, 224))
        image = np.expand_dims(image, axis = 0)
        feature = extractor.predict(image)
        features.append(feature[0])

            
    return np.array(features)

def cluster_mapping(preds, idx2img, path):
    """
    Create a mapping between images and their respective clusters
    preds: Cluster each image is in
    idx2img: Index-Image mapping
    path: Image Directory
    
    Returns:
    A dictionary between images and theor respective clusters
    """
    
    idx2cluster = {}
    for idx, img in idx2img.items():
        pred = preds[idx]
        idx2cluster[idx] = pred
    
    return idx2cluster

def cluster_images(idx2cluster, idx2img, path, directory):
    """
    Save Clustered Images
    idx2cluster: Mapping between images and their respective clusters
    idx2img: Index - Image Mapping
    path: Image Directory
    directory: Directory to cluster Images
    """
    import shutil
    
    for i, img in idx2img.items():
        cluster = idx2cluster[i]
        img = idx2img[i]
        
        original_path = path + img
        
        cluster_path = os.path.join(directory, str(cluster))
        if os.path.exists(cluster_path):
            img_path = os.path.join(cluster_path, img)
            shutil.copyfile(original_path, img_path)
        else:
            os.mkdir(cluster_path)
            img_path = os.path.join(cluster_path, img)
            shutil.copyfile(original_path, img_path)

            
def make_clusters():

    #Loading Trained Model
    saved_model = tf.keras.models.load_model("C:/Users/Asus/Desktop/Project Folder/inception_v3.h5")
    #Creating a Model to extract 128 dimensional image features
    extractor = tf.keras.Model(inputs = saved_model.inputs, outputs = saved_model.layers[-2].output)


    idx2img_men, idx2img_women = img_mappings()

    # Feature Extraction of Images from trained Model
    features_men = extract_features(extractor, idx2img_men, IMG_PATH_MEN)
    features_women = extract_features(extractor, idx2img_women, IMG_PATH_WOMEN)
    

    # Clustering Images using T-SNE and KMeans
    men_embedded = TSNE(n_components=2).fit_transform(features_men)
    preds_men = KMeans(n_clusters=5).fit_predict(features_men)

    preds_women = KMeans(n_clusters=5).fit_predict(features_women)
    women_embedded = TSNE(n_components=2).fit_transform(features_women)

    idx2cluster_men = cluster_mapping(preds_men, idx2img_men, IMG_PATH_MEN)
    idx2cluster_women = cluster_mapping(preds_women, idx2img_women, IMG_PATH_WOMEN)

    # Make Directories for Clustees
    cluster_images(idx2cluster_men, idx2img_men, IMG_PATH_MEN, IMG_CLUSTER_MEN)
    cluster_images(idx2cluster_women, idx2img_women, IMG_PATH_WOMEN, IMG_CLUSTER_WOMEN)

    # Creating the Wordclouds
    create_wordcloud(group="Men")
    create_wordcloud(group="Women")