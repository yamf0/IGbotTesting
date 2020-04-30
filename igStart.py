'''
    Developers: Yael Abelardo Martínez & Hugo Armando Zepeda Ruiz
    Created: 03,2020
    Purpose: Automation of interaction in Instagram from Mexican Sombrero & -less. 
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
#Library to print personalize message. Allows more control in message control 
import logging
from logging import StreamHandler


##path to chrome driver##
path_driver = os.path.dirname(os.path.realpath(__file__))
print (path_driver)

class igStart():
    """
        Class that starts Chrome Instance and opens IG
        Functions:
    """
    def __init__(self, username, pw ):
    
        self.username = username
        self.pw = pw
    
    def openAccount(self):
        """
        """
        ##Open chrome
        self.web_driver = webdriver.Chrome(path_driver + "\chromedriver\chromedriver.exe" )
        self.web_driver.get("https://instagram.com")
        sleep(2)
        ##Input account and Pw
        self.web_driver.find_element_by_name("username").send_keys(self.username)
        sleep(1)
        self.web_driver.find_element_by_name("password").send_keys(self.pw)
        sleep (3)
        self.web_driver.find_element_by_xpath("/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div[4]/button/div").click()
        sleep(3)

        ##click Accept
        self.Exception_Handler("/html/body/div[4]/div/div/div[3]/button[2]")
        sleep(3)

        ##We are in

    def Exception_Handler (self,xpath):
        """
            Method will try to click Xpath, if not find will wait untill it is found (Solves Bad internet Issue)
        """
        while (True):
            try:
                self.web_driver.find_element_by_xpath(xpath).click()
                break

            except Exception as ex:
                sleep(3)
                continue

def main ():
    #Little GUI
    var = input("Running Mexican(1) // test code in Mexico(2) // test code in Germany (3) ")
    if(var == '1'):
        var_1 = input("Running Mexican(1) or Mexicanless(2)?")
        if (var_1 == '1'):
            Bot = igStart('mexicansombrero','YaelHugoPato')
            Bot.openAccount()
        elif (var_1 == '2'): 
            Bot = igStart('mexicansombreroless','mannheimzittau')
            Bot.openAccount()
        else:
            print("Stop playing around! Work please")
    elif(var == '2'):
        Bot = igStart('photoandtravel2020','mannheimzittau')
        Bot.openAccount()
    elif(var == '3'):
        Bot = igStart('travelandphoto2020','mannheimzittau')
        Bot.openAccount()      
    else: 
        account = input("Please give the account username")
        password = input("Please give the password")
        print("You entered: " + account)
        print("You entered: " + password)
        var_2 = input("Is the data true(1)? Any other number for no.")
        if(var_2 == '1'):
            Bot = igStart(account,password)
            Bot.openAccount()



if __name__ == "__main__":
    main()
