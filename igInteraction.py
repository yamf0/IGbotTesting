'''
    Developers: Yael Abelardo Martínez, Oscar Herrera & Hugo Armando Zepeda Ruiz
    Created: 03,2020
    Purpose: Automation of interaction in Instagram from Mexican Sombrero & -less, Testing
    Copyright
'''
#from igStart import igStart
from igFollowers import igFollowers
from logging import StreamHandler
from igJSON import jsonConstructor
from igAntiban import igAntiban
#from driveFile import driveFile
from igProfile import igProfile

import os
#Library to control the timings of execution
from time import sleep
import threading
from concurrent import futures
#Principal library for web scrapping
from selenium import webdriver
from selenium.webdriver.common import keys
from selenium.webdriver.remote.command import Command
from selenium.common.exceptions import NoSuchElementException
#Libraries used to avoid being banned
import random
import argparse
import math
#Library to print personalize message. Allows more control in message control 

#---------------------LOGGER--------------------------------#
import logging
import logging.config

logging.config.fileConfig('logging.conf')

logger = logging.getLogger('igInteraction')

#Library to Data science
from scipy.stats import norm
import numpy as np
#Library for checking the code
import inspect

#TODO CHANGE find_element_by_xpath --->> find_element(By.XPATH, xpath)
class igInteraction(jsonConstructor):
    """
        Class that starts the interaction through Likes & Comments
    """
    def __init__(self, obj):
        super().__init__()
        self.web_driver = obj.driver
        self.obj = obj

    def enterHashtag(self, hashtagGlobal):
        """
            Will enter a hashtag

            Variables:
                ->hashtagGlobal: hashtag to enter to
        """
        
        self.web_driver.find_element_by_xpath("//input[@type = 'text' or @class = 'XTCLo x3qfX']").send_keys(hashtagGlobal)
        self.web_driver.antiBan.randomSleep()
        self.obj.exceptionHandler("//div[@class = 'fuqBx']//a[1]")
        self.web_driver.antiBan.randomSleep()
        return 1

    def iterateHastag(self,hashtagGlobal):
        """
            Will iterate through the hastags

            Variables:
                ->hashtagGlobal: hashtag used in iteration
        """

        self.web_driver.hashtagData.update({hashtagGlobal:{}})
        self.comCount = 10
        self.maxComm = self.comCount

        #TODO cambiar por el metodo nuevo
        ##Search the Hashtag
        sleep(2)
        self.web_driver.find_element_by_xpath("//input[@type = 'text' or @class = 'XTCLo x3qfX']").send_keys(hashtagGlobal)
        self.web_driver.antiBan.randomSleep()
        self.web_driver.exceptionHandler("//div[@class = 'fuqBx']//a[1]")
        self.web_driver.antiBan.randomSleep()
        self.prof = 3
        #TODO Buscar aqui las fotos que estan en cada ### (tomar como base el de iterar perfil ajeno) para no hacerlo por recursion
        self.iteratePhotos("top",hashtagGlobal)
    
    def iteratePhotos(self, section, hashtagGlobal):
        """
            Will do the iteration through the photos

            Variables:
                section: HTML div element
        """

        #TODO esto se soluciona con el ultimo commentario
        if section == "top" :
            pathInit = "/html/body/div[1]/section/main/article/div[1]/div/div/"    
        else:
            pathInit = "/html/body/div[1]/section/main/article/div[2]/div/"    
        pathEnd = "/a/div/div[2]"
        for i in range(1,4):
            pathI = "div["+ str(i) + "]"
            for j in range(1,4):
                pathJ = "/div[" + str(j) + "]"
                #Generate the Comment for that point
                self.usedComment = self.generateComment()
                #click the image
                realPath=pathInit+pathI+pathJ+pathEnd
                
                #TODO ver como se puede integrar lo de thread al nuevo codigo
                #HERE WE TRY THE EXCEPTION HANDLER
                errorCode = self.interactThread(func= self.web_driver.exceptionHandler, path= realPath, trys= 3)
                if errorCode == 1:
                    self.web_driver.antiBan.randomSleep()
                    continue
                #self.exceptionHandler(realPath)
                self.web_driver.antiBan.randomSleep()
                #Search previous Like
                if (self.havingLike()):
                    logger.info("Photo already has like or could not open photo")
                    #close the picture
                    self.web_driver.find_element_by_xpath("//div[ contains(@class, 'Igw0E ')]/button[@class = 'wpO6b ']").click()
                    self.web_driver.antiBan.randomSleep()
                    continue

                #TODO INTEGRAR HAS XPATH EN OTROS LUGARES QUE HACEMOS LO MISMO     
                #Check if comments are disabled
                if (self.hasXpath("//div[@class = '_7UhW9   xLCgt      MMzan        mDXrS   uL8Hv     l4b0S    ']")):
                    #//div[contains(@class, 'MhyEU')]/div[@class = '_7UhW9   xLCgt      MMzan        mDXrS   uL8Hv     l4b0S    '] por si falla el otro
                    #Close Photo
                    self.web_driver.find_element_by_xpath("//div[ contains(@class, 'Igw0E ')]/button[@class = 'wpO6b ']").click()
                    print ("Comments on Photo are Disabled")
                    self.web_driver.antiBan.randomSleep()
                    continue

                #Do the necessary math to see if making the comment
                choice = random.choices([True,False],[((math.e)**((self.comCount/self.maxComm)-1)),((math.e)**(-self.comCount/self.maxComm))],k=1)
                print (choice[0])
                print(self.comCount)

                ##Check the number of likes the photo has and if it is a cool photo or not
                photoLikes, cool = self.coolPhoto()
               
                if (choice[0]):

                    ##Get the info of the photo and save the information in the Jsons##
                    self.getPhotoInfo(photoLikes, hashtagGlobal)

                    self.comCount = self.comCount - 1

                    #TODO MANDAR ESTAS A LA FUNCION NUEVA DE EXCEPTION HANDLER
                    #Click Like
                    self.web_driver.exceptionHandler("//div[contains(@class, eo2As)]//span[@class = 'fr66n']/button")
                    self.web_driver.antiBan.randomSleep()
                    ##Click comment
                    self.web_driver.find_element_by_xpath("//div[contains(@class, eo2As)]//span[@class = '_15y0l']/button").click()
                    self.web_driver.find_element_by_xpath("//div[contains(@class, eo2As)]//form/textarea").send_keys(self.usedComment)
                    self.web_driver.find_element_by_xpath("//div[contains(@class, eo2As)]//form/button").click()
                    self.web_driver.antiBan.randomSleep()

                    ##Will Photo be opened or not???##
                
                    
                    ##close photo
                    self.web_driver.find_element_by_xpath("//div[ contains(@class, 'Igw0E ')]/button[@class = 'wpO6b ']").click()
                    if not (self.checkComment(realPath)):
                        self.web_driver.antiBan.histories()
                        return 
                    if (self.comCount==0):
                        self.web_driver.find_element_by_xpath("//div[ contains(@class, 'Igw0E ')]/button[@class = 'wpO6b ']").click()
                        return                
                    #cool <= photoLikes and self.prof >= 0
                    if (cool <= photoLikes and self.prof >= 0 and self.likedPhotos): 
                        self.prof -= 1
                        self.web_driver.antiBan.enterProfile(hashtagGlobal)
                        continue
                        #self.exceptionHandler(realPath)
                        #self.web_driver.antiBan.randomSleep()
                       
                #This is the close button
                self.web_driver.exceptionHandler("//div[ contains(@class, 'Igw0E ')]/button[@class = 'wpO6b ']", 5)
                self.web_driver.antiBan.randomSleep()
        if (section == "recent"): return
        #Re-run Hashtag for recent photos
        self.iteratePhotos("recent",hashtagGlobal)


    def havingLike (self):
        """
            Will see if the chosen photo has already a like 
        """
        i=0
        while (True):
            try:
                fill = self.web_driver.find_element_by_xpath("//*[local-name()='span' and @class='fr66n']/*[local-name()='button']/*[local-name()='svg']").get_attribute("fill")
                print(fill)
                break
            except Exception as ex:
                logger.warning("Could not Find the Like Button")
                self.web_driver.antiBan.randomSleep()
                i+= 1
                if (i == 5) :
                    break
                continue

        if fill == "#ed4956":
            return True
        else:
            return False
    
    def getPhotoInfo(self, photoLikes, hashtagGlobal):
        """
            Will get the information of the current opened photo
            
            return -> 0 succesfull
        """

            #create writable Dict
        photoInfo = {}

        photoNumber = self.maxComm - self.comCount 
        #get profile of the photo
        photoProfile = self.getAttributes("/html/body/div[4]/div[2]/div/article/header/div[2]/div[1]/div[1]/a","text")
        #get info of the foto from IG
        photoInfoInsta = self.getAttributes("//*[local-name()='div']/*[local-name()='article']//*[local-name()='div' and @class='KL4Bh']/*[local-name()='img']","alt")
        #Get link of photo
        photoLink = self.getAttributes("//*[local-name()='div']/*[local-name()='article']//*[local-name()='img']","src")
        #Get hashtags from photo
        photoHashtags = self.getListAttributes("//*[local-name()='a' and @class = ' xil3i']")

        ##Get the last number photo in dictionary
        if(self.web_driver.timeOfRun in self.web_driver.permaData.keys()):
            lastNumber = list(self.web_driver.permaData[self.web_driver.timeOfRun].keys())[-1] + 1
        else:
            lastNumber = 0
        
        ##Put info into Server JSON##
        photoData = {"Profile": photoProfile,"Likes": photoLikes,"hashtag": photoHashtags}
        #put photoData under last photo number in photoData global dict
        self.append(photoData, (lastNumber) , self.photoData)
        #put photoData global under time of run in the permament Data dict (this will be appended to all times ran dictionary)
        self.append(self.photoData, self.timeOfRun, self.permaData)


        ##Put info into Local JSON##
        ##this info will help for the generation of the Comments
        self.append(({"Profile": photoProfile,"Likes": photoLikes,"InfoInsta": photoInfoInsta,"Link": photoLink}), photoNumber, photoInfo)
        self.append(photoInfo, hashtagGlobal, self.hashtagData)
        ##Write to the Json the information
        self.writeInfo("photoInfo","w",self.hashtagData)

        return 0 

    def coolPhoto (self):
        """
            Check if the photo is really liked or not
        """
        ##<<<<<<<<TODO MANDAR Todo esto a una funcion (se encarga de checar si la foto es muy gustada o no)
        ##check if Photo is liked##
        photoLikes = self.getAttributes("//div//button[@class = 'sqdOP yWX7d     _8A5w5    ']/span","text")
        
        sleep(2)

        if(photoLikes):
            if("," in photoLikes):  photoLikes = photoLikes.replace(",","")
            photoLikes = int(photoLikes) 
            self.likes = np.append(self.likes, photoLikes)
        else:
            photoLikes = 0
        mu, std = norm.fit(self.likes)
        
        ##check for 2 z deviations from center##
        cool = mu + 2 * std
        print("Photos with more than {} Likes are cool".format(cool))
        
        return photoLikes, cool
       

    def checkComment(self,realPath):
        #Opening photo again
        self.web_driver.find_element_by_xpath(realPath).click()
        self.web_driver.antiBan.randomSleep()
        try:
            self.web_driver.find_element_by_xpath("//div/article//h3[//a[contains(text(),\"{}\")]]/following-sibling::span".format(self.web_driver.username))
            logger.info("Comment was succesfully made")
            return True
        except:
            #logger.warning("Unable to find Comment")
            return False
       
    def interactThread (self, **kwargs):
        """
            Open a Path which reference to an image using Threads

            Variables:
                ->path: relative path to the image to open
        """
        
        func = kwargs["func"]
        kwargs.pop("func")
        arguments= inspect.getfullargspec(func)[0][1:]
        default = func.__defaults__
        #print(default)
        
        if len(kwargs)  < len(arguments)-len(default):
            logger.error("You missed an argument to pass, passed args {}, required {}".format(kwargs, arguments))
            return 1
    
        args = [arg for arg in kwargs.values()]
        #Try to click the image
        with futures.ThreadPoolExecutor() as ex:
            f1 = ex.submit(func, *args)
            result = f1.result()
            print ("RESULTS",result)
            return result
