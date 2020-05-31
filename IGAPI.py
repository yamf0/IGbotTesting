from InstagramAPI import InstagramAPI
import pandas as pd
from time import sleep
import json


profile = {}

class igAPI:

    def __init__(self):
        self.api = InstagramAPI("mexicansombreroless", "mannheimzittau")

    def getLikesList(self):
        hasMorePosts = True
        maxId=""
        api=self.api
        api.login()
        i = 0
        api.getSelfUsernameInfo()
        result = api.LastJson
        media_acount = result['user']['media_count'] #Get user posts
        print(media_acount)
        listofLists = [[] for i in range(media_acount+1)]
        ##username_id = result['user']['pk'] # Get user ID
        while hasMorePosts:
            api.getSelfUserFeed(maxid=maxId)
            if api.LastJson['more_available'] is not True:
                hasMorePosts = False #stop condition
                print ("stopped")    
            result1 = api.LastJson
            maxId = api.LastJson.get('next_max_id','')
            if 'items' in result1.keys():
                for item in result1['items']:
                    mediaId = item['id']
                    api.getMediaLikers(mediaId) # Get users who liked
                    users = api.LastJson['users']
                    i+=1
                    for user in users: # Push users to list
                        listofLists[i].append(user['username'])
                    self.append(listofLists[i],i,profile)
                sleep(3)
        self.writeInfo('PhotosFeed','a',profile)
    def appendList(self):
        return []

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

    
    def writeInfo(self, jsonPath, action, dictionary):
        """
                Write info to JSON FILE 

                ->jsonPath:  json file name
                
                ->action: w for overwirte a for append
        """
        jsonPath = jsonPath + ".json"
        with open (jsonPath, action, encoding='utf8') as file:
            json.dump(dictionary, file, sort_keys=True, ensure_ascii=False, indent=4, separators=(',',':'))

def main ():
    Ins = igAPI()
    Ins.getLikesList()

if __name__ == "__main__":
    main()