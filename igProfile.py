'''
    Developers: Yael Abelardo Martínez, Oscar Herrera & Hugo Armando Zepeda Ruiz
    Created: 03,2020
    Purpose: Automation of interaction in Instagram from Mexican Sombrero & -less, Testing
    Copyright
'''
import os
import json
#Library to control the timings of execution
from time import sleep
from datetime import datetime
from igJSON import jsonConstructor
#Principal library for web scrapping
from selenium import webdriver
from selenium.webdriver.common import keys
from selenium.webdriver.remote.command import Command
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
#---------------------LOGGER--------------------------------#
import logging
import logging.config
logging.config.fileConfig('logging.conf')
logger = logging.getLogger('igProfile')

from igAntiban import igAntiban

class igProfile():
    def __init__(self,obj):
        """
        Will open the profile and click on the first picture

        """
        #TODO Revisar esta nueva instancia y ver como se manejara el uso entre instancia de modulos
        #obj.antiBan = igAntiban(self)
        #Entra al perfil, analiza el numero de post que tiene y abre la primera foto
        self.web_driver = obj.driver
        #self.timeOfRun = obj.timeOfRun

        # Click on profile
        obj.driver.find_element(By.XPATH, "//*[local-name()='nav' and contains(@class, 'NXc7H')]//span[img]").click()
        obj.driver.find_element(By.XPATH, "//*[local-name()='div' and contains(@class, 'fDxYl')]").click()
        WebDriverWait(obj.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME,'g47SY' )))
        logger.info("Entramos al perfil")
        self.post = obj.driver.find_element_by_class_name('g47SY').text
        self.num = int(self.post)
        print(self.num)
        #Click last image
        obj.driver.find_element(By.XPATH, "(//div[@class=\"eLAPa\"])[{}]".format(self.num)).click()
        # TODO Instanciar con igJSON
        """ 
        #Inicia funcion
        self.hashtagInfo = {}
        self.hashtime ={}
        self.likesNames = {}

        profileCount = self.compareLikesProfiles(self.likesNames)

        self.writeInfo("likesProfiles","w",profileCount) """
  
    def iterarPerfil (self, obj):
        """
            Will do the iteration through profile photos and save likes, hashtags and date.

        """
        # self.hashtime.update({t:{}})

        for i in range(self.num-1):
            pathBoton = "//a[@class=\"ITLxV  coreSpriteLeftPaginationArrow \"]"
            sleep(1)
            obj.driver.find_element(By.XPATH, pathBoton).click()
            #TODO AJustar esto con instancia de igJSON
            """ 
            ##Check if it is a video##
            sleep(2)
            try:
                self.web_driver.find_element_by_xpath("//div[@class='PyenC']")
                video = True
            except:
                video = False
            if(video):
                print("this is a Video")
                self.obj.exceptionHandler(pathperfil)
                sleep(1)
                continue          
            
            sleep(2)
            l = self.getAttributes("//div[@class = 'Nm9Fw']/button/span", "text")
            f = self.getAttributes("/html/body/div[4]/div[2]/div/article/div[2]/div[2]/a/time","datetime")
            h = self.getListAttributes("//a[@class=' xil3i']")
            t = self.timeOfRun

            sleep(1)
            self.append(({"Likes": l,"Fecha": f,"Hastags": h}), i, self.hashtagInfo)
            self.append(self.hashtagInfo,t,self.hashtime)
            self.writeInfo("PerfilInfo","w",self.hashtime)
                
            self.append(profiles, i, self.likesNames)

            #self.writeInfo("Likes","w",self.likesNames)
            
            sleep(2)
            
            # self.getDict(t,self.hashtagInfo)
            self.exceptionHandler(pathperfil) """

        sleep(1)
        WebDriverWait(obj.driver,10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[4]/div[3]/button"))).click()
         

    def compareLikesProfiles (self, dictionary, key= "num"):
        """
            Method that compares the name of diferent lists

            Variable:
            -> dict = dictionary where lists are stored
            ->key = under which elements exist
            return 
            ->list = single list of not repeating elements
        """
        elList= []
        newDict = {}
        for i in range(len(dictionary.keys())):
            nextKey = list(dictionary.keys())[i]
            elList += self.getDict(nextKey, dictionary) #TODO Revisar ajuste con funcion de igJSON, usar instancia

        profiles = list(set(elList))
        for i in profiles:
            self.append(elList.count(i), i, newDict)#TODO Revisar ajuste con instancia de igJSON
        
        return newDict