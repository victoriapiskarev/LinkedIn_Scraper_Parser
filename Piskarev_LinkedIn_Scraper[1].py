# -*- coding: utf-8 -*-
"""
Created on Fri Nov 27 12:01:11 2020

* Author: Victoria Piskarev
* Descrption: BIA-660 WS Extra Credit: Script for scraping Job Data from LinkedIn.com
* I pledge my honor that I have abided by the Stevens Honors Code
"""

# Scrape 2000 LinkedIn profiles. 
#Focus on people who have had the title "Software Architect" at some point in their career

from selenium import webdriver
import time
from time import sleep
import csv
from selenium.webdriver.common.keys import Keys
#from parsel import Selector
import os 
import re
import sys
from bs4 import BeautifulSoup
import re

#Used these search filters: Software Architect, Senior Software Architect, Web Architect, IT Architect, Software Engineer in UK, Software Enginner in Asia, Software Developer
#https://www.linkedin.com/search/results/people/?keywords=%22software%20architect%22&origin=GLOBAL_SEARCH_HEADER
#https://www.linkedin.com/search/results/people/?keywords=%22web%20architect%22&origin=GLOBAL_SEARCH_HEADER
#https://www.linkedin.com/search/results/people/?keywords=%22senior%20software%20architect%22&origin=CLUSTER_EXPANSION
#https://www.linkedin.com/search/results/people/?keywords=%22web%20architect%22&origin=GLOBAL_SEARCH_HEADER
#https://www.linkedin.com/search/results/people/?keywords=%22it%20architect%22&origin=CLUSTER_EXPANSION
#https://www.linkedin.com/search/results/people/?geoUrn=%5B%22101165590%22%5D&keywords=%22software%20engineer%22&origin=GLOBAL_SEARCH_HEADER
#https://www.linkedin.com/search/results/people/?geoUrn=%5B%22102713980%22%2C%22101355337%22%2C%22102890883%22%5D&keywords=%22software%20engineer%22&origin=FACETED_SEARCH
#https://www.linkedin.com/search/results/people/?keywords=%22junior%20software%20architect%22&origin=CLUSTER_EXPANSION


#this function takes in one parameter, which is how many LinkedIn profiles you would like to scrape. I have seen the best results with 150 profiles at a time.
def getLinkedInJobs(numjobs):
    #open the browser and visit the url
    driver = webdriver.Chrome('chromedriver.exe')
    driver.get('https://www.linkedin.com')
    time.sleep(2)
        
    # locate sign in form by_xpath
    driver.find_element_by_xpath('//a[text()="Sign in"]').click()
    #Locate username form by name
    username = driver.find_element_by_name('session_key')
    # send_keys() to simulate key strokes
    #add your username and password for LinkedIn
    username.send_keys('YOUR USERNAME')
    # locate password form by__name
    password = driver.find_element_by_name('session_password')
    # send_keys() to simulate key strokes
    password.send_keys('YOUR PASSWORD')

    # locate submit button by_xpath
    log_in_button = driver.find_element_by_xpath('//button[text()="Sign in"]')
    
    # .click() to mimic button click
    log_in_button.click()
    time.sleep(10)

    #set initial parameters for number of profiles, page to start scraping, and list of URLs
    num_profiles = 0
    current_page = 1
    urls_scraped = []
    #loop to scrape URLs and go to next page while amount is less than input. Use "Software Architect" to search for people who have had that job title.
    while num_profiles <= numjobs:
        if (current_page == 1):
            driver.get('https://www.linkedin.com/search/results/people/?keywords=%22software%20architect%22&origin=GLOBAL_SEARCH_HEADER')
            time.sleep(10)
        else:
            driver.get('https://www.linkedin.com/search/results/people/?keywords=%22software%20architect%22&origin=GLOBAL_SEARCH_HEADER&page='+str(current_page+1))
            time.sleep(10)

        #use BeautifulSoup to find URLs for each entry
        src = driver.page_source
        soup = BeautifulSoup(src, 'lxml')
        ul_thing = soup.select(".reusable-search__entity-results-list")
        time.sleep(8)
        lis = ul_thing[0].select("li")
        time.sleep(4)
        #create list for all URLs
        extracted_urls = []
        time.sleep(3)
        print("about to scrape these:")
        print(extracted_urls)
        #scrape each link and append to URL list
        for li in lis:
            links = li.select("a")
            time.sleep(5)
            for link in links:
                extracted_urls.append(link.attrs['href'])
                time.sleep(15)
        for i, link in enumerate(extracted_urls):
            time.sleep(5)
        #only write if the link has not already been scraped  
            if not link in urls_scraped:
                driver.get(link)
                prof_src = driver.page_source
                time.sleep(5)
                f = open("page"+str(current_page)+"person"+str(i)+"_software_architect"+".html", "w", encoding = 'UTF-8')
                time.sleep(10)
                f.write(prof_src)
                time.sleep(10)
                f.close()
                urls_scraped.append(link)
                print("just scraped "+link)
                time.sleep(15)
                num_profiles += 1

        current_page = current_page+1

    print("done")
getLinkedInJobs(150)