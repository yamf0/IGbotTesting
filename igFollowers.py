'''
    Developers: Yael Abelardo Martínez, Oscar Herrera & Hugo Armando Zepeda Ruiz
    Created: 03,2020
    Purpose: Automation of interaction in Instagram from Mexican Sombrero & -less, Testing
    Copyright
'''
from igStart import igStart
from igJSON import jsonConstructor
from igAntiban import igAntiban
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
    def __init__(self, bot):
        self.bot = bot
        self.web_driver = bot.web_driver
        self.antiBan = igAntiban()

    def profile(self):
        self.web_driver.find_element_by_xpath("/html/body/div[1]/section/nav/div[2]/div/div/div[3]/div/div[5]/a").click()
        self.antiBan.randomSleep()
        self.follow()

    def follow(self):
        #Check followers
        self.web_driver.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/ul/li[2]/a/span").click()
        self.antiBan.randomSleep()

        self.follower = jsonConstructor(self.web_driver)
        ##Scroll though the list of followers
        self.follower.scrollList("//*[local-name()='div' and @role='dialog']/*[local-name()='div' and @class='isgrP']")

        path = "//*[local-name()='a' and @class='FPmhX notranslate  _0imsa ']"
        self.name = self.follower.getListAttributes(path)

        self.web_driver.find_element_by_xpath("/html/body/div[4]/div/div[1]/div/div[2]/button").click()
        self.antiBan.randomSleep()
        self.unfollow()
        
    def unfollow(self):
        #Check unfollowers
        self.web_driver.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/ul/li[3]/a/span").click()
        self.antiBan.randomSleep()

        ##Scroll through list
        self.follower.scrollList("//*[local-name()='div' and @role='dialog']/*[local-name()='div' and @class='isgrP']")

        path2 = "//*[local-name()='a' and @class='FPmhX notranslate  _0imsa ']"
        self.name2 = self.follower.getListAttributes(path2)

        self.followerDict()

        self.web_driver.find_element_by_xpath("/html/body/div[4]/div/div[1]/div/div[2]/button").click()
        self.antiBan.randomSleep()

    def followerDict(self):
        ##Second Permanent JSON for Followers##
        self.followersData = {}
        ##Register Time##
        lastTimeRun = self.bot.timeOfRun
        ##Append the data to our dictonary##
        self.follower.append(({"DateRunning" : lastTimeRun,"Followers" : self.name}),self.bot.username,self.followersData)
        self.follower.append(({"DateRunning" : lastTimeRun,"Following" : self.name2}),self.bot.username,self.followersData)
        self.follower.writeInfo("followersInfo","w",self.followersData)


