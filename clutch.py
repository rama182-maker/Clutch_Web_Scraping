# PROBLEM STATEMENT
# =================================================================================================
# Our Sourcing team needs to get a list of companies working on specific domains 
# (web development, mobile app development, react, etc.). 
# But the manual lookup for the same becomes tedious and time-consuming. 
# If they are provided with CSV/excel files of the firms with all the details, it may help them save a significant amount of time. 
# For that, we need you to write a python script that can scrape data from this website (https://clutch.co).
# =================================================================================================

# MY WORK
# ---------------------
# Considering Mobile App Development (https://clutch.co/directory/mobile-application-developers)
# Took the xpath to find out the elements through selenium 
# ==================================================================================================

# importing required libraries
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException

# to store all the elements in to a list then to csv
list_of_elem = []

# Checks all the page from page 0 to last, 
# To test a few page change 'while True:' --> 'while page < n:' (where n is the last required page)
page = 0
while True:
    try:
        service = Service('/usr/local/bin/chromedriver')
        driver = webdriver.Chrome(service=service) 
        print("\n====================== page: ", page, " ======================")
        driver.get("https://clutch.co/directory/mobile-application-developers?page="+str(page))
        print('start page')
        time.sleep(2)
    
        try:
            all_ul_from_xpath = driver.find_element("xpath",'//*[@class="directory-list"]')
        except:
            driver.quit()
            print('end of results')
            break
        all_li = all_ul_from_xpath.find_elements("xpath",'//li[starts-with(@class, "provider")]') 
        
        i = 0
        for li in all_li[:-1]:
            try:
                company = li.find_elements("xpath",'//h3/a[@data-link_text="Profile Title"]')[i].text
            except:
                company = 'NA'
            try:
                website = li.find_elements("xpath",'//ul/li/a[@class="website-link__item"]')[i].get_attribute('href')
            except:
                website = 'NA'
            try:
                location = li.find_elements("xpath",'//span[@class="locality"]')[i].text
            except:
                location = 'NA'
            contact = li.find_elements("xpath",'//li/a[@class="provider-detail-contact"]')[i].get_attribute('href')
            try:
                rating = li.find_elements("xpath",'//span[@class="rating sg-rating__number"]')[i].text
            except:
                rating = 'NA'
            try:
                review_count = li.find_elements("xpath",'//a[@data-link_text="Reviews Count"]')[i].text.lower()
            except:
                review_count = 'NA'
            try:
                hourly_rate = li.find_elements("xpath",'//div[@data-content="<i>Avg. hourly rate</i>"]/span')[i].text
            except:
                hourly_rate = 'NA'
            try:
                min_proj_size = li.find_elements("xpath",'//div[@data-content="<i>Min. project size</i>"]/span')[i].text
            except:
                min_proj_size = 'NA'
            try:
                emp_size = li.find_elements("xpath",'//div[@data-content="<i>Employees</i>"]/span')[i].text
            except:
                emp_size = 'NA'
            list_of_elem.append([company, website, location, contact, rating, review_count, hourly_rate, min_proj_size, emp_size])
            i += 1
        print('i: ', i)
        page += 1
        driver.quit()
        print('end of page') 
    except (TimeoutException, StaleElementReferenceException) as e:
        driver.quit()
        break

print(len(list_of_elem))

# converting to dataframes
df = pd.DataFrame(list_of_elem)
headerlist=['Company','Website','Location','Contact','Rating','Review Count,','Hourly Rate','Min Project Size','Employee Size']	
# converting dataframes to csv
df.to_csv('clutch_csv.csv', index=False, header=headerlist)