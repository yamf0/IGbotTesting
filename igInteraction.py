'''
    Developers: Yael Abelardo Martínez & Hugo Armando Zepeda Ruiz
    Created: 03,2020
    Purpose: Automation of interaction in Instagram from Mexican Sombrero & -less, Testing
    Copyright
'''
from igStart import igStart

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
import argparse
import math
#Library to print personalize message. Allows more control in message control 
import logging
from logging import StreamHandler
from igJSON import jsonConstructor
from igAntiban import igAntiban

#Lists of hashstags & comments.
poss = ["#stayandwander", "#europe_perfection","#landscape", "#travel", "#travelphotography", "#travelling","#wanderlust",\
"#wanderlusting", "#wanderluster", "#europetravel","#sunset","#traveltheworld", "#travellingthroughtheworld"]
comm = ["what an amazing pic!", "Perfection", "We loved it", "Keep up the Great Photos", "This place is amazing",\
    "This is amazing", "Congrats for the great photo", "What a Pic!!!", "That is great!",\
    "Wow that pic!", "This place is amazing", "Keep up the great photos", "Amazing",\
    "Perfect!", "Amazing", "That is nice!", "Great",\
    "What a destination", "That is amazing", "Great!!!",\
    "Wish to be there","Cannot wait to be there","Maybe this is the sombrero next destination","Nice photo",\
    "Really love this part of the day",\
    "Wish to be there","Cannot wait to be there","Maybe this is the sombrero next destination",\
    "WOW", "This is Perfect", "Congrats for the great Photo", "Simply Beautiful",\
    "Amazing pic!!", "Congrats, this is Great!", "That seems amazing!", "Great Pic",\
    "Pff that is amazing", "Keep up the great Photos", "We loved it", "That is incredible",\
    "Great Photo!", "We loved it!",\
    "Amazing Place!", "that is Amazing!", "WOW", "Perfect!"]



class igIteraction(jsonConstructor):
    """
        Class that starts the interaction through Likes & Comments
    """
    def __init__(self,username,pw):
        """
            Starting the instagram iteraction 

            Variables:

                username: account name
                pw: password name
        """
        self.username = username
        self.pw = pw
        #self.dicInit()
        self.openAccount()
        self.antiBan = igAntiban()
        ##JSON for current run##
        self.hashtagData = {}
        ##Permanent JSON##
        self.photoData = {self.username : self.timeOfRun}
        for i in range (5):
            #logger.info("Hashtag number: {} ".format(i))
            self.iterateHastag(self.generateHashtag())
        self.web_driver.quit()
    
    def iterateHastag(self,hashtagGlobal):
        """
            Will iterate through the hastags

            Variables:
                hashtagGlobal: hashtag used in iteration
        """
        self.hashtagData.update({hashtagGlobal:{}})
        self.comCount = 14
        self.maxComm = self.comCount
        ##Search the Hashtag
        self.web_driver.find_element_by_xpath("/html/body/div[1]/section/nav/div[2]/div/div/div[2]/input").send_keys(hashtagGlobal)
        sleep(2)
        self.exceptionHandler("/html/body/div[1]/section/nav/div[2]/div/div/div[2]/div[2]/div[2]/div/a[1]")
        sleep(1)
        self.iteratePhotos("top",hashtagGlobal)
    
    def iteratePhotos(self, section, hashtagGlobal):
        """
            Will do the iteration through the photos

            Variables:
                section: HTML div element
        """
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
                #HERE WE TRY THE EXCEPTION HANDLER
                self.exceptionHandler(realPath)
                sleep(5)
                #Search previous Like
                if (self.havingLike()):
                    self.web_driver.find_element_by_xpath("/html/body/div[4]/div[3]/button").click()
                    sleep(1)
                    continue
                #Do the necessary math to see if making the comment
                choice = random.choices([True,False],[((math.e)**((self.comCount/self.maxComm)-1)),((math.e)**(-self.comCount/self.maxComm))],k=1)
                print (choice[0])
                print(self.comCount)
                if (choice[0]):
                    ##Get info Photos##
                    photoInfo = {}
                    photoNumber = self.maxComm - self.comCount 
                    photoProfile =self.append(self.getAttributes("/html/body/div[4]/div[2]/div/article/header/div[2]/div[1]/div[1]/a","text"), "Profile",photoInfo)
                    photoLikes = self.append(self.getAttributes("/html/body/div[4]/div[2]/div/article/div[2]/section[2]/div/div/button/span","text"), "Likes",photoInfo)
                    photoInfoInsta = self.append(self.getAttributes("//*[local-name()='div']/*[local-name()='article']//*[local-name()='div' and @class='KL4Bh']/*[local-name()='img']","alt"), "Info",photoInfo)
                    photoLink = self.append(self.getAttributes("//*[local-name()='div']/*[local-name()='article']//*[local-name()='img']","src"), "Link",photoInfo)
                    photoHashtags = self.getHastagInfo("//*[local-name()='a' and @class = ' xil3i']")
                    
                    photoHashtags = self.append(photoHashtags, "Hashtags", photoInfo)
                    
                    self.append({photoNumber : photoInfo},hashtagGlobal, self.hashtagData)
                    self.writeInfo("photoInfo","w",self.hashtagData)

                    self.comCount = self.comCount - 1
                    #Click Like
                    self.exceptionHandler("/html/body/div[4]/div[2]/div/article/div[2]/section[1]/span[1]/button")
                    sleep(2)
                    ##Click comment
                    self.web_driver.find_element_by_xpath("/html/body/div[4]/div[2]/div/article/div[2]/section[1]/span[2]/button").click()
                    self.web_driver.find_element_by_xpath("/html/body/div[4]/div[2]/div/article/div[2]/section[3]/div/form/textarea").send_keys(self.usedComment)
                    self.web_driver.find_element_by_xpath("/html/body/div[4]/div[2]/div/article/div[2]/section[3]/div/form/button").click()
                    sleep(3)
                    #close photo
                    #self.web_driver.find_element_by_xpath("/html/body/div[4]/div[3]/button").click()
                    """
                        if not (self.CheckComment(real_path)):
                        self.Scroll()
                        return 
                    """
                    if (self.comCount==0):
                        self.web_driver.find_element_by_xpath("/html/body/div[4]/div[3]/button").click()
                        return                
                #This is the close button
                self.web_driver.find_element_by_xpath("/html/body/div[4]/div[3]/button").click()
                sleep(2)
        if (section == "recent"): return
        #Re-run Hashtag for recent photos
        self.iteratePhotos("recent",hashtagGlobal)

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
                fill = self.web_driver.find_element_by_xpath("//*[local-name()='span' and @class='fr66n']/*[local-name()='button']/*[local-name()='svg']").get_attribute("fill")
                print(fill)
                break
            except Exception as ex:
                #logger.warning("Could not Find the Like Button")
                sleep (3)
                i+= 1
                if (i == 5) :
                    self.web_driver.find_element_by_xpath("/html/body/div[4]/div[3]/button").click()
                continue

        if fill == "#ed4956":
            return True
        else:
            return False

def main ():
    #Little GUI
    var = input("Running Mexican(1) // test code in Mexico(2) // test code in Germany (3) // Any other number for another account ")
    if(var == '1'):
        var_1 = input("Running Mexican(1) or Mexicanless(2)?")
        if (var_1 == '1'):
            Bot = igIteraction('mexicansombrero','YaelHugoPato')
        elif (var_1 == '2'): 
            Bot = igIteraction('mexicansombreroless','mannheimzittau')
        else:
            print("Input error")
    elif(var == '2'):
        Bot = igIteraction('photoandtravel2020','mannheimzittau')
    elif(var == '3'):
        Bot = igIteraction('travelandphoto2020','mannheimzittau')  
    else: 
        account = input("Please give the account username")
        password = input("Please give the password")
        print("You entered: " + account)
        print("You entered: " + password)
        var_2 = input("Is the data true(1)? Any other number for no.")
        if(var_2 == '1'):
            Bot = igIteraction(account,password)
        else:
            print("Input error")

if __name__ == "__main__":
    main()