'''
    Developers: Yael Abelardo Martínez, Oscar Herrera & Hugo Armando Zepeda Ruiz
    Created: 03,2020
    Purpose: Automation of interaction in Instagram from Mexican Sombrero & -less, Testing
    Copyright
'''
#from igStart import igStart

import os
#Library to control the timings of execution
from time import sleep
#Principal library for web scrapping
from selenium import webdriver
from selenium.webdriver.common import keys
from selenium.webdriver.remote.command import Command
from selenium.common.exceptions import NoSuchElementException
#Libraries used to avoid being banned
import random

#TODO Quitar herencia de igStart y utilizar la instancia del bot en las funciones
class igAntiban():
    """
        Class that avoids banning
    """
    def __init__(self, obj):
        self.obj = obj
        self.web_driver = obj.driver
        


    def histories(self):
        """
            Go to main page and scroll through ig Histories
        """
        
        #Close the Photo
        self.web_driver.find_element_by_xpath("/html/body/div[4]/div[3]/button").click()
        sleep(2)
        #Click Return "Instagram Button"
        self.exceptionHandler("/html/body/div[1]/section/nav/div[2]/div/div/div[1]/a")
        #logger.info("returned to Main page")
        #self.web_driver.find_element_by_xpath("/html/body/div[1]/section/nav/div[2]/div/div/div[1]/a/div/div/img").click()
        sleep(2)
        self.exceptionHandler("//li[@class='Ckrof'][2]")
        #logger.info("start checking histories, expected return at: {} minutes".format(localtime()[4] + 5))
        sleep(300)
        self.exceptionHandler("/html/body/div[1]/section/div/div/section/div[2]/button[3]") 
        
    def randomSleep(self):
        """
            Will generate a random sleep time
            
            -> time : random int 1-5 seconds
        """
        return sleep(random.choice(range(2,6)))
    
    def enterProfile(self, returnHashtag):
        """
            Enter Current photo profile
        """
        ##Click name in foto of the profile to enter profile##
        self.exceptionHandler("//div[@class = 'e1e1d']")
        sleep(2)
        likes, elements = self.obj.fastCheck()
        
        ##get top 3 photos##
        sortedLikes = sorted(likes, key=lambda x: x[0], reverse= True)
        best = [x[2] for x in sortedLikes[:3]]
        #print(sortedLikes[:3])
        #print(best)
        for i in range(len(best)):
            print(elements[best[i]])
            errorCode = self.obj.interactThread(func= self.exceptionHandler, path= elements[best[i]], trys= 3)
            if errorCode == 1: continue
            #self.web_driver.execute_script("arguments[0].click();", elements[best[i]])
            #self.iteratePhotos(elements[best[i]])
            sleep(3)
            if(self.obj.havingLike()): 
                self.exceptionHandler("//div[ contains(@class, 'Igw0E ')]/button[@class = 'wpO6b ']")
            
            ##Like Photo
            if(random.choice([True,False])):
                self.exceptionHandler("/html/body/div[4]/div[2]/div/article/div[2]/section[1]/span[1]/button")
            
            ##close photo##
            self.exceptionHandler("//div[ contains(@class, 'Igw0E ')]/button[@class = 'wpO6b ']")
            sleep(2)
        self.obj.enterHashtag(returnHashtag)
        return 1

    def iteratePhotos(self, path):
        """
            Open other fotos

            Variables
            -> path: Xpath to open (photo)
        """
        self.exceptionHandler(path)


        

        

    