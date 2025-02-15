# -*- coding: utf-8 -*-
"""
Created on Wed Jan 25 11:42:16 2023

@author: Moumita
"""

##
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
##############################################################
########################### 	Parameters
##############################################################
##############################################################

basepage 		= 'http://epos.assam.gov.in/FPS_Trans_Abstract.jsp'
remote 			= True

if remote:
	htmlpath 		= 'html'
	progressfile 	= 'progress.csv'
	headless = True
else:
	htmlpath 		= 'C:/Users/Moumita/Dropbox/PDS data/Assam/html'
	progressfile 	= 'C:/Users/Moumita/Dropbox/PDS data/Assam/progress.csv'
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
# browser = setup_browser(headless)
# get_url(basepage, 3) 


# district_wise_shops_list= getShopList(basepage) #Takes about 20 mins
# district_wise_shops=pd.concat(district_wise_shops_list)

# district_wise_shops.to_csv('district_wise_shops.csv')

# len(district_wise_shops_list)
# district_wise_shops.shape

#if not os.path.exists(htmlpath):
#	os.makedirs(htmlpath)

#noULBDetails = []

#noGroupDetails = []


####################################################
################## 	Navigate and set agenda
####################################################


browser = setup_browser(headless)
get_url(basepage, 3)

#Get source
if os.path.exists(progressfile):
	print('Progress record found. Starting where we left off...', flush=True)
	agenda = pd.read_csv(progressfile,dtype={'District Value':'str','District Name':'str','Shop Name':'str','Shop Value':'str','month':'str'}) 
   
else :
    print('No progress record found. Starting from the beginning...', flush=True)
    ShopsList = getShopList(basepage)
    agenda=pd.concat(ShopsList)
    no_of_shops = agenda.shape[0]
    agenda = pd.DataFrame(np.repeat(agenda.values, 12, axis=0), columns=agenda.columns)
    agenda['month'] = np.tile(range(1,13),no_of_shops).astype(str)
    agenda['done'] = 0
    agenda['anydata'] = 0

   

# Keep year to be 2022 for now
pickyear()



#For counting how many shops we've processed (we'll update the progress file after each updateN)
progcount = 0
#
message='None'

#count = 1 # This number is just for distinguishing the file name
old_complete = len(agenda[agenda['done']==1])
print('So far, '+ str(old_complete) +' shop-months have been fetched') #This counts the number of shop-months already completed
# This is a loop choosing each (previously unscraped) shop and month

for row in agenda[agenda['done']==0].iterrows():

    
    dist 	= row[1]['District Value']
    fps 	= row[1]['Shop Value']
    mon 	= row[1]['month']
    #print('Getting transactions from district '+dist+' and shop '+fps+' for month '+mon)
    
    
    try:
		# get shop wise details
        pickdistrict(dist)
        time.sleep(2)
        pickshop(fps)
        pickmonth(mon)
        
        #Wait for data to fetch
        time.sleep(2)
        datareturned = False
        clickSubmit()
        time.sleep(1)
        #for j in range(10):
            #print(j)
         #   
        if(checkAnyData()==True):
            datareturned = True
                #break
                
        time.sleep(3)
        dataall = False
        if datareturned:
            #for j in range(60):
             allrecords()
             time.sleep(2)
             if(checkFullRecord()==True):
                 dataall = True
                 #   break
            
      
        if dataall:
            # Saving source code for later parsing
            #if (browser.page_source != ''):
            savefile(browser,htmlpath, 'Source_' + dist +'_' + fps + '_' + mon + '.html')
            #print('Saving file for ' + dist +', ' + fps + ', ' + mon)
            agenda.loc[row[0],'anydata'] = 1
            agenda.loc[row[0],'done'] = 1
        elif (checkAnyData()==False):
            agenda.loc[row[0],'done'] = 1    
        else:
            print('Timed out waiting for data', flush=True)
        #count += 1
    except InvalidSessionIdException:
        browser.quit()
        break
    except Exception as ex:
        print('Exception on ' + dist +'_' + fps + '_' + mon, flush=True)
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message, flush=True)
    

    
       
    progcount += 1
    if progcount % updateN == 0:
        agenda.to_csv(progressfile,index=False)
        print('A total of %d out of %d shop-months have been attempted' % (  len(agenda[agenda['done']==1]) , len(agenda) ) , flush=True )
        time.sleep(2)
    #new_complete =  len(agenda[agenda['done']==1]) - old_complete
    if progcount % restN == 0:
        time.sleep(5)
    
browser.quit()   

#agenda.to_csv(progressfile,index=False)	
###########################################################################################								
# try:
#     if(checkAnyData()==False):
#          print('Not found')
#     else:
#         print('Found')
# except Exception as ex:
#         print('Exception on ' + dist +'_' + fps + '_' + mon, flush=True)
#         template = "An exception of type {0} occurred. Arguments:\n{1!r}"
#         message = template.format(type(ex).__name__, ex.args)
#         print(message, flush=True)
#         template2 = "An exception of type {0} occurred."
#         message2 = template2.format(type(ex).__name__)
#         print(message2, flush=True)
        
     