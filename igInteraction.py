'''
    Developers: Yael Abelardo Martínez, Oscar Herrera & Hugo Armando Zepeda Ruiz
    Created: 03,2020
    Purpose: Automation of interaction in Instagram from Mexican Sombrero & -less, Testing
    Copyright
'''
from igStart import igStart
from igFollowers import igFollowers
from logging import StreamHandler
from igJSON import jsonConstructor
from igAntiban import igAntiban
from driveFile import driveFile
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

logger = logging.getLogger('root')

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
    def __init__(self, username, pw, arguments):
        """
            Starting the instagram iteraction 

            Variables:

                username: account name
                pw: password name
        """
        
        self.username = username
        self.pw = pw
        self.fileNameRoot = self.username 
        self.runDrive = arguments.drive

        if self.runDrive == True:
            self.driveObj = driveFile(self)

        self.openAccount() #TODO Se hara con el Main

        #TODO CREAR TODOS LOS OBJETOS DE LAS FUNCIONES QUE NECESITEMOS AQUI
        self.antiBan = igAntiban(self) 
        ##JSON for current run##
        self.hashtagData = {}
        ##Permanent JSON for Data Science##
        ##return Dict for username running##
        if (os.path.isfile(self.fileNameRoot + ".json")):
            self.permaData = self.loadInfo(self.fileNameRoot + ".json")
        else:
            self.permaData = {}
        self.photoData = {}

        #TODO meter un argumento en ARGPARSE para saber si vamos a correr lo de meterse a una cuenta de una foto con muchos likes
        ## esto nos quita tiempo si lo que se quiere es solo probar // parte del codigo de abajo se tendria que mover a un if##
        ##List of current run Likes of photos##
        self.likes = np.random.randint(280, size=300)

        ##Check/Iterate in Profile photos##
        #self.Profile = igProfile(self)
        
        #TODO Cambiar esto apra que se mande a llamar desde el main Aqui iteramos en el init (esta mal)
        for i in range (4):
            logger.info("Hashtag number: {} ".format(i))
            self.iterateHastag(self.generateHashtag())
            self.writeInfo(self.fileNameRoot, "w", self.permaData)

        #TODO migrar a main
        if self.runDrive == True:
            self.driveObj.uploadFile(self.fileNames)

        self.web_driver.quit()
       
    def enterHashtag(self, hashtagGlobal):
        """
            Will enter a hashtag

            Variables:
                ->hashtagGlobal: hashtag to enter to
        """
        
        self.web_driver.find_element_by_xpath("//input[@type = 'text' or @class = 'XTCLo x3qfX']").send_keys(hashtagGlobal)
        self.antiBan.randomSleep()
        self.exceptionHandler("//div[@class = 'fuqBx']//a[1]")
        self.antiBan.randomSleep()
        return 1

    def iterateHastag(self,hashtagGlobal):
        """
            Will iterate through the hastags

            Variables:
                ->hashtagGlobal: hashtag used in iteration
        """
        self.hashtagData.update({hashtagGlobal:{}})
        self.comCount = 10
        self.maxComm = self.comCount

        #TODO cambiar por el metodo nuevo
        ##Search the Hashtag
        sleep(2)
        self.web_driver.find_element_by_xpath("//input[@type = 'text' or @class = 'XTCLo x3qfX']").send_keys(hashtagGlobal)
        self.antiBan.randomSleep()
        self.exceptionHandler("//div[@class = 'fuqBx']//a[1]")
        self.antiBan.randomSleep()
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
                errorCode = self.interactThread(func= self.exceptionHandler, path= realPath, trys= 3)
                if errorCode == 1:
                    self.antiBan.randomSleep()
                    continue
                #self.exceptionHandler(realPath)
                self.antiBan.randomSleep()
                #Search previous Like
                if (self.havingLike()):
                    logger.info("Photo already has like or could not open photo")
                    #close the picture
                    self.web_driver.find_element_by_xpath("/html/body/div[4]/div[3]/button").click()
                    self.antiBan.randomSleep()
                    continue

                #TODO INTEGRAR HAS XPATH EN OTROS LUGARES QUE HACEMOS LO MISMO     
                #Check if comments are disabled
                if (self.hasXpath("/html/body/div[4]/div[2]/div/article/div[2]/div[3]/div")):
                    #Close Photo
                    self.web_driver.find_element_by_xpath("/html/body/div[4]/div[3]/button").click()
                    print ("Comments on Photo are Disabled")
                    self.antiBan.randomSleep()
                    continue

                #Do the necessary math to see if making the comment
                choice = random.choices([True,False],[((math.e)**((self.comCount/self.maxComm)-1)),((math.e)**(-self.comCount/self.maxComm))],k=1)
                print (choice[0])
                print(self.comCount)

                
                ##<<<<<<<<TODO MANDAR Todo esto a una funcion (se encarga de checar si la foto es muy gustada o no)
                ##check if Photo is liked##
                photoLikes = self.getAttributes("/html/body/div[4]/div[2]/div/article/div[2]/section[2]/div/div/button/span","text")
                
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
                
                ### END TODO>>>>>
               
                if (choice[0]):

                    ##Get the info of the photo and save the information in the Jsons##
                    self.getPhotoInfo(photoLikes, hashtagGlobal)

                    self.comCount = self.comCount - 1

                    #TODO MANDAR ESTAS A LA FUNCION NUEVA DE EXCEPTION HANDLER
                    #Click Like
                    self.exceptionHandler("/html/body/div[4]/div[2]/div/article/div[2]/section[1]/span[1]/button")
                    self.antiBan.randomSleep()
                    ##Click comment
                    self.web_driver.find_element_by_xpath("/html/body/div[4]/div[2]/div/article/div[2]/section[1]/span[2]/button").click()
                    self.web_driver.find_element_by_xpath("/html/body/div[4]/div[2]/div/article/div[2]/section[3]/div/form/textarea").send_keys(self.usedComment)
                    self.web_driver.find_element_by_xpath("/html/body/div[4]/div[2]/div/article/div[2]/section[3]/div/form/button").click()
                    self.antiBan.randomSleep()

                    ##Will Photo be opened or not???##
                
                    
                    ##close photo
                    self.web_driver.find_element_by_xpath("/html/body/div[4]/div[3]/button").click()
                    if not (self.checkComment(realPath)):
                        self.antiBan.histories()
                        return 
                    if (self.comCount==0):
                        self.web_driver.find_element_by_xpath("/html/body/div[4]/div[3]/button").click()
                        return                
                    #cool <= photoLikes and self.prof >= 0
                    if (cool <= photoLikes and self.prof >= 0): 
                        self.prof -= 1
                        self.antiBan.enterProfile(hashtagGlobal)
                        continue
                        #self.exceptionHandler(realPath)
                        #self.antiBan.randomSleep()
                       
                #This is the close button
                self.exceptionHandler("/html/body/div[4]/div[3]/button", 5)
                self.antiBan.randomSleep()
        if (section == "recent"): return
        #Re-run Hashtag for recent photos
        self.iteratePhotos("recent",hashtagGlobal)


    def havingLike (self):
        """
            Will see if the chosen photo has already a like 
        """
        i=0;
        while (True):
            try:
                fill = self.web_driver.find_element_by_xpath("//*[local-name()='span' and @class='fr66n']/*[local-name()='button']/*[local-name()='svg']").get_attribute("fill")
                print(fill)
                break
            except Exception as ex:
                logger.warning("Could not Find the Like Button")
                self.antiBan.randomSleep()
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
        if(self.timeOfRun in self.permaData.keys()):
            lastNumber = list(self.permaData[self.timeOfRun].keys())[-1] + 1
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

    def checkComment(self,realPath):
        #Opening photo again
        self.web_driver.find_element_by_xpath(realPath).click()
        self.antiBan.randomSleep()
        try:
            self.web_driver.find_element_by_xpath("//div/article//h3[//a[contains(text(),\"{}\")]]/following-sibling::span".format(self.username))
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



def main ():
    parser = argparse.ArgumentParser()

    parser.add_argument("-a", "--account", help="Account to run (m for MexicanTest, d for GermanyTest, Account name for other)")
    parser.add_argument("-p", "--password", help="Password to account", default= None)
    parser.add_argument("-d", "--drive", help="Will drive download Info", default=False, action="store_true")

    args = parser.parse_args()

    if (args.account == "m"):
        Bot = igInteraction('photoandtravel2020','mannheimzittau', args)
    
    elif (args.account == "d"):
        Bot = igInteraction('travelandphoto2020','mannheimzittau', args) 
    
    else:
        account = args.account
        password = args.password
        print("You entered: " + account)
        print("You entered: " + password)
        sleep(2)
        Bot = igInteraction(account,password, args)


if __name__ == "__main__":
    main()