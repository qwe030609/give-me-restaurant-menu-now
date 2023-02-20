#from bs4 import BeautifulSoup
#import requests
#from selenium import webdriver
#from selenium.webdriver.chrome.options import Options

# !/usr/bin/python
# -*- coding:utf-8 -*-
import random
import time
import re
import os
from datetime import datetime
from google_images_download import google_images_download

from PIL import Image
import requests
import eventlet
eventlet.monkey_patch()
from io import BytesIO
import urllib.request
#location_driver = 'C:\\ProgramData\\Anaconda3\\chromedriver' # Chrome驱动程序在电脑中的位置

class GoogleImageUrl:

    def __init__(self, InputMessage):
        self.InputMessage = InputMessage


    def GetGoogleImageUrlByKeyword(self):

        imglist = list()
        search_pic_count = 10
        search_key = self.InputMessage
#        self.base_url_part3 = '#imgrc='

        # use google image search api to get image urls
        response = google_images_download.googleimagesdownload()
        arguments = {"keywords":search_key, "limit":search_pic_count, "print_urls":False, "no_download":True, "format": "jpg"}   #creating list of arguments

        results = response.download(arguments)   #passing the arguments to the function
        print(results)   #printing absolute paths of the downloaded images

        image_url_list = results[0][search_key]


        image_url_list_clean = image_url_list.copy()
        session = requests.Session()        # for faster request 
        
        # for i in range(search_pic_count):
        
        # 隨機生成一整數，做為選取圖片url的index
        url_random_index = random.randint(0, len(image_url_list_clean) - 1)

        # 隨機選取一圖片的url
        ImgUrl = image_url_list_clean[url_random_index]

        try:
            with eventlet.timeout.Timeout(0.5):
                response = session.get(ImgUrl)
                # response = requests.get(image_url)

            with Image.open(BytesIO(response.content)) as img:
                 print('ok')
                 # break


        except requests.exceptions.ReadTimeout:
            print("READ TIMED OUT -", ImgUrl)
        except requests.exceptions.ConnectionError:
            print("CONNECT ERROR -", ImgUrl)
        except eventlet.timeout.Timeout as e:
            print("TOTAL TIMEOUT -", ImgUrl)
        except requests.exceptions.RequestException as e:
            print("OTHER REQUESTS EXCEPTION -", ImgUrl, e)

        except:
            print(ImgUrl)
            print('Image Corrupted')
            image_url_list_clean.remove(ImgUrl)
        
        # save Image URLs to log
        if os.path.exists('Image urls result.txt'):
          os.remove('Image urls result.txt')

        f = open('Image urls result.txt', 'a', encoding="utf-8")
        for image_url in image_url_list:

            # for LOG 
            now = datetime.now()
            current_time = now.strftime("%m/%d %H:%M:%S.%f")
            # print("Current Time =", current_time)
            LOG_prefix = "Test Image Url saved in " + current_time + ":\t"

            f.write(LOG_prefix + image_url + "\n")
            
        f.close()

#            imglist.append(image_url)
        return ImgUrl


if __name__ == "__main__":

    try:
        # test sample keyword for google image url query
        google_search_keyword = "naked hot"
        GoogleImageUrlQuery = GoogleImageUrl(google_search_keyword)
        ImgUrl = GoogleImageUrlQuery.GetGoogleImageUrlByKeyword()
            

        # print(f"Image Url: {ImgUrl}")
        # print("URL GET SUCCESS!")

    except KeyError:
        print("ERROR!")
