import os
import json
from pathlib import Path
#Library to control the timings of execution
from time import sleep
import threading
from concurrent import futures
#Principal library for web scrapping
from selenium import webdriver
from selenium.webdriver.common import keys
from selenium.webdriver.remote.command import Command
from selenium.common.exceptions import NoSuchElementException


username = "travelandphoto2020"
pw = "mannheimzittau"
path_driver = os.path.dirname(os.path.realpath(__file__))
path_driver = os.path.split(os.path.abspath(path_driver))[0]
print(path_driver)

resource_path = os.path.split(os.path.abspath(path_driver))[0]
resource_path = os.path.join(resource_path, "resources")

web_driver =  webdriver.Chrome(path_driver + "\chromedriver\chromedriver.exe" )
web_driver.get("https://instagram.com")


sleep(2)
web_driver.find_element_by_name("username").send_keys(username)
sleep(1)
web_driver.find_element_by_name("password").send_keys(pw)
sleep (1)
web_driver.find_element_by_xpath("//button[contains(@class, 'sqdOP') and @type='submit']").click()
sleep(2)
web_driver.find_element_by_xpath("//div//button[contains(text( ), 'no')]").click()
sleep(2)
web_driver.find_element_by_xpath("//div//button[contains(text( ), 'no')]").click()

while(True):
    title = web_driver.title
    photFlag = False
    try:
        web_driver.find_element_by_xpath("//body//div[contains(@class, '_2dDPU')]")
        photFlag = True
    except:
        pass
    if photFlag:
        print("You are in Photo")
    elif "@" in title:
        print("In Profile")
        title = title.split("@")[1]
        title = title.split(")")[0]
        print(title)
    elif "Instagram" in title:
        chunks = list(title.split(" "))
        print(chunks)
        if len(chunks) == 1:
            title = chunks[0]
            print("In HomePage")
        elif "#" in title:
            title = title.split("#")[1]
            title = title.split(" ")[0]
            print(title)
        else:
            title = chunks[0]
            print("in Histories")
    

    sleep(1)