
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
        sleep(5)
        self.web_driver.find_element_by_name("username").send_keys(username)
        self.web_driver.find_element_by_name("password").send_keys(pw)
        self.web_driver.find_element_by_xpath("/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div[4]/button/div")\
            .click()
        sleep(2)
        self.web_driver.find_element_by_xpath("/html/body/div[4]/div/div/div[3]/button[2]").click()
        used_hs = self.hashtag()  
        print(used_hs)
        used_comment = self.comment(used_hs)
        print(used_comment)

    def hashtag(self):
        """
            Will choose randomly a Hashtag and rerturn its value
        """
        choose = random.randint(0,len(poss))
        return poss[choose]
    
    def comment (self,hs):
        """
            Will choose a comment depending on the hashtag that was opened
        """
        comment = comm[hs]
        num = random.randint(0,len(comment))
        comment = comment[num]
        return comment


Bot = InstaComment('mexicansombreroless','mannheimzittau')