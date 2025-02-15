# -*- coding: utf-8 -*-
"""
Created on Sat Feb  4 21:26:28 2023

@author: Moumita
"""

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import InvalidSessionIdException
from selenium.common.exceptions import NoSuchElementException
#from bs4 import BeautifulSoup
import requests, codecs, time, os
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import numpy as np
import atexit

################## 	Major Functions
####################################################
def setup_browser():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--incognito')
    prefs = {"download.default_directory" : "C:\\Users\\Moumita\\Dropbox\\research_ideas\\migration\\onorc india\\SALE_STATE_DELHI\\nov2022\\"}
    chrome_options.add_experimental_option("prefs",prefs)
    return webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
	#return webdriver.Chrome(chrome_options=chrome_options,executable_path = chromedriver )
    print('Driver Loaded', flush=True)

def get_url(url, tries):
	keepLooping = True
	count = 0

	while keepLooping == True:
		count += 1

		try:
			browser.get(url)
			keepLooping = False
		except:
			if count >= tries:
				keepLooping = False
				print('Failure to load URL', flush=True)
				exit()

pickDelhi = lambda: browser.find_element(By.CSS_SELECTOR, '#myTable > tbody > tr:nth-child(9) > th:nth-child(1) > a').click()

pickCentral = lambda: browser.find_element(By.CSS_SELECTOR, '#myTable > tbody > tr:nth-child(1) > td:nth-child(6) > a').click()
pickEast = lambda: browser.find_element(By.CSS_SELECTOR, '#myTable > tbody > tr:nth-child(2) > td:nth-child(6) > a').click()
pickNewDelhi = lambda: browser.find_element(By.CSS_SELECTOR, '#myTable > tbody > tr:nth-child(3) > td:nth-child(6) > a').click()
pickNorth = lambda: browser.find_element(By.CSS_SELECTOR, '#myTable > tbody > tr:nth-child(4) > td:nth-child(6) > a').click()
pickNorthEast = lambda: browser.find_element(By.CSS_SELECTOR, '#myTable > tbody > tr:nth-child(5) > td:nth-child(6) > a').click()
pickNorthWest = lambda: browser.find_element(By.CSS_SELECTOR, '#myTable > tbody > tr:nth-child(6) > td:nth-child(6) > a').click()
pickSouth = lambda: browser.find_element(By.CSS_SELECTOR, '#myTable > tbody > tr:nth-child(7) > td:nth-child(6) > a').click()
pickSouthWest = lambda: browser.find_element(By.CSS_SELECTOR, '#myTable > tbody > tr:nth-child(8) > td:nth-child(6) > a').click()
pickWest = lambda: browser.find_element(By.CSS_SELECTOR, '#myTable > tbody > tr:nth-child(9) > td:nth-child(6) > a').click()

getExcel = lambda: browser.find_element(By.CSS_SELECTOR, '#myTable_wrapper > div.dt-buttons > button > span').click()
#####
url = 'https://impds.nic.in/portal/portal?month=11&year=2022'
browser = setup_browser()
get_url(url, 5)

pickDelhi() 

time.sleep(5)
pickCentral()
time.sleep(5)
getExcel()
browser.execute_script("window.history.go(-1)")
time.sleep(5)
pickEast()
time.sleep(5)
getExcel()
browser.execute_script("window.history.go(-1)")
time.sleep(5)
pickNewDelhi()
time.sleep(5)
getExcel()
browser.execute_script("window.history.go(-1)")
time.sleep(5)
pickNorth()
time.sleep(5)
getExcel()
browser.execute_script("window.history.go(-1)")
time.sleep(5)
pickNorthEast()
time.sleep(5)
getExcel()
browser.execute_script("window.history.go(-1)")
time.sleep(5)



pickNorthWest()
time.sleep(5)
getExcel()
browser.execute_script("window.history.go(-1)")
time.sleep(5)
pickSouth()
time.sleep(5)
getExcel()
browser.execute_script("window.history.go(-1)")
time.sleep(5)
pickSouthWest()
time.sleep(5)
getExcel()
browser.execute_script("window.history.go(-1)")
time.sleep(5)
pickWest()
time.sleep(5)
getExcel()

time.sleep(3)
browser.quit()