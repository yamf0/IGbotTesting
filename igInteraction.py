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


#Lists of hashstags & comments.
poss = ["#stayandwander", "#europe_perfection","#landscape", "#travel", "#travelphotography", "#travelling","#wanderlust",\
"#wanderlusting", "#wanderluster", "#europetravel","#sunset","#traveltheworld", "#travellingthroughtheworld"]
comm = ["what an amazing pic!", "Perfection", "We loved it", "Keep up the Great Photos", "This place is amazing",\
    "This is amazing", "Congrats for the great photo", "What a Pic!!!", "That is great!",\
    "Wow that pic!", "This place is amazing", "Keep up the great photos", "Amazing",\
    "Perfect!", "Amazing", "That is nice!", "Great",\
    "What a destination", "That is amazing", "Great!!!",\
    "Wish to be there","Cannot wait to be there","Nice photo",\
    "Really love this part of the day",\
    "Wish to be there","Cannot wait to be there","Maybe this is the sombrero next destination",\
    "WOW", "This is Perfect", "Congrats for the great Photo", "Simply Beautiful",\
    "Amazing pic!!", "Congrats, this is Great!", "That seems amazing!", "Great Pic",\
    "Pff that is amazing", "Keep up the great Photos", "We loved it", "That is incredible",\
    "Great Photo!", "We loved it!",\
    "Amazing Place!", "that is Amazing!", "WOW", "Perfect!"]



class igInteraction(jsonConstructor):
    """
        Class that starts the interaction through Likes & Comments
    """
    def __init__(self,username,pw, arguments):
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

        self.openAccount()

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

        ##List of current run Likes of photos##
        self.likes = np.random.randint(280, size=300)

        ##Check/Iterate in Profile photos##
        #self.Profile = igProfile(self)
        
        for i in range (4):
            logger.info("Hashtag number: {} ".format(i))
            self.iterateHastag(self.generateHashtag())
            self.writeInfo(self.fileNameRoot, "w", self.permaData)

        if self.runDrive == True:
            self.driveObj.uploadFile(self.fileNames)

        self.web_driver.quit()
        
    def enterHashtag(self, hashtagGlobal):
        """
            Will enter a hashtag

            Variables:
                ->hashtagGlobal: hashtag to enter to
        """
        self.web_driver.find_element_by_xpath("/html/body/div[1]/section/nav/div[2]/div/div/div[2]/input").send_keys(hashtagGlobal)
        self.antiBan.randomSleep()
        self.exceptionHandler("/html/body/div[1]/section/nav/div[2]/div/div/div[2]/div[2]/div[2]/div/a[1]")
        self.antiBan.randomSleep()
        return 1

    def iterateHastag(self,hashtagGlobal):
        """
            Will iterate through the hastags

            Variables:
                hashtagGlobal: hashtag used in iteration
        """
        self.hashtagData.update({hashtagGlobal:{}})
        self.comCount = 10
        self.maxComm = self.comCount
        ##Search the Hashtag
        self.web_driver.find_element_by_xpath("/html/body/div[1]/section/nav/div[2]/div/div/div[2]/input").send_keys(hashtagGlobal)
        self.antiBan.randomSleep()
        self.exceptionHandler("//a[@class= 'yCE8d  '][1]")
        self.antiBan.randomSleep()
        self.prof = 3
        self.iteratePhotos("top",hashtagGlobal)
    
    def iteratePhotos(self, section, hashtagGlobal):
        """
            Will do the iteration through the photos

            Variables:
                section: HTML div element
        """
        self.antiBan.randomSleep()
        photosElements = self.web_driver.find_elements_by_xpath("//div[@class = 'eLAPa']")
        print ("ELEMENTS: ", photosElements)

        
        for j in range(0,10):
            
            #Generate the Comment for that point
            self.usedComment = self.generateComment()
            
            #HERE WE TRY THE EXCEPTION HANDLER
            """errorCode = self.interactThread(self.exceptionHandler, path= realPath, trys= 3)
            if errorCode == 1:
                continue"""

            self.exceptionHandler(photosElements[j], 3)
            #self.exceptionHandler(realPath)
            self.antiBan.randomSleep()
            #Search previous Like
            if (self.havingLike()):
                self.web_driver.find_element_by_xpath("/html/body/div[4]/div[3]/button").click()
                self.antiBan.randomSleep()
                continue

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
            
            
            if (choice[0]):

                
                ##Get info Photos##
                photoInfo = {}

                photoNumber = self.maxComm - self.comCount 
                photoProfile = self.getAttributes("/html/body/div[4]/div[2]/div/article/header/div[2]/div[1]/div[1]/a","text")
                photoInfoInsta = self.getAttributes("//*[local-name()='div']/*[local-name()='article']//*[local-name()='div' and @class='KL4Bh']/*[local-name()='img']","alt")
                photoLink = self.getAttributes("//*[local-name()='div']/*[local-name()='article']//*[local-name()='img']","src")

                photoHashtags = self.getListAttributes("//*[local-name()='a' and @class = ' xil3i']")

                ##Get the last number photo in dictionary
                if(self.timeOfRun in self.permaData.keys()):
                    lastNumber = list(self.permaData[self.timeOfRun].keys())[-1] + 1
                else:
                    lastNumber = 0
                
                ##Put info into Server JSON##
                photoData = {"Profile": photoProfile,"Likes": photoLikes,"hashtag": photoHashtags}
                self.append(photoData, (lastNumber) , self.photoData)
                self.append(self.photoData, self.timeOfRun, self.permaData)

                ##Put info into Local JSON##
                self.append(({"Profile": photoProfile,"Likes": photoLikes,"InfoInsta": photoInfoInsta,"Link": photoLink}), photoNumber, photoInfo)
                self.append(photoInfo,hashtagGlobal, self.hashtagData)
                self.writeInfo("photoInfo","w",self.hashtagData)

                self.comCount = self.comCount - 1
                #Click Like
                self.exceptionHandler("(//div[@class='eo2As ']//button[@class='wpO6b '])[1]")
                self.antiBan.randomSleep()
                ##Click comment
                self.web_driver.find_element_by_xpath("(//div[@class='eo2As ']//button[@class='wpO6b '])[2]").click()
                self.web_driver.find_element_by_xpath("//textarea[contains(@class, 'Ypffh')]").send_keys(self.usedComment)
                self.web_driver.find_element_by_xpath("//textarea[contains(@class, 'Ypffh')]/following-sibling::button").click()
                self.antiBan.randomSleep()

                ##Will Photo be opened or not???##
            
                
                ##close photo
                self.web_driver.find_element_by_xpath("/html/body/div[4]/div[3]/button").click()
                if not (self.checkComment(photosElements[j])):
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
        

        

    def generateHashtag(self):
        """
            Will choose randomly a Hashtag and return its value
        """
        choose = random.randint(0,len(poss)-1)
        hashtag = poss[choose]
        poss.pop(choose)
        return hashtag
    
    def generateComment (self):
        """
            Will choose a comment depending on the hashtag that was opened
        """
        num = random.randint(0,len(comm)-1)
        comment = comm[num]
        return comment

    def havingLike (self):
        """
            Will see if the chosen photo has already a like 
        """
        i=0;
        while (True):
            try:
                fill = self.web_driver.find_element_by_xpath("//div[@class='QBdPU ']/*[local-name()='svg'][1]")\
                        .get_attribute("fill")
                print(fill)
                break
            except Exception as ex:
                #logger.warning("Could not Find the Like Button")
                self.antiBan.randomSleep()
                i+= 1
                if (i == 5) :
                    self.web_driver.find_element_by_xpath("/html/body/div[4]/div[3]/button").click()
                continue

        if fill == "#ed4956":
            return True
        else:
            return False

    def hasXpath(self, path):

        try:
            self.web_driver.find_element_by_xpath(path)
            return True
        except:
            return False

    def checkComment(self, element):
        #Opening photo again
        element.click()
        self.antiBan.randomSleep()
        try:
            self.web_driver.find_element_by_xpath("//div/article//h3[//a[contains(text(),\"{}\")]]/following-sibling::span".format(self.username))
            logger.info("Comment was succesfully made")
            return True
        except:
            #logger.warning("Unable to find Comment")
            return False
       
    def interactThread (self, func, **kwargs):
        """
            Open a Path which reference to an image using Threads

            Variables:
                ->path: relative path to the image to open
        """
        arguments= inspect.getfullargspec(func)[0][1:]
        default = func.__defaults__
        #print(default)
        
        if len(kwargs) < len(arguments)-len(default):
            logger.error("You missed an argument to pass, passed args {}, required {}".format(kwargs, arguments))
            return 1
    
        args = [arg for arg in kwargs.values()]
        #Try to click the image
        with futures.ThreadPoolExecutor() as ex:
            f1 = ex.submit(func, *args)
            result = f1.result()
            return result

        print ("RESULS",result)

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