'''
    Developers: Yael Abelardo Martínez, Oscar Herrera & Hugo Armando Zepeda Ruiz
    Created: 03,2020
    Purpose: Automation of interaction in Instagram from Mexican Sombrero & -less, Testing
    Copyright
'''
from driveFile import driveFile

import os
import json
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


#---------------------LOGGER--------------------------------#
import logging
import logging.config

logging.config.fileConfig('logging.conf')

logger = logging.getLogger('igStart')

#path to chrome driver##
path_driver = os.path.dirname(os.path.realpath(__file__))
print (path_driver)

resourceFolder = os.path.join(os.getcwd(), "resources")
with open (os.path.join(resourceFolder, "xpaths.json"), "r") as f:
    xpaths = json.load(f)

driverFiles = []
class igStart():
    """
        Class that starts Chrome Instance and opens IG
    """
    def __init__(self):
       pass
    
    def openChrome(self):
        """
            Will open webdrive instance and crhome driver
        """
         #Open chrome
        if(platform.system() == 'Windows'):
            self.web_driver = webdriver.Chrome(path_driver + "\chromedriver\chromedriver.exe" )
        elif(platform.system()== 'Linux'):
            self.web_driver = webdriver.Chrome(path_driver + "/chromedriver/chromedriver_daniel")
        else:
            self.web_driver = webdriver.Chrome(path_driver + "/chromedriver/chromedriver")
        self.web_driver.get("https://instagram.com")
        sleep(2)
        return 0

    def openAccount(self):
        """
            start Chrome & IG
        """
        
        if self.runDrive:
            self.fileNames = [self.username + ".json", "likesProfiles.json"]
            exitCode = self.driveObj.downloadFile(self.fileNames)
            if (exitCode == 0): exit()

        #Input account and pw
        self.web_driver.find_element_by_name("username").send_keys(self.username)
        sleep(1)
        self.web_driver.find_element_by_name("password").send_keys(self.pw)
        sleep (1)
        ##Click iniciar sesion 
        self.exceptionHandler(xpaths["log in"], trys= 3)
        sleep(3)
        #click accept
        try:
            self.exceptionHandler(xpaths["button no"])
            sleep(2)
        except:
            pass
        self.exceptionHandler(xpaths["button no"],3)
        sleep(3)
        self.timeOfRun = datetime.utcnow().strftime('%m/%d/%Y %H:%M:%S %Z') 
        logger.info("Access Granted")
        ##We are in
        
    def exceptionHandler (self, xpath, trys= None):
        """
            Method will try to click Xpath, if not find will wait untill it is found (Solves Bad internet Issue)

            Variables: 
                xpath: html path to search for
        """
        while (True):
            try:
                if(trys == 0 and not None): 
                    errorCode = 1
                    break 
                ##Check if the Path passed is a webdriver object or a string Xpath object
                if type(xpath) == str:
                    self.web_driver.find_element_by_xpath(xpath).click()
                else:
                    xpath.click()
                errorCode = 0
                break
            except Exception as ex:
                print("Exception: ")
                print(ex)
                if (trys): trys -= 1
                sleep(2)
                continue 
        return errorCode       