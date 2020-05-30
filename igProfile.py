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
        self.antiBan = igAntiban(self)
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
        self.hashtime ={}
        self.likesNames = {}
        self.iterarPerfil()
        #Cierra la ultima foto
        self.web_driver.find_element_by_xpath("/html/body/div[4]/div[3]/button").click()
        profileCount = self.compareLikesProfiles(self.likesNames)

        self.writeInfo("likesProfiles","w",profileCount)
  




    def iterarPerfil (self):

        """
            Will do the iteration through perfil photos and save likes, hashtags and date.

        """
        # self.hashtime.update({t:{}})
        for i in range(self.num - 1 ):
            if(i == 0):
                pathperfil ="/html/body/div[4]/div[1]/div/div/a"
            else:
                pathperfil ="/html/body/div[4]/div[1]/div/div/a[2]"
            

                    ##Check if it is a video##
            sleep(2)
            try:
                self.web_driver.find_element_by_xpath("//div[@class='PyenC']")
                video = True
            except:
                video = False
            if(video):
                print("this is a Video")
                self.exceptionHandler(pathperfil)
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
            self.exceptionHandler(pathperfil)

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
            elList += self.getDict(nextKey, dictionary)

        profiles = list(set(elList))
        for i in profiles:
            self.append(elList.count(i), i, newDict)
        
        return newDict