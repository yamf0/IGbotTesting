'''
    Developers: Yael Abelardo Martínez, Oscar Herrera & Hugo Armando Zepeda Ruiz
    Created: 03,2020
    Purpose: Automation of interaction in Instagram from Mexican Sombrero & -less, Testing
    Copyright
'''
from igStart import igStart
from igAntiban import igAntiban
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains


from time import sleep
import json
import os
import random


#Lists of hashstags & comments.
poss = ["#stayandwander", "#europe_perfection","#landscape", "#travel", "#travelphotography", "#travelling","#wanderlust",\
"#wanderlusting", "#wanderluster", "#europetravel","#sunset","#traveltheworld", "#travellingthroughtheworld"]
comm = ["what an amazing pic!", "Perfection", "We loved it", "Keep up the Great Photos", "This place is amazing",\
    "This is amazing", "Congrats for the great photo", "What a Pic!!!", "That is great!",\
    "Wow that pic!", "This place is amazing", "Keep up the great photos", "Amazing",\
    "Perfect!", "Amazing", "That is nice!", "Great",\
    "What a destination", "That is amazing", "Great!!!",\
    "Wish to be there","Cannot wait to be there","Nice photo",\
    "Really love this part of the day",\
    "Wish to be there","Cannot wait to be there","Maybe this is the sombrero next destination",\
    "WOW", "This is Perfect", "Congrats for the great Photo", "Simply Beautiful",\
    "Amazing pic!!", "Congrats, this is Great!", "That seems amazing!", "Great Pic",\
    "Pff that is amazing", "Keep up the great Photos", "We loved it", "That is incredible",\
    "Great Photo!", "We loved it!",\
    "Amazing Place!", "that is Amazing!", "WOW", "Perfect!"]

    
class jsonConstructor (igStart):
    """
        Class that handles the construction of all required JSON's 

        functions:

        ->getAttributes:

        ->append

        ->writeAppend
        
    """

    def __init__(self,web_driver):
        self.web_driver = web_driver
        self.antiBan = igAntiban(web_driver)

    def getAttributes(self, path, attribute):
        """
            Get information required (Generic)

            Variables:

            -> path: xPath to access to 

            -> attribute: Which attribute you want to get
        """
        try:
            if (attribute == 'text'):
                return self.web_driver.find_element_by_xpath(path).text
            else:
                return self.web_driver.find_element_by_xpath(path).get_attribute(attribute)
        except:
            print("element not found")
            return None


    def append (self, data, key, dictAppend):
        """
            Append Data to Dictionary

            ->data: data inside key (can be a dictionary)

            ->key: key for the data to be saved

            ->dictAppend:  in which dictionary will the data be saved
        """
        if (key in dictAppend):
            dictAppend[key].update(data)
        else:
            dictAppend.update({key : data})
        return dictAppend

    def getDict (self, key, dictionary):
        """
            Will retrun a new dictionary of the key within a dictionary
            
            ->key: key to be searched

            ->dictionary: dictionary to search within

        """
        if (key in dictionary):
            newDict = dictionary[key]
            return newDict
        for k, val in dictionary.items():
            if (isinstance(val, dict) and val == key):
                return self.getDict(key, dictionary)


    def writeInfo(self, jsonPath, action, dictionary):
        """
                Write info to JSON FILE 

                ->jsonPath:  json file name
                
                ->action: w for overwirte a for append
        """
        jsonPath = jsonPath + ".json"
        with open (jsonPath, action, encoding='utf8') as file:
            json.dump(dictionary, file, sort_keys=True, ensure_ascii=False, indent=4, separators=(',',':'))
    
    def loadInfo (self, jsonPath):
        """
            Open a JSON file to import dict

            return dict
        """
        with open(jsonPath, "r", encoding="utf8") as file:
            dictionary = json.load(file)
            return dictionary

    def getListAttributes (self, path):
        """
            Get all hashtags used in a photo

            -> profile: username of the person uploading the photo
        """
        attributeList = [element.text for element in self.web_driver.find_elements_by_xpath(path)]
        
        return attributeList

    def scrollList(self, path):
        """
            Scroll a List until the end

            varibales:
            -> path: Xpath to the list
        """
        last_ht, ht = 0, 1
        while last_ht != ht:
            last_ht = ht
            sleep(2)
            ht = self.web_driver.execute_script("""
            arguments[0].scrollTo(0, arguments[0].scrollHeight);
            return arguments[0].scrollHeight;
            """, self.web_driver.find_element_by_xpath(path))
            print("SCROLLING")

    def fastCheck(self):
        """
            Hover over fotos to retrieve Likes and Comments
            
            return
                -> likes: list of list with likes and commets from X first photos 
                -> elements: list of webdriver elements where photos are
        """

        #TODO se tiene que arreglar este codigo para que no hoverie por todas las fotos en cada loop
        self.action = ActionChains(self.web_driver)
        likes = []
        sleep(3)
        elements = []
        ##hover over Photos to get numbers##
        elements = self.web_driver.find_elements_by_xpath("//div[@class = 'eLAPa']")
        
        while True:
            try:
                self.web_driver.execute_script("arguments[0].click();", elements[0])
                self.exceptionHandler("//div[ contains(@class, 'Igw0E ')]/button[@class = 'wpO6b ']")
                break
            except StaleElementReferenceException as Ex:
                element = self.web_driver.find_element_by_xpath("//div[@class = 'eLAPa']")

        


        print(len(elements) % 10 + 10)
        for i in range(len(elements) % 10 + 10):
            
            self.action.move_to_element(elements[i]).perform()
            ##Find Elements that has a sibling span, focus on the preceding one##
            likes.append(self.getListAttributes("//ul[@class='Ln-UN']//span/preceding-sibling::span"))
            likes[i] = self.convertToInt(likes[i])
            
            ##Save original Index##
            likes[i].append(i)
        return likes, elements
    
    def convertToInt(self, string):
        """
            Convert a str to int
            Variables
                ->string : list or string to convert (list must all be strings)

            return
                -> num : converted int
        """
        if isinstance(string, str):
            string = string.replace(",","")
            string = string.replace(".","")
            string = string.replace("k","000")
            num = int(string)
        else:
            for i in range(len(string)):
                string[i] = self.convertToInt(string[i])
            num = string
        return num
        

    def hasXpath(self, path):

        try:
            self.web_driver.find_element_by_xpath(path)
            return True
        except:
            return False

    def generateHashtag(self):
        """
            Will choose randomly a Hashtag and return its value
        """
        choose = random.randint(0,len(poss)-1)
        hashtag = poss[choose]
        poss.pop(choose)
        return hashtag
    
    def generateComment (self):
        """
            Will choose a comment depending on the hashtag that was opened
        """
        num = random.randint(0,len(comm)-1)
        comment = comm[num]
        return comment