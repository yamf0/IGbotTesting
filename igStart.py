'''
    Developers: Yael Abelardo Martínez, Oscar Herrera & Hugo Armando Zepeda Ruiz
    Created: 03,2020
    Purpose: Automation of interaction in Instagram from Mexican Sombrero & -less, Testing
    Copyright
'''
from driveFile import driveFile

import os
import platform
#Library to control the timings of execution
from time import sleep
from datetime import datetime
#Principal library for web scrapping
from selenium import webdriver
from selenium.webdriver.common import keys
from selenium.webdriver.remote.command import Command
from selenium.common.exceptions import NoSuchElementException
#Libraries used to avoid being banned
#Library to print personalize message. Allows more control in message control 
import logging
from logging import StreamHandler


#path to chrome driver##
path_driver = os.path.dirname(os.path.realpath(__file__))
print (path_driver)

class igStart():
    """
        Class that starts Chrome Instance and opens IG
    """
    def __init__(self):
       pass

    def openAccount(self):
        """
            start Chrome & IG
        """
        
        #exitCode = self.driveObj.downloadFile("photoInfoHistory.json")
        #if (exitCode == 0): exit()

        #Open chrome
        if(platform.system() == 'Windows'):
            self.web_driver = webdriver.Chrome(path_driver + "\chromedriver\chromedriver.exe" )
        else:
            self.web_driver = webdriver.Chrome(path_driver + "/chromedriver/chromedriver")
        self.web_driver.get("https://instagram.com")
        sleep(2)
        #Input account and pw
        self.web_driver.find_element_by_name("username").send_keys(self.username)
        sleep(1)
        self.web_driver.find_element_by_name("password").send_keys(self.pw)
        sleep (1)
        self.web_driver.find_element_by_xpath("/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div[4]/button/div").click()
        sleep(3)
        #click accept
        self.exceptionHandler("/html/body/div[4]/div/div/div[3]/button[2]",3)
        sleep(3)
        self.timeOfRun = datetime.utcnow().strftime('%m/%d/%Y %H:%M:%S %Z') 
        ##We are in
        
    def exceptionHandler (self,xpath, trys= None):
        """
            Method will try to click Xpath, if not find will wait untill it is found (Solves Bad internet Issue)

            Variables: 
                xpath: html path to search for
        """
        while (True):
            try:
                if(trys == 0 and not None): break
                self.web_driver.find_element_by_xpath(xpath).click()
                break
            except Exception as ex:
                print("Exception: ")
                print(ex)
                if (trys): trys -= 1
                sleep(3)
                continue        