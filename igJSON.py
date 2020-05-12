'''
    Developers: Yael Abelardo Martínez, Oscar Herrera & Hugo Armando Zepeda Ruiz
    Created: 03,2020
    Purpose: Automation of interaction in Instagram from Mexican Sombrero & -less, Testing
    Copyright
'''
from igStart import igStart
from igAntiban import igAntiban

from time import sleep
import json
import os

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
        self.antiBan = igAntiban()

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
        with open (jsonPath, action) as file:
            json.dump(dictionary, file, sort_keys=True, indent=4, separators=(',',':'))
    
    def loadInfo (self, jsonPath):
        """
            Open a JSON file to import dict

            return dict
        """
        with open(jsonPath, "r") as file:
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

