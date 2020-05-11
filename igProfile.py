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

from igAntiban import igAntiban

class igProfile(jsonConstructor):
    def __init__(self,obj):
        """
        Will open the profile and click on the first picture

        """
        self.antiBan = igAntiban()
        #Entra al perfil, analiza el numero de post que tiene y abre la primera foto
        self.web_driver = obj.web_driver
        self.timeOfRun = obj.timeOfRun

        ##CLick go to profile
        self.web_driver.find_element_by_xpath("//*[local-name()='nav' and contains(@class, 'NXc7H')]//a[img]").click()
        sleep(2)
        self.post = self.web_driver.find_element_by_class_name('g47SY').text
        self.num = int(self.post)
        self.maxNumPhotos = self.num
        sleep (2)

        ##Click first image
        self.web_driver.find_element_by_xpath("(//div[@class= 'eLAPa'])[1]").click()
        sleep(2)
        #Inicia funcion
        self.hashtagInfo = {}
        self.likesNames = {}
        self.iterarPerfil()
        #Cierra la ultima foto
        self.web_driver.find_element_by_xpath("/html/body/div[4]/div[3]/button").click()
        print(self.likesNames)
   




    def iterarPerfil (self):

        """
            Will do the iteration through perfil photos and save likes, hashtags and date.

        """

        if((self.maxNumPhotos-self.num) == 0):
            pathperfil ="/html/body/div[4]/div[1]/div/div/a"
        else:
            pathperfil ="/html/body/div[4]/div[1]/div/div/a[2]"
        self.num -= 1
        
        l = self.getAttributes("/html/body/div[4]/div[2]/div/article/div[2]/section[2]/div/div/button", "text")
        f = self.getAttributes("/html/body/div[4]/div[2]/div/article/div[2]/div[2]/a/time","title")
        h = self.getListAttributes("//a[@class=' xil3i']")
        t = self.timeOfRun

        ##get list of people who liked the photo
        profiles = self.getLikesNames()

        self.append(profiles, self.maxNumPhotos-self.num, self.likesNames)
        self.append(({"Likes": l,"Fecha": f,"Hastags": h}), self.maxNumPhotos-self.num, self.hashtagInfo)
        self.writeInfo("PerfilInfo","w",self.hashtagInfo)
        # self.getDict(t,self.hashtagInfo)
        self.exceptionHandler(pathperfil)
        sleep(2)

        

        if (self.num == 1): return
        self.iterarPerfil()

    def getLikesNames (self):
        """
            Gets the Profiles of the Likes obtained from each photo
        """
        likesButtonPath = "//*[local-name()='div' and @class='Nm9Fw']/*[local-name()='button']"
        self.exceptionHandler(likesButtonPath)

        ##Scroll through names
        self.scrollList("//*[local-name()='div' and @class= 'pbNvD  fPMEg   ' and @role='dialog']/div[contains(@class,'Igw0E')]/div")

        
        profiles = self.getListAttributes("//*[local-name()='div' and contains(@class , 'HVWg4')]/div[2]")

        sleep(1)
        ##CLOSE LIST
        self.web_driver.find_element_by_xpath("//div[@class = 'WaOAr']/button[ @class= 'wpO6b ']").click()
        return profiles


