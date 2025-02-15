# -*- coding: utf-8 -*-
"""
Created on Sat Jan 28 12:13:52 2023

@author: Moumita
"""


##
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.common.exceptions import NoSuchElementException
#from bs4 import BeautifulSoup
import requests, codecs, time, os
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import numpy as np
import atexit
##############################################################
########################### 	Parameters
##############################################################
##############################################################

basepage 		= 'https://epos.bihar.gov.in/FPSDayWiseInterface.jsp'
remote 			= True

if remote:
	htmlpath 		= 'html'
	progressfile 	= 'progress.csv'
	headless = True
else:
	htmlpath 		= 'C:/Users/Moumita/Dropbox/PDS data/Bihar/html'
	progressfile 	= 'C:/Users/Moumita/Dropbox/PDS data/Bihar/progress.csv'
	headless = False


#We should updated the progress file after every ___ shops
updateN = 10
yr = "2022"
#Give the browser a break after every 200 (successful) iterations
restN = 200


####################################################
################## 	Major Functions
####################################################
def setup_browser(head):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--incognito')
    if headless:
        chrome_options.add_argument('--headless')
	# driver = webdriver.Safari()
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


#####


# This function is going to return a list that contains a list of districts and a list of corresponding shops
# Input: the basepage link
# Output: a list
def getShopList(URL):
    districtShoplist = []
    get_url(URL, 3)
    
	
    
    dist = Select(browser.find_element(by=By.CSS_SELECTOR, value="#dist_code"))
    dist_options = dist.options
    for d in range(1,len(dist_options)):
        dist.select_by_index(d)
        districtList = []
        districtName = []
        districtList.append(dist_options[d].get_attribute('value'))
        districtName.append(dist_options[d].get_attribute('innerText'))
        print('Getting shops for district '+dist_options[d].get_attribute('innerText'))
        time.sleep(2)
        shopList = []
        shopName = []
        fps = Select(browser.find_element(by=By.CSS_SELECTOR, value="#fps_id"))
        fps_options = fps.options
        for f in range(1,len(fps_options)):
            shopList.append(fps_options[f].get_attribute('value'))
            shopName.append(fps_options[f].get_attribute('innerText'))
    
        tmp = pd.DataFrame({'District Value' : np.repeat(districtList,len(fps_options)-1),
                       'District Name' : np.repeat(districtName,len(fps_options)-1),
                       'Shop Value' : shopList,
                       'Shop Name' : shopName
                  })
         
        districtShoplist.append(tmp)
	

    return districtShoplist
	


#####
# def checkUpdate():
#     time.sleep(3)
#     try:
#         fetchEle = browser.find_element(By.XPATH, '//*[@id="Report"]')
#         #if (fetchEle.is_displayed() == True):
#          #   return True
#         #else:
#         return True
#     except NoSuchElementException:
#         return False



#####


def checkAnyData():
    time.sleep(3)
    try:
        browser.find_element(By.XPATH, '//*[@id="Report"]')
    except NoSuchElementException:
        return False
    return True



#####
def checkFullRecord():
    try:
        browser.find_element(By.CSS_SELECTOR, ".next.paginate_button.paginate_button_disabled")
    except NoSuchElementException:
        return False
    return True
#####
def savefile(browser, path, filename):
	with codecs.open(path + '/' + filename, "w+", "utf-8-sig") as temp:
		temp.write(browser.page_source)
        
#####
@atexit.register
def goodbye():
    print("Bye bye!Session ended.")

####################################################
################## 	Lambda Functions
####################################################

pickyear = lambda: Select(browser.find_element(By.NAME, 'year')).select_by_value(yr)
pickmonth = lambda x: Select(browser.find_element(By.NAME, 'month')).select_by_value(x)
pickdistrict = lambda x: Select(browser.find_element(By.NAME, 'dist_code')).select_by_value(x)
pickshop = lambda x: Select(browser.find_element(By.NAME, 'fps_id')).select_by_value(x)
    
allrecords = lambda: Select(browser.find_element(By.NAME, 'Report_length')).select_by_visible_text('All')     
clickSubmit = lambda: WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH , '//*[@id="container"]/div[1]/table/tbody/tr[3]/td/button[1]'))).click()
                
              
##############################################################
##############################################################
########################### 	Main Body
##############################################################
##############################################################
	
	

####################################################
################## 	Prepare
####################################################
browser = setup_browser(headless)
get_url(basepage, 3) 


district_wise_shops_list= getShopList(basepage) #Takes about 20 mins
district_wise_shops=pd.concat(district_wise_shops_list)

district_wise_shops.to_csv('district_wise_shops.csv')

print(len(district_wise_shops_list))
district_wise_shops.shape

#if not os.path.exists(htmlpath):
#	os.makedirs(htmlpath)

#noULBDetails = []

#noGroupDetails = []

