
import os
from time import sleep
from selenium import webdriver
from selenium.webdriver.common import keys
import random

#Find PATH to current Directory (to find the dirver)
path_driver = os.path.dirname(os.path.realpath(__file__))
print (path_driver)

poss = ["#stayandwander", "#europe_perfection","#landscape", "#travel", "#travelphotography"]
comm = {
    "#stayandwander" : ["what an amazing pic!", "Perfection", "We loved it"],
    "#europe_perfection": ["This is amazing", "Congrats for the great photo", "What a Pic!!!"],
    "#landscape": ["Wow that pic!", "This place is amazing", "Keep up the great photos"],
    "#travel": ["Perfect!", "Amazing", "That is nice!"],
    "#travelphotography": ["What a destination", "That is amazing", "Great!!!"]
}

class InstaComment ():
    def __init__(self, username, pw):
        self.web_driver = webdriver.Chrome(path_driver + "\chromedriver\chromedriver.exe" )
        self.web_driver.get("https://instagram.com")
        sleep(2)
        self.web_driver.find_element_by_name("username").send_keys(username)
        self.web_driver.find_element_by_name("password").send_keys(pw)
        self.web_driver.find_element_by_xpath("/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div[4]/button/div").click()
        sleep(3)
        self.web_driver.find_element_by_xpath("/html/body/div[4]/div/div/div[3]/button[2]").click()

        used_hs = self.hashtag()  
        used_comment = self.comment(used_hs)

        self.web_driver.find_element_by_xpath("/html/body/div[1]/section/nav/div[2]/div/div/div[2]/input").send_keys(used_hs)
        sleep(1)
        self.web_driver.find_element_by_xpath("/html/body/div[1]/section/nav/div[2]/div/div/div[2]/div[2]/div[2]/div/a[1]/div").click()
        sleep(3)
        self.web_driver.find_element_by_xpath("/html/body/div[1]/section/main/article/div[1]/div/div/div[1]/div[1]/a/div/div[2]").click()
        sleep(3)
        self.web_driver.find_element_by_xpath("/html/body/div[4]/div[2]/div/article/div[2]/section[1]/span[1]/button").click()
        sleep(1)
        self.web_driver.find_element_by_xpath("/html/body/div[4]/div[2]/div/article/div[2]/section[1]/span[2]/button").click()
        self.web_driver.find_element_by_xpath("/html/body/div[4]/div[2]/div/article/div[2]/section[3]/div/form/textarea").send_keys(used_comment)
        #self.web_driver.find_element_by_tag_name("textarea").send_keys(used_comment)
        self.web_driver.find_element_by_xpath("/html/body/div[4]/div[2]/div/article/div[2]/section[3]/div/form/button").click()

    def hashtag(self):
        """
            Will choose randomly a Hashtag and rerturn its value
        """
        choose = random.randint(0,len(poss)-1)
        return poss[choose]
    
    def comment (self,hs):
        """
            Will choose a comment depending on the hashtag that was opened
        """
        comment = comm[hs]
        num = random.randint(0,len(comment)-1)
        comment = comment[num]
        return comment

Bot = InstaComment('mexicansombreroless','mannheimzittau')