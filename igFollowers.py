from InstagramAPI import InstagramAPI
import pandas as pd
from time import sleep
import json

usersFollower = []
usersFollowing = []

class igFollowers:

    def __init__(self):
        self.api = InstagramAPI("mexicansombreroless", "mannheimzittau")

    def getFFList(self):
        api=self.api
        api.login()
        api.getSelfUserFollowers()
        result = api.LastJson
        for user in result['users']:
            usersFollower.append(user['username'])

        api.getSelfUsersFollowing()
        result1 = api.LastJson
        for user in result1['users']:
            usersFollowing.append(user['username'])
    
    def writeInfo(self):
        jsonPath =  "FollowersList.json"
        jsonPath1 = "FollowingList.json"
        with open(jsonPath,'w',encoding='utf8') as file:
            json.dump(usersFollower,file)
        with open(jsonPath1,'w',encoding='utf8') as file:
            json.dump(usersFollowing,file)

def main ():
    Ins = igFollowers()
    Ins.getFFList()
    Ins.writeInfo()

if __name__ == "__main__":
    main()