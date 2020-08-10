import requests
import os
import urllib.request
import json
from utils import *
from Model import *
from Clustering.clustering import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

# Collecting and Sorting Data
collect_data()

# Training Neural Network Model
train_save_model()

#Grouping Similar Images and creating the wordclouds
make_clusters()

