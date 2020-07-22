'''
    Developers: Yael Abelardo Martínez, Oscar Herrera & Hugo Armando Zepeda Ruiz
    Created: 03,2020
    Purpose: Automation of interaction in Instagram from Mexican Sombrero & -less, Testing
    Copyright
'''
#from driveFile import driveFile

import os
import platform
import numpy as np
#Library to control the timings of execution
from time import sleep
from datetime import datetime
#Principal library for web scrapping
from selenium import webdriver
from selenium.webdriver.common import keys
from selenium.webdriver.remote.command import Command
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
#Libraries used to avoid being banned
#from igAntiban import igAntiban
from igInteraction import igInteraction
from igJSON import jsonConstructor
#Library to print personalize message. Allows more control in message control 


#---------------------LOGGER--------------------------------#
import logging
import logging.config

logging.config.fileConfig('logging.conf')

logger = logging.getLogger('igStart')

#path to chrome driver##
path_driver = os.path.dirname(os.path.realpath(__file__))
print (path_driver)

driverFiles = []
class igStart():
    """
        Class that starts Chrome Instance and opens IG
    """
    def __init__(self, username, password, args):
        super().__init__()

        #Open chrome
        if(platform.system() == 'Windows'):
            self.driver = webdriver.Chrome("./chromedriver/chromedriver.exe" )
        elif(platform.system()== 'Linux'):
            self.driver = webdriver.Chrome()
        else:
            self.driver = webdriver.Chrome("./chromedriver/chromedriver")
        logger.warning("This code was executed from {}".format(platform.system()))

        #Access information
        self.driver.maximize_window()
        self.driver.get("https://instagram.com")
        self.username = WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.NAME, 'username'))).send_keys(username)
        self.password = WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.NAME, 'password'))).send_keys(password + Keys.ENTER)
        logger.info("Access Granted")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//img[contains(@alt, 'Instagram')]")))
        # Nos podemos saltar las acciones primarias e irnos directo al perfil con el nuevo xpath 
        """ .click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[4]//button[2][@tabindex=\"0\"]"))).click() """
        
        #TODO revisar la creacion de objetos del segundo TODO del bloque tanto para json como antiBan y primer TODO
        """ 
        #TODO Checar instancia de creacion de archivos google drive 
        if self.runDrive:
            self.fileNames = [self.username + ".json", "likesProfiles.json"]
            exitCode = self.driveObj.downloadFile(self.fileNames)
            if (exitCode == 0): exit() 

        self.fileNameRoot = username 
        self.runDrive = args.drive

        if self.runDrive == True:
            self.driveObj = driveFile(self)

        #TODO CREAR TODOS LOS OBJETOS DE LAS FUNCIONES QUE NECESITEMOS AQUI
        self.antiBan = igAntiban(self)
        self.jsonobj = jsonConstructor(self)
        ##JSON for current run##
        self.hashtagData = {}
        ##Permanent JSON for Data Science##
        ##return Dict for username running##
        if (os.path.isfile(self.fileNameRoot + ".json")):
            self.permaData = self.jsonobj.loadInfo(self.fileNameRoot + ".json")
        else:
            self.permaData = {}
        self.photoData = {}

        #TODO meter un argumento en ARGPARSE para saber si vamos a correr lo de meterse a una cuenta de una foto con muchos likes
        ## esto nos quita tiempo si lo que se quiere es solo probar // parte del codigo de abajo se tendria que mover a un if##
        ##List of current run Likes of photos##
        self.likes = np.random.randint(280, size=300) """  
        
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
                    self.driver.find_element_by_xpath(xpath).click()
                else:
                    xpath.click()
                errorCode = 0
                break
            except Exception as ex:
                print("Exception: ")
                print(ex)
                if (trys): trys -= 1
                sleep(3)
                continue 
        return errorCode       

    def getCurrentStatus (self):
        """
            Get the current status or current window
        """

        #Initial Window /html/body/div[1]/section/main/section
        #Hashtag Window /html/body/div[1]/section/main/article
        #Hashtag Photo /html/body/div[4] class="_2dDPU CkGkG" Se agrega otro div
        #Profile window /html/body/div[1]/section/main/div  Este no parte a un article seguido, sino hasta despues
            ## dEBAJO DE ESE DIV ESTA header - div - div - div 
        #profile photo /html/body/div[4]  class="_2dDPU CkGkG"
        #Histories /html/body/div[1]/section/div/div class="yS4wN "

        pass