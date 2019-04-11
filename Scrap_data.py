# -*- coding: utf-8 -*-
"""
Created on Thu Jan 17 18:48:51 2019


"""

import pandas
import numpy
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options 
import collections
'''read processed data'''
london_data=pandas.read_csv('C:\Sameer\Data Science\Aegis\Machine Learning\Project\nan_list.csv')
nan_list=pandas.read_csv('C:\\Sameer\\Data Science\\Aegis\\Machine Learning\\Project\\nan_lists.csv')

'''scrape'''
dollar_rate=70.38
chrome_options = Options()  
chrome_options.add_argument("--headless")  
new_prices_nan=pandas.DataFrame(data=None,columns=['listing_url','new_price'])
capa = DesiredCapabilities.CHROME
capa["pageLoadStrategy"] = "none"
            
index=0
'''change below condition according to what you want to scrape'''    
#subset=london_data.loc[(london_data.price<200) & (london_data.bedrooms==4),: ] 

for url in nan_list['listing_url']:          
    try:            
        driver = webdriver.Chrome('C:\Sameer\Data Science\Aegis\chromedriver_win32\chromedriver.exe',desired_capabilities=capa,chrome_options=chrome_options)
        driver.get(url)                
        wait = WebDriverWait(driver, 20)#10 seconds wait.increase if your net is slow    
        myelem=wait.until(EC.presence_of_element_located((By.CLASS_NAME, '_doc79r')))
        driver.execute_script("window.stop();")        
        source=driver.page_source
        soup=BeautifulSoup(source,'html.parser')
        spandiv=soup.find_all('span',attrs={'class':'_doc79r'}) 
        if(spandiv!=None and len(spandiv)>0):
            price=spandiv[0].text
            price=price.replace(',','').replace('₹','')
            price=int(price)
            price=numpy.ceil(price/dollar_rate)
            new_prices_nan.loc[index,:]=(url,price)
            index+=1                    
            driver.close()
        else:
            driver.close()
    except:
        print('Timeout exception:',url)
        new_prices_nan.loc[index,:]=(url,'NaN')
        index+=1
        driver.close()
    print(index)

'''write file.add ur name to the file'''
new_prices_nan.to_csv('scrapped_file3.csv',index=False)
