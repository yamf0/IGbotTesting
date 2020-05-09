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
path_driver = os.path.dirname(os.path.realpath(__file__))

#Find PATH to current Directory (to find the driver)
print (path_driver)


class igProfile(jsonConstructor):
    def __init__(self,obj):
        """
        Will open the profile and click on the first picture

        """
        #Entra al perfil, analiza el numero de post que tiene y abre la primera foto
        self.web_driver = obj.web_driver
        self.timeOfRun = obj.timeOfRun

        self.web_driver.find_element_by_xpath("/html/body/div[1]/section/nav/div[2]/div/div/div[3]/div/div[5]/a/img").click()
        sleep(2)
        self.post = self.web_driver.find_element_by_class_name('g47SY').text
        self.num = int(self.post)
        self.maxNumPhotos = self.num
        sleep (2)
        self.web_driver.find_element_by_xpath("/html/body/div[1]/section/main/div/div[2]/article/div/div/div[1]/div[1]/a/div").click()
        sleep(2)
        #Inicia funcion
        self.hashtagInfo = {}
        self.iterarPerfil()
        #Cierra la ultima foto
        self.web_driver.find_element_by_xpath("/html/body/div[4]/div[3]/button").click()
   




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
        self.append(({"Likes": l,"Fecha": f,"Hastags": h,}), self.maxNumPhotos-self.num, self.hashtagInfo)
        self.writeInfo("PerfilInfo","w",self.hashtagInfo)
        # self.getDict(t,self.hashtagInfo)
        self.exceptionHandler(pathperfil)
        sleep(2)

        

        if (self.num == 1): return
        self.iterarPerfil()


