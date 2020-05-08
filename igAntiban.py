'''
    Developers: Yael Abelardo Martínez, Oscar Herrera & Hugo Armando Zepeda Ruiz
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


class igAntiban(igStart):
    """
        Class that avoids banning
    """
    def __init__(self):
        pass
    
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
        self.exceptionHandler("/html/body/div[1]/section/main/section/div[1]/div/div/div/div[1]/button")
        #logger.info("start checking histories, expected return at: {} minutes".format(localtime()[4] + 5))
        sleep(300)
        self.exceptionHandler("/html/body/div[1]/section/div/div/section/div[2]/button[3]") 
        
    def randomSleep(self):
        """
            Will generate a random sleep time
            
            -> time : random int 1-5 seconds
        """
        return random.choice(range(1,6))