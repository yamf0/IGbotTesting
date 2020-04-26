'''
    Developers: Yael Abelardo Martínez & Hugo Armando Zepeda Ruiz
    Created: 03,2020
    Purpose: Automation of interaction in Instagram fro Mexican Sombrero & -less. 
'''

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
import json

#Find PATH to current Directory (to find the driver)
path_driver = os.path.dirname(os.path.realpath(__file__))
print (path_driver)

#------------------LOGGER CONFIGURATION------------------------------#

##Create a custom logger for this .py
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

##Creates a Handler (this way only logger will print in terminal logging msg)
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - at line - %(lineno)s - %(levelname)s - %(message)s',style="%")
handler.setFormatter(formatter)
logger.addHandler(handler)

##Add all .DEBUG msg to specific File
file = logging.FileHandler("msg.log",mode='w')
file.setFormatter(formatter)
logger.addHandler(file)

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


class InstaComment ():
    def __init__(self, username, pw):
        self.username = username
        self.pw = pw
        #create photo data dictionary
        self.photo_data = {}

    def start_account(self):

        self.web_driver = webdriver.Chrome(path_driver + "\chromedriver\chromedriver.exe" )
        self.web_driver.get("https://instagram.com")
        sleep(2)
        self.web_driver.find_element_by_name("username").send_keys(self.username)
        sleep(1)
        self.web_driver.find_element_by_name("password").send_keys(self.pw)
        sleep (3)
        self.web_driver.find_element_by_xpath("/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div[4]/button/div").click()
        sleep(3)

        logger.info("Account successfully opened")

        self.Exception_Handler("/html/body/div[4]/div/div/div[3]/button[2]")
        #self.web_driver.find_element_by_xpath("/html/body/div[4]/div/div/div[3]/button[2]").click()
        sleep(3)

        for i in range (4):
            logger.info("Hashtag number: {} ".format(i))
            self.iterate_hastag(self.hashtag())
        self.web_driver.quit()

    def iterate_hastag(self,hashtag_global):
        """
            Will iterate through the hastags
        """
        #create dict
        self.photo_data.update({hashtag_global:{}})

        self.com_count = 14
        self.max_comm = self.com_count
        ##Search the Hashtag
        self.web_driver.find_element_by_xpath("/html/body/div[1]/section/nav/div[2]/div/div/div[2]/input").send_keys(hashtag_global)

        sleep(4)

        logger.info("Hashtag is: " + hashtag_global)
        self.Exception_Handler("/html/body/div[1]/section/nav/div[2]/div/div/div[2]/div[2]/div[2]/div/a[1]")
        #self.web_driver.find_element_by_xpath("/html/body/div[1]/section/nav/div[2]/div/div/div[2]/div[2]/div[2]/div/a[1]").click()
        
        sleep(3)
        self.iterate_photos("top",hashtag_global)
        
    def iterate_photos(self, section, hashtag_global):
        """
            Will do the iteration through the photos 
        """
        #Check if section is over
        if section == "top" :
            path_init = "/html/body/div[1]/section/main/article/div[1]/div/div/"    
        else:
            path_init = "/html/body/div[1]/section/main/article/div[2]/div/"    
        path_end = "/a/div/div[2]"
        for i in range(1,4):
            path_i = "div["+ str(i) + "]"
            for j in range(1,4):
                path_j = "/div[" + str(j) + "]"

                #Generate the Comment for that point
                self.used_comment = self.comment()
                #click the image
                real_path=path_init+path_i+path_j+path_end
                ##HERE WE TRY THE EXCEPTION HANDLER
                self.Exception_Handler(real_path)
                
                sleep(5)

                ##Search previous Like
                if (self.has_like()):
                    self.web_driver.find_element_by_xpath("/html/body/div[4]/div[3]/button").click()
                    sleep(1)
                    continue
                
                photo_info = self.get_photo_info(hashtag_global)
                sleep(5)
                choice = random.choices([True,False],[((math.e)**((self.com_count/self.max_comm)-1)),((math.e)**(-self.com_count/self.max_comm))],k=1)
                print (choice[0])
                print(self.com_count)
                if (choice[0]):
                    
                    self.com_count = self.com_count - 1
                    #Click Like
                    self.Exception_Handler("/html/body/div[4]/div[2]/div/article/div[2]/section[1]/span[1]/button")
                    sleep(2)
                    ##Click comment
                    self.web_driver.find_element_by_xpath("/html/body/div[4]/div[2]/div/article/div[2]/section[1]/span[2]/button").click()
                    self.web_driver.find_element_by_xpath("/html/body/div[4]/div[2]/div/article/div[2]/section[3]/div/form/textarea").send_keys(self.used_comment)
                    self.web_driver.find_element_by_xpath("/html/body/div[4]/div[2]/div/article/div[2]/section[3]/div/form/button").click()
                    sleep(1)
                    ##close photo
                    self.web_driver.find_element_by_xpath("/html/body/div[4]/div[3]/button").click()
                    if not (self.CheckComment(real_path)):
                        self.Scroll()
                        return 
                    if (self.com_count==0):
                        self.web_driver.find_element_by_xpath("/html/body/div[4]/div[3]/button").click()
                        return                
                ##This is the close Button
                self.web_driver.find_element_by_xpath("/html/body/div[4]/div[3]/button").click()
                sleep(2)
        if (section == "recent"): return
        ##Rerun Hashtag for recent photos
        self.iterate_photos("recent",hashtag_global)

    def hashtag(self):
        """
            Will choose randomly a Hashtag and rerturn its value
        """
        choose = random.randint(0,len(poss)-1)
        hashtag = poss[choose]
        poss.pop(choose)
        return hashtag
    
    def comment (self):
        """
            Will choose a comment depending on the hashtag that was opened
        """
        num = random.randint(0,len(comm)-1)
        comment = comm[num]
        return comment

    def has_like (self):
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
                sleep (3)
                i+= 1
                if (i == 5) :
                    self.web_driver.find_element_by_xpath("/html/body/div[4]/div[3]/button").click()
                continue

        if fill == "#ed4956":
            return True
        else:
            return False

    def Exception_Handler (self,xpath):
        """
            Method will try to click Xpath, if not find will wait untill it is found (Solves Bad internet Issue)
        """
        while (True):
            try:
                self.web_driver.find_element_by_xpath(xpath).click()
                break

            except Exception as ex:
                logger.warning("Unable to access xpath")
                sleep(3)
                continue

    def CheckComment(self,realpath):
        #Opening photo again
        self.web_driver.find_element_by_xpath(realpath).click()
        sleep(2)
        try:
            self.web_driver.find_element_by_xpath("//*[local-name()='div']/*[local-name()='article']//*[contains(text(),\"{}\")]".format(self.used_comment))
            logger.info("Comment was succesfully made")
            return True
        except:
            logger.warning("Unable to find Comment")
            return False

    def Scroll (self):
        ##Close the Photo
        self.web_driver.find_element_by_xpath("/html/body/div[4]/div[3]/button").click()
        sleep(2)
        ##Click Return "Instagram Button"
        self.Exception_Handler("/html/body/div[1]/section/nav/div[2]/div/div/div[1]/a")
        logger.info("returned to Main page")
        #self.web_driver.find_element_by_xpath("/html/body/div[1]/section/nav/div[2]/div/div/div[1]/a/div/div/img").click()
        sleep(2)
        self.Exception_Handler("/html/body/div[1]/section/main/section/div[1]/div/div/div/div[1]/button")
        logger.info("start checking histories, expected return at: {} minutes".format(localtime()[4] + 5))
        sleep(300)
        self.Exception_Handler("/html/body/div[1]/section/div/div/section/div[2]/button[3]")  

    def get_photo_info(self, hashtag_global):

        photo_info = {}
        photo_number = self.max_comm - self.com_count 
        photo_profile = self.attributes("/html/body/div[4]/div[2]/div/article/header/div[2]/div[1]/div[1]/a","text")
        photo_likes = self.attributes("/html/body/div[4]/div[2]/div/article/div[2]/section[2]/div/div/button/span","text")
        photo_info_insta = self.attributes("//*[local-name()='div']/*[local-name()='article']//*[local-name()='div' and @class='KL4Bh']/*[local-name()='img']","alt")
        photo_link = self.attributes("//*[local-name()='div']/*[local-name()='article']//*[local-name()='img']","src")
        photo_info.update({
            "Profile": photo_profile,
            "likes": photo_likes,
            "info_insta": photo_info_insta,
            "link": photo_link,
        })
        self.photo_data[hashtag_global].update({photo_number:photo_info})
        self.write_info()

    
    
    def attributes (self, xpath, attr):
        try:
            if (attr == 'text'):
                return self.web_driver.find_element_by_xpath(xpath).text
            else:
                return self.web_driver.find_element_by_xpath(xpath).get_attribute(attr)
        except:
            print("element not found")

    def write_info(self):
        with open ("photo_info.json", "w") as file:
            json.dump(self.photo_data, file, sort_keys=True, indent=4, separators=(',',':'))

def main ():
    #Little GUI
    var = input("Running Mexican(1) or testing account(2)?")
    if(var == '1'):
        var_1 = input("Running Mexican(1) or Mexicanless(2)?")
        if (var_1 == '1'):
            logger.debug("Running in Mexicansombrero account")
            Bot = InstaComment('mexicansombrero','YaelHugoPato')
            Bot.start_account()
        elif (var_1 == '2'): 
            logger.debug("Running in Mexicansombreroless account")
            Bot = InstaComment('mexicansombreroless','mannheimzittau')
            Bot.start_account()
        else:
            print("Stop playing around! Work please")
    elif(var == '2'):
        var_3 = input("Are you Hugo(h), Yael(y)?")
        if(var_3 == 'h') | (var_3 == 'y'):
            logger.debug("Running in Test account")
            Bot = InstaComment('photoandtravel2020','mannheimzittau')
            Bot.start_account()
        else:
            account = input("Please give the account username")
            password = input("Please give the password")
            print("You entered: " + account)
            print("You entered: " + password)
            var_2 = input("Is the data true(1)? Any other number for no.")
            if(var_2 == '1'):
                logger.debug("Running in Test account")
                Bot = InstaComment(account,password)
                Bot.start_account()
            else:
                print("Last change, bitch")
                account_1 = input("Please give again the account username")
                password_1 = input("Please give again the password")
                logger.debug("Running in Test account")
                Bot = InstaComment(account_1,password_1)
                Bot.start_account()
    else: 
        print("Stop playing around! Work please")


    """
    ##Create the argument parser to know which account will be runned the code on
    ap = argparse.ArgumentParser()
    ap.add_argument("-a", "--account", required=True,\
        help="Which account will be used (s for mexicansombrero // less for mexicansombreroless")
    args = vars(ap.parse_args())

    ##Start code with required account
    if args['account'] == "less":
        logger.debug("Running in Mexicansombreroless account")
        Bot = InstaComment('mexicansombreroless','mannheimzittau')
        Bot.start_account()
    if args['account'] == "s":
        logger.debug("Running in Mexicansombrero account")
        Bot = InstaComment('mexicansombrero','YaelHugoPato')
        Bot.start_account()
    if args['account'] == "test":
        logger.debug("Running in Test account")
        Bot = InstaComment('photoandtravel2020','mannheimzittau')
        Bot.start_account()
        """

if __name__ == "__main__":
    main()