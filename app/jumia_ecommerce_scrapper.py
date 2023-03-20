
from concurrent.futures import ThreadPoolExecutor
import itertools
import requests
import json
from bs4 import BeautifulSoup 
import pandas as pd
import os
import csv
import time
import sys
import urllib.request
from datetime import date, datetime
from htmldate import find_date
from dotenv import load_dotenv
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from json import JSONDecoder
from fake_useragent import UserAgent
from selenium.webdriver.chrome.service import Service
import logging as Log
import logging.handlers
import os
import pandas as pd 
import numpy as np
import validators
 
handler = Log.handlers.WatchedFileHandler(
    os.environ.get("LOGFILE", "../logs/scrap.log"))
formatter = Log.Formatter(Log.BASIC_FORMAT)
handler.setFormatter(formatter)
root = Log.getLogger()
  #The application will now log all messages with level INFO or above to file
root.setLevel(os.environ.get("LOGLEVEL", "INFO"))
root.addHandler(handler)


def driver_setup():
    try:
        Log.info(datetime.now())
        load_dotenv() 
        EMAIL = os.environ.get('EMAIL')
        contact_info = EMAIL
        user_agent = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:94.0) Gecko/20100101 Firefox/94.0"+ contact_info
        
        #remove certain stuff for performance
        """ chrome_options.experimental_options["prefs"] = { 
            "profile.managed_default_content_settings.images": 2, 
            "profile.managed_default_content_settings.stylesheets": 2, 
            "profile.managed_default_content_settings.javascript": 2, 
            "profile.managed_default_content_settings.cookies": 2, 
            "profile.managed_default_content_settings.geolocation": 2, 
            "profile.default_content_setting_values.notifications": 2, 
        } """

        chrome_options = Options()
        chrome_options.add_argument(f'user-agent={user_agent}')
        #chrome_options.add_argument("--headless")
        chrome_options.add_experimental_option("detach", True)
        s=Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=s, options=chrome_options)
    except Exception as e:
        Log.error("logOpeningBrowserFail:",e)
        Log.info(datetime.now())
    else:
        Log.info("logOpenBrowserSuccess")
        return driver

driver = driver_setup()


def scroll_down_page(speed=20):
    print("scroll down page")
    current_scroll_position, new_height= 0, 1
    while current_scroll_position <= new_height:
        current_scroll_position += speed
        driver.execute_script("window.scrollTo(0, {});".format(current_scroll_position))
        new_height = driver.execute_script("return document.body.scrollHeight")

def save_product(products, count, file):
    data = []
    for product in products:
        details = product.find_element(By.TAG_NAME, "a")
        if details:
            url = details.get_attribute('href')
            #image_div = a.find_element(By.CSS_SELECTOR, "div.img-c")
            #image = image_div.find_element(By.TAG_NAME, "img").get_attribute('src')
            #image = details.find_element(By.XPATH,"//img[contains(@class,'img')]").get_attribute('src')
            image = details.find_element(By.CSS_SELECTOR,"img").get_attribute("src")
            name = details.find_element(By.CSS_SELECTOR,"h3").get_attribute("innerText")
            new_price = details.find_element(By.CSS_SELECTOR,"div.prc").get_attribute("innerText")
            ##old_price = details.find_element(By.CSS_SELECTOR,"div.old").get_attribute("innerText")
            
            data_list = np.array([name, image,url, new_price])
            data.append(data_list) 
        else:
            raise Exception("Product details not found")

    save_data(np.array(data), count, file)
      

def get_url(search_query, page_number ):
    base_url = "https://www.jumia.co.ke/catalog/"
    params = {"q": search_query, "page": str(page_number)}
    fragment = "catalog-listing"

    url_parts = list(urllib.parse.urlparse(base_url))
    url_parts[4] = urllib.parse.urlencode(params)
    url_parts[5] = fragment

    url = urllib.parse.urlunparse(url_parts)

    #url = 'https://www.jumia.co.ke/catalog/?q=samsung+galaxy&page={}#catalog-listing'.format(page)
    return url
 

def make_file():
    now = datetime.now()
    d1 = now.strftime("%Y%m%d%H%M%S")
    name = f'../bulk/jumia_{d1}.csv'
    csv_file = open(name, 'w', encoding='utf-8') 
    #writer = csv.writer(csv_file)
    return name
   

def save_data(data, count, file):
    if count == 1:
        columns = ['Name', 'Image', 'Url', 'Price']
        df = pd.DataFrame(data, columns=columns)
        df.to_csv(file, mode='a', encoding='utf-8', index=False)
        count += 1
    if count == 2:
        #print("count = %d" % count)
        df = pd.DataFrame(data)
        df.to_csv(file, mode='a', encoding='utf-8', index=False, header=False)


def get_data(driver, file, search_query):
    try:
        page = 1
        count = 1
        nav = get_url(search_query,page)
        #print(driver.title)
        wait = WebDriverWait(driver, 10)
        
        while validators.url(nav):
            driver.get(nav)       
            if page == 1:
                pop_up = wait.until(EC.presence_of_element_located((By.ID, "pop")))
                pop_up.find_element(By.CLASS_NAME,"cls").click()
                
                page += 1
            
            #scroll for images loading
            scroll_down_page()
            
            ##content_section = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "-paxs")))
            section = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"section.card.-fh")))
            #header = section.find_element(By.TAG_NAME,"header")
            #header = section.find_element(By.CSS_SELECTOR,"p.-gy5.-phs").text
            #products_total = int("".join(filter(str.isdigit, header)))
                

            #catalogue = section.find_element(By.CSS_SELECTOR,"div.-paxs.row._no-g._4cl-3cm-shs")
            #articles  = catalogue.find_elements(By.TAG_NAME, "article")
            articles = section.find_elements(By.XPATH, "//div[contains(@class,'-paxs row _no-g _4cl-3cm-shs')]//article[contains(@class,'prd _fb col c-prd')]")
            print(len(articles))
            save_product(articles, count, file)
            
            if count == 1:
                count = 2
            nav = section.find_element(By.XPATH, "//div[contains(@class,'pg-w -ptm -pbxl')]//a[contains(@aria-label,'Next Page')]").get_attribute('href')
            


        """ save_product(articles)
        page = 2
        while products_total > 0:
            driver.get(get_url(page))
            scroll_down_page()
                    
            section = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"section.card.-fh")))
            catalogue = section.find_element(By.CSS_SELECTOR,"div.-paxs.row._no-g._4cl-3cm-shs")
            articles  = catalogue.find_elements(By.TAG_NAME, "article")
            save_product(articles)
            products_total -= len(articles)
            page += 1
            print(page)
            """

    except:
        print('non')
        pass

file = make_file()
search_query = "Samsung Galaxy"
get_data(driver,file, search_query)