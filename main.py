
import os
from selenium import webdriver

#Find PATH to current Directory (to find the dirver)
path_driver = os.path.dirname(os.path.realpath(__file__))
print (path_driver)

class InstaComment ():
    def __init__(self):
        self.web_driver = webdriver.Chrome(path_driver + "\chromedriver\chromedriver.exe" )
        self.web_driver.get("https://instagram.com")

InstaComment()