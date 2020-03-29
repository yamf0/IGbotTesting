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
import random

#Find PATH to current Directory (to find the driver)
path_driver = os.path.dirname(os.path.realpath(__file__))
print (path_driver)

poss = ["#stayandwander", "#europe_perfection","#landscape", "#travel"]
comm = {
    "#stayandwander" : ["what an amazing pic!", "Perfection", "We loved it"],
    "#europe_perfection": ["This is amazing", "Congrats for the great photo", "What a Pic!!!"],
    "#landscape": ["Wow that pic!", "This place is amazing", "Keep up the great photos"],
    "#travel": ["Perfect!", "Amazing", "That is nice!"],
    "#travelphotography": ["What a destination", "That is amazing", "Great!!!"],
    "#travelling":["Wish to be there","Cannot wait to be there","Maybe this is the sombrero next destination"]
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
        for i in range (10):
            self.iterate_hastag()
        self.web_driver.quit()

    def iterate_hastag(self):
        """
            Will iterate through the hastags 
        """
        ##Checks for the Hashtag entry
        used_hs = self.hashtag()  
        used_comment = self.comment(used_hs)
        ##Search the Hashtag
        self.web_driver.find_element_by_xpath("/html/body/div[1]/section/nav/div[2]/div/div/div[2]/input").send_keys(used_hs)
        sleep(3)

        self.web_driver.find_element_by_xpath("/html/body/div[1]/section/nav/div[2]/div/div/div[2]/div[2]/div[2]/div/a[1]/div").click()
        sleep(3)
        
        self.iterate_photos()
        
    def iterate_photos(self):
        """
            Will do the iteration through the photos 
        """
        #Iterate through photos
        path_init = "/html/body/div[1]/section/main/article/div[1]/div/div/"
        path_end = "/a/div/div[2]"
        for i in range(1,4):
            path_i = "div["+ str(i) + "]"
            for j in range(1,4):
                path_j = "/div[" + str(j) + "]"
                #click the image
                real_path=path_init+path_i+path_j+path_end
                self.web_driver.find_element_by_xpath(real_path).click()
                sleep(3)

                ##Search previous Like
                if (self.has_like()):
                    self.web_driver.find_element_by_xpath("/html/body/div[4]/div[3]/button").click()
                    sleep(1)
                    return
                
                #Click Like
                self.web_driver.find_element_by_xpath("/html/body/div[4]/div[2]/div/article/div[2]/section[1]/span[1]/button").click()
                sleep(2)
        
                self.web_driver.find_element_by_xpath("/html/body/div[4]/div[2]/div/article/div[2]/section[1]/span[2]/button").click()
                self.web_driver.find_element_by_xpath("/html/body/div[4]/div[2]/div/article/div[2]/section[3]/div/form/textarea").send_keys(used_comment)
                self.web_driver.find_element_by_xpath("/html/body/div[4]/div[2]/div/article/div[2]/section[3]/div/form/button").click()
                sleep(2)
                
                ##This is the close Button
                self.web_driver.find_element_by_xpath("/html/body/div[4]/div[3]/button").click()
                sleep(2)

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

    def has_like (self):
        """
            Will see if the chosen photo has already a like 
        """
        fill = self.web_driver.find_element_by_xpath("//*[local-name()='span' and @class='fr66n']/*[local-name()='button']/*[local-name()='svg']").get_attribute("fill")
        print(fill)
        if fill == "#ed4956":
            return True
        else:
            return False


def main ():
    
    Bot = InstaComment('mexicansombreroless','mannheimzittau')
    

if __name__ == "__main__":
    main()