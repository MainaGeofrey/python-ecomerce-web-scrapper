
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
import logging
import logging.handlers
import os
import pandas as pd 
import numpy as np
 
handler = logging.handlers.WatchedFileHandler(
    os.environ.get("LOGFILE", "../logs/scrap.log"))
formatter = logging.Formatter(logging.BASIC_FORMAT)
handler.setFormatter(formatter)
root = logging.getLogger()
  #The application will now log all messages with level INFO or above to file
root.setLevel(os.environ.get("LOGLEVEL", "INFO"))
root.addHandler(handler)


def driver_setup():
    try:
        logging.info(datetime.now())
        contact_info = "jeffdevops6@gmail."
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
        logging.error("logOpeningBrowserFail:",e)
        logging.info(datetime.now())
    else:
        logging.info("logOpenBrowserSuccess")
        return driver

driver = driver_setup()
driver.get('https://www.jumia.co.ke/catalog/?q=samsung+galaxy&page=6#catalog-listing')
print(driver.title)

wait = WebDriverWait(driver, 10)

try:
    pop_up = wait.until(EC.presence_of_element_located((By.ID, "pop")))
    exit_button = pop_up.find_element(By.CLASS_NAME,"cls").click()
    
    ##content_section = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "-paxs")))
    content_div = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"section.card.-fh")))
    #header = content_div.find_element(By.TAG_NAME,"header")
    header = content_div.find_element(By.CSS_SELECTOR,"p.-gy5.-phs").text
    items_total = int("".join(filter(str.isdigit, header)))
    
    catalogue = content_div.find_element(By.CSS_SELECTOR,"div.-paxs.row._no-g._4cl-3cm-shs")
    articles  = catalogue.find_elements(By.TAG_NAME, "article")
    ##article  = catalogue.find_element(By.TAG_NAME, "article").click()
    

    for article in articles:
        a = article.find_element(By.TAG_NAME, "a")
        article_url = a.get_attribute('href')
        #article_image = a.find_element(By.CSS_SELECTOR, "div.img-c").get
       # article_info = a.find_element(By.CSS_SELECTOR, "div.info")
        #name = article_info.find_element(By.CSS_SELECTOR, "h3.name").text
        print(article_url)

  
except:
    print('non')
    pass
