'''
    Developers: Yael Abelardo Martínez & Hugo Armando Zepeda Ruiz
    Created: 03,2020
    Purpose: Automation of interaction in Instagram fro Mexican Sombrero & -less. 
'''
import os
from time import sleep
from selenium import webdriver
from selenium.webdriver.common import keys
from selenium.webdriver.remote.command import Command
from selenium.common.exceptions import NoSuchElementException
import random
import argparse
import math

#Find PATH to current Directory (to find the driver)
path_driver = os.path.dirname(os.path.realpath(__file__))
print (path_driver)


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
        self.web_driver = webdriver.Chrome(path_driver + "\chromedriver\chromedriver.exe" )
        self.web_driver.get("https://instagram.com")
        sleep(2)
        self.web_driver.find_element_by_name("username").send_keys(username)
        sleep(1)
        self.web_driver.find_element_by_name("password").send_keys(pw)
        sleep (3)
        self.web_driver.find_element_by_xpath("/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div[4]/button/div").click()
        sleep(3)

        self.Exception_Handler("/html/body/div[4]/div/div/div[3]/button[2]")
        #self.web_driver.find_element_by_xpath("/html/body/div[4]/div/div/div[3]/button[2]").click()
        sleep(3)
        for i in range (10):
            self.iterate_hastag(self.hashtag())
        self.web_driver.quit()

    def iterate_hastag(self,hashtag_global):
        """
            Will iterate through the hastags 
        """
        self.com_count = 10
        ##Search the Hashtag
        self.web_driver.find_element_by_xpath("/html/body/div[1]/section/nav/div[2]/div/div/div[2]/input").send_keys(hashtag_global)

        sleep(4)

        self.Exception_Handler("/html/body/div[1]/section/nav/div[2]/div/div/div[2]/div[2]/div[2]/div/a[1]")
        #self.web_driver.find_element_by_xpath("/html/body/div[1]/section/nav/div[2]/div/div/div[2]/div[2]/div[2]/div/a[1]").click()
        
        sleep(3)
        
        self.iterate_photos("top",hashtag_global)
        self.iterate_photos("recent",hashtag_global)
        
    def iterate_photos(self, section,hashtag_global):
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
                #self.web_driver.find_element_by_xpath(real_path).click()
                sleep(5)

                ##Search previous Like
                if (self.has_like()):
                    self.web_driver.find_element_by_xpath("/html/body/div[4]/div[3]/button").click()
                    sleep(1)
                    continue
                
                #Click Like
                self.Exception_Handler("/html/body/div[4]/div[2]/div/article/div[2]/section[1]/span[1]/button")
                #self.web_driver.find_element_by_xpath("/html/body/div[4]/div[2]/div/article/div[2]/section[1]/span[1]/button").click()
                sleep(2)
                choice = random.choices([True,False],[((math.e)**((self.com_count/10)-1)),((math.e)**(-self.com_count/10))],k=1)
                print (choice[0])
                print(self.com_count)
                if (choice[0]):
                    self.com_count = self.com_count - 1
                    self.web_driver.find_element_by_xpath("/html/body/div[4]/div[2]/div/article/div[2]/section[1]/span[2]/button").click()
                    self.web_driver.find_element_by_xpath("/html/body/div[4]/div[2]/div/article/div[2]/section[3]/div/form/textarea").send_keys(self.used_comment)
                    self.web_driver.find_element_by_xpath("/html/body/div[4]/div[2]/div/article/div[2]/section[3]/div/form/button").click()
                    sleep(3)
                    if (self.com_count==0):
                        self.web_driver.find_element_by_xpath("/html/body/div[4]/div[3]/button").click()
                        return
                
                ##This is the close Button
                self.web_driver.find_element_by_xpath("/html/body/div[4]/div[3]/button").click()
                sleep(2)

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
                print (ex)
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
                print (ex)
                sleep(3)
                continue

def main ():
    ##Create the argument parser to know which account will be runned the code on
    ap = argparse.ArgumentParser()
    ap.add_argument("-a", "--account", required=True,\
        help="Which account will be used (s for mexicansombrero // less for mexicansombreroless")
    args = vars(ap.parse_args())

    ##Start code with required account
    if args['account'] == "less":
        Bot = InstaComment('mexicansombreroless','mannheimzittau')
    if args['account'] == "s":
        Bot = InstaComment('mexicansombrero','YaelHugoPato')

if __name__ == "__main__":
    main()