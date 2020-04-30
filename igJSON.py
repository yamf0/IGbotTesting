from igStart import igStart
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

    def __init__(self):
        ##construct General Dictionary##
        self.dictionary = {}


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

        dictAppend.update({key : data})
    

    def writeInfo(self, jsonPath, action):
        """
                Write info to JSON FILE 

                ->jsonPath:  jason file name
                
                ->action: w for overwirte a for append
        """
        jsonPath = jsonPath + ".json"
        with open (jsonPath, action) as file:
            json.dump(self.photo_data, file, sort_keys=True, indent=4, separators=(',',':'))

    



