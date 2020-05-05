'''
    Developers: Yael Abelardo Martínez & Hugo Armando Zepeda Ruiz
    Created: 03,2020
    Purpose: Automation of interaction in Instagram from Mexican Sombrero & -less, Testing
    Copyright
'''
from igStart import igStart
from igJSON import jsonConstructor
import json

import os
#Library to control the timings of execution
from time import sleep
#Principal library for web scrapping
from selenium import webdriver
from selenium.webdriver.common import keys
from selenium.webdriver.remote.command import Command
from selenium.common.exceptions import NoSuchElementException
#Library to print personalize message. Allows more control in message control 
import logging
from logging import StreamHandler



class igFollowers(igStart):
    def __init__(self):
        pass

    def profile(self):
        self.web_driver.find_element_by_xpath("/html/body/div[1]/section/nav/div[2]/div/div/div[3]/div/div[5]/a").click()
        sleep(2)
        self.follow()

    def follow(self):
        #Check followers
        followers = int(self.web_driver.find_element_by_xpath("//*[local-name()='ul']/*[local-name()='li'][2]//*[local-name()='span']").text)

        self.web_driver.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/ul/li[2]/a").click()
        sleep(2)

        last_ht, ht = 0, 1
        while last_ht != ht:
            last_ht = ht
            sleep(1)
            ht = self.web_driver.execute_script("""
            arguments[0].scrollTo(0, arguments[0].scrollHeight);
            return arguments[0].scrollHeight;
            """, self.web_driver.find_element_by_xpath("//*[local-name()='div' and @role='dialog']/*[local-name()='div' and @class='isgrP']"))
        
        followerInfo = {}
        follower = jsonConstructor()
        for i in range(followers):
            path = "//*[local-name()='div' and @class='PZuss']/*[local-name()='li'][" + str(i) + "]//*[local-name()='div' and @id]//*[local-name()='a']"
            follower.append(follower.getAttributes(path,"text"),"Followers",followerInfo)
        print(followerInfo)
        sleep(500)
        self.unfollow()

    def unfollow(self):
        #Check unfollowers 
        self.web_driver.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/ul/li[2]/a").click()
        sleep(2) 
        self.web_driver.find_element_by_xpath("/html/body/div[4]/div/div[1]/div/div[2]/button").click()
        sleep(2)


