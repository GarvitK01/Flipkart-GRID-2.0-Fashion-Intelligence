from bs4 import BeautifulSoup
import requests
import socket
import os
import urllib.request, urllib.parse, urllib.error
import json
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import nltk
from wordcloud import WordCloud


#Path of directory to store Images
IMG_PATH = "Pics - Copy/"
CONFIG_PATH = "Config/" 

def download(images, site, dest):

    """
    Download Image from URL
    img: img tag from list
    site: Configuration of Site stucture (HTML Tags)
    dest: Location to download image
    """
    print("In download function: ", site["name"] + "\n")
    for i, img in enumerate(images):
        src = img.get_attribute("src")
        src = site["add"] + src
        name = img.get_attribute("alt")
        name = name.replace("/", " ")
        name = name.replace("|", " ")
        name = name.replace("\t", "")
        
        if "png" in src:
            continue 
        else:
            try:
                urllib.request.urlretrieve(src, dest + name + ".jpg")
            except:
                page = requests.get(src)
                with open(name + ".jpg", 'wb') as f:
                    f.write(page.content)



def return_info(driver, site):

    """
    Return Image Web Elements
    driver: WebDriver
    """
    
    images = driver.find_elements_by_xpath(site["img"])
    print("Retreiving Image Selectors")

    return images

    


def collect_data():
    """
    To scrape data from multiple E Commerce Platforms
    """
    PATH = "Drivers/"
    option = Options()
    option.headless = True
    driver = webdriver.Firefox(PATH, options=option)
    
    for i in range(2):
        for file in os.listdir(CONFIG_PATH):
            path = CONFIG_PATH + file
            with open(path) as f:
                data = json.load(f)
            
            if "women" in file:
                dest = IMG_PATH + "Women/"
            else:
                dest = IMG_PATH + "Men/"

            print("File: " + file)
            for i in range(len(data["websites"])):
                site = data["websites"][i]
                print("Site Name: " + site["name"])

                #try: #Try block 
                for url in site["url"]: 
                    try:   
                        driver.get(url)
                        print("Inside Try Block: " + site["name"])
                        images = return_info(driver, site)
                        print(len(images), site["name"], "\n")
                        download(images, site, dest)
                    except:
                        continue
                # except:
                #     continue

def create_wordcloud(group):
    """
    Create Worcloud from Image Names
    path: Img Directory
    """
    
    text = ""
    path = IMG_PATH + group
    for file in os.listdir(path):
        name = file.replace(".jpg", "")
        
        tokens = nltk.word_tokenize(name)
        for token in tokens:
            text += " " + token.lower()
                
        stopwords = ['T-Shirt','-',  'Men',  "'s",  'KOOVS', 'Polo',  'White',  'Shirt',  'T-shirt',  'Print', 
                    'Cotton', 'in'
                    'Tee',  'KOOVS', 'Men', 'women', 'tee', 'shirt']
        for word in stopwords:
            word = word.lower()
        
    wordcloud = WordCloud(width = 480, height=480, stopwords=stopwords).generate(text)

    wordcloud.to_file(f"Wordcloud-{group}.jpg")

        

