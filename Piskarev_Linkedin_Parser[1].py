# -*- coding: utf-8 -*-
"""
Created on Fri Nov 27 19:53:31 2020

* Author: Victoria Piskarev
* Descrption: BIA-660 WS Extra Credit: Script for parsing Job Data from LinkedIn HTML profiles
* I pledge my honor that I have abided by the Stevens Honors Code
"""

#second script to parse the html of all 2000 profiles and create a single csv file that includes
#1 line per person (2000 lines total). each line should include the names of the
#companies that the person has worked for during their entire career 
#(separated by commas)

import csv
import os 
import re
import sys
from bs4 import BeautifulSoup
import codecs

#create csv to hold output
csv_output = "LinkedIn_CompanyNames_FINAL"


#function to clean name and company name of any spaces and status
def cleanData(text):
    text = text.replace("\\n", "").replace(",","").replace(".", "").replace("Full-time", "").replace("Part-time", "").replace("\r\n", "").replace("Internship", "").replace("\n", "").replace("Self-employed", "").strip()
    return text
            
#function to parse all files in the directory
#This function takes in no parameter, just change the base_directory to where the HTML files are stored
def parse():
    #open and prepare to write to csv output
    linkedin_output = open(csv_output + ".csv", 'w', encoding = 'UTF-8')
    linkedin_writer = csv.writer(linkedin_output, delimiter = ',', lineterminator = '\n')
    
    #change directory to HTML folders
    base_directory = 'C:/Users/Victoria/Documents/Stevens/BIA660/LinkedIN_HTMLs_FINAL'
    os.chdir(base_directory)
    files = os.listdir(os.getcwd())
    #for loop that goes into every html file and parses with beautiful soup
    #for count in len(base_directory):
    for file in files:
        #only run HTML files
        if file.endswith(".html"):
            #open each file
            f = codecs.open( base_directory + "/" + file, 'r', encoding="UTF-8")
            src= f.read()
            soup = BeautifulSoup(src, 'lxml')
            #Find class where the Name of the LinkedIn profile is located
            ul_test = soup.select(".ph5")
            #only parse where LinkedIn profile has a name
            if(len(ul_test)) > 0:
                ul_test_lis = ul_test[0].select("ul")
                ul_test_name = cleanData(ul_test_lis[1].select("li")[0].text)
                #find classes where info for experience is  
                ul_thing = soup.select(".pv-profile-section__section-info--has-more")
                ul_thing_test = soup.select(".pv-profile-section__section-info--has-no-more")
               
                #parse if experience is in the "no more" class
                if(len(ul_thing_test)) > 0:
                    companies_2 = []
                    lis2 = ul_thing_test[0].select("li")
                    for li in lis2:
                        ps2 = li.select("p")
                        h3 = li.select("h3")
                        try:
                            if ps2[0].text == "Company Name":
                                companies_2.append(cleanData(ps2[1].text)+ ', ')
                        except:
                            splitted2 = h3[0].text.split("Company Name")
                            if len(splitted2) > 1:
                                companies_2.append(cleanData(splitted2[1]) + ', ')
                    #only writerow if there is at least one company name
                    if (len(companies_2)) > 0:
                        print("".join(map(str, companies_2)))
                        linkedin_writer.writerow([ul_test_name, "".join(map(str, companies_2))])
                    
               # parse if experience is in the "has more" class
                if((len(ul_thing)) > 0):
                    lis = ul_thing[0].select("li")
                    companies = []
                    for li in lis:
                        ps = li.select("p")
                        aa = li.select("h3")
                        try:
                            if ps[0].text == "Company Name":
                                companies.append(cleanData(ps[1].text) + ', ')  
                        except:
                            splitted = aa[0].text.split("Company Name")
                            if len(splitted) > 1: 
                                companies.append(cleanData(splitted[1]) + ", ")
                     #only writerow if there is at least one company name
                    if (len(companies) > 0):
                        print("".join(map(str, companies)))
                        linkedin_writer.writerow([ul_test_name, "".join(map(str, companies))])
                # writerow if profile has no company names    
                elif((len(ul_thing)) < 1) and ((len(ul_thing_test))< 1):
                    companies2 = "N/A"
                    linkedin_writer.writerow([ul_test_name, companies2])
        else:
            continue
    linkedin_output.close()
    print("done")
    return
parse()
    
    

