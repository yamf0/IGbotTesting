
import os
from time import sleep
from selenium import webdriver
from selenium.webdriver.common import keys

#Find PATH to current Directory (to find the dirver)
path_driver = os.path.dirname(os.path.realpath(__file__))
print (path_driver)

class InstaComment ():
    def __init__(self, username, pw):
        self.web_driver = webdriver.Chrome(path_driver + "\chromedriver\chromedriver.exe" )
        self.web_driver.get("https://instagram.com")
        sleep(5)
        self.web_driver.find_element_by_name("username").send_keys(username)
        self.web_driver.find_element_by_name("password").send_keys(pw)
        self.web_driver.find_element_by_xpath("/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div[4]/button/div")\
            .click()
        


Bot = InstaComment('mexicansombreroless','mannheimzittau')