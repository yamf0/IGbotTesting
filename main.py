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

<<<<<<< HEAD
poss = ["#stayandwander", "#europe_perfection","#landscape", "#travel","#travelphotography","#travelling","#sunset"]
=======
poss = ["#stayandwander", "#europe_perfection","#landscape", "#travel", "#travelphotography", "#travelling"]
>>>>>>> 8751377e57a215e9a1b3f278561540575f0aa286
comm = {
    "#stayandwander" : ["what an amazing pic!", "Perfection", "We loved it"],
    "#europe_perfection": ["This is amazing", "Congrats for the great photo", "What a Pic!!!"],
    "#landscape": ["Wow that pic!", "This place is amazing", "Keep up the great photos"],
    "#travel": ["Perfect!", "Amazing", "That is nice!"],
    "#travelphotography": ["What a destination", "That is amazing", "Great!!!"],
    "#travelling":["Wish to be there","Cannot wait to be there","Maybe this is the sombrero next destination","Nice photo"]
    "#sunset":["Really love this part of the day"]
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
            self.iterate_hastag(self.hashtag())
        self.web_driver.quit()

    def iterate_hastag(self,hashtag_global):
        """
            Will iterate through the hastags 
        """
<<<<<<< HEAD
        ##Search the Hashtag
        self.web_driver.find_element_by_xpath("/html/body/div[1]/section/nav/div[2]/div/div/div[2]/input").send_keys(hashtag_global)
=======
        ##Checks for the Hashtag entry
        self.used_hs = self.hashtag()  

        ##Search the Hashtag
        self.web_driver.find_element_by_xpath("/html/body/div[1]/section/nav/div[2]/div/div/div[2]/input").send_keys(self.used_hs)
>>>>>>> 8751377e57a215e9a1b3f278561540575f0aa286
        sleep(3)

        self.web_driver.find_element_by_xpath("/html/body/div[1]/section/nav/div[2]/div/div/div[2]/div[2]/div[2]/div/a[1]").click()
        
        sleep(3)
        
<<<<<<< HEAD
        self.iterate_photos(hashtag_global)
        
    def iterate_photos(self,hashtag_global_photos):
=======
        self.iterate_photos("top")
        self.iterate_photos("recent")
        
    def iterate_photos(self, section):
>>>>>>> 8751377e57a215e9a1b3f278561540575f0aa286
        """
            Will do the iteration through the photos 
        """
        #Check if section is over
        if section == "top" :
            path_init = "/html/body/div[1]/section/main/article/div[1]/div/div/"    
        else:
            path_init = "/html/body/div[1]/section/main/article/div[2]/div/"    
        path_end = "/a/div/div[2]"
        for i in range(1,4):
            path_i = "div["+ str(i) + "]"
            for j in range(1,4):
                path_j = "/div[" + str(j) + "]"

                #Generate the Comment for that point
                self.used_comment = self.comment(self.used_hs)
                #click the image
                real_path=path_init+path_i+path_j+path_end
                self.web_driver.find_element_by_xpath(real_path).click()
                sleep(5)

                ##Search previous Like
                if (self.has_like()):
                    self.web_driver.find_element_by_xpath("/html/body/div[4]/div[3]/button").click()
                    sleep(1)
                    continue
                
                #Click Like
                self.web_driver.find_element_by_xpath("/html/body/div[4]/div[2]/div/article/div[2]/section[1]/span[1]/button").click()
                sleep(2)
        
                self.web_driver.find_element_by_xpath("/html/body/div[4]/div[2]/div/article/div[2]/section[1]/span[2]/button").click()
<<<<<<< HEAD
                self.web_driver.find_element_by_xpath("/html/body/div[4]/div[2]/div/article/div[2]/section[3]/div/form/textarea").send_keys(self.comment(hashtag_global_photos))
=======
                self.web_driver.find_element_by_xpath("/html/body/div[4]/div[2]/div/article/div[2]/section[3]/div/form/textarea").send_keys(self.used_comment)
                sleep(2)
>>>>>>> 8751377e57a215e9a1b3f278561540575f0aa286
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