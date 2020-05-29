from InstagramAPI import InstagramAPI
import pandas as pd
from time import sleep


class InstaBot:

    def __init__(self):
        self.api = InstagramAPI("mexicansombreroless", "mannheimzittau")

    def get_likes_list(self):
        has_more_posts = True
        max_id=""
        users_list = []
        api=self.api
        api.login()
        i = 0
        api.getSelfUsernameInfo()
        result_1 = api.LastJson
        media_acount = result_1['user']['media_count'] #Get user posts
        print(media_acount)
        ##username_id = result['user']['pk'] # Get user ID
        while has_more_posts:
            api.getSelfUserFeed(maxid=max_id)
            if api.LastJson['more_available'] is not True:
                has_more_posts = False #stop condition
                print ("stopped")    
            result_2 = api.LastJson
            max_id = api.LastJson.get('next_max_id','')
            if 'items' in result_2.keys():
                for item in result_2['items']:
                    media_id = item['id']
                    api.getMediaLikers(media_id) # Get users who liked
                    users = api.LastJson['users']
                    for user in users: # Push users to list
                        users_list.append({'username':user['username']})
                    print(users_list)
                    i+=1
                    print(str(i) + '\n')
                sleep(3)
def main ():
    Ins = InstaBot()
    Ins.get_likes_list()

if __name__ == "__main__":
    main()