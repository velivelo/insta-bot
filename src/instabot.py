

import time
import random
import requests
from fake_useragent import UserAgent
import re
import json
from functools import wraps
import os


class InstaBot ():

    urls = {
        "default": "https://www.instagram.com/",
        "login": "https://www.instagram.com/accounts/login/ajax/",
        "follow": "https://www.instagram.com/web/friendships/{}/follow/", # user_id
        "unfollow": "https://www.instagram.com/web/friendships/{}/unfollow/", # user_id
        "user_details": "https://www.instagram.com/{}/", # username
        "api_user_details": "https://i.instagram.com/api/v1/users/{}/info/", # user_id
        "explore": "https://www.instagram.com/explore/tags/{}/?__a=1", # tag
        "like": "https://www.instagram.com/web/likes/{}/like/", # media_id
        "unlike": "https://www.instagram.com/web/likes/{}/unlike/", # media_id
        "comment": "https://www.instagram.com/web/comments/{}/add/",  # media_id
        "remove_comment": "https://www.instagram.com/web/comments/{}/delete/{}/", # media_id, comment_id
        "media": "https://www.instagram.com/p/{}/", # media shortcode
    }

    def __init__ (self, username, password):
        self.username, self.password = username, password

        self.s = requests.Session()
        self.logged = False

    def require_loggin (func):
        @wraps(func)
        def wrapper (*args, **kwargs):
            if not args[0].logged:
                raise Exception('Method "{}" require the bot to be logged'.format(func.__name__))
            return func(*args, **kwargs)
        return wrapper 

    def login (self):
        """Loggin to Instagram"""
        self.s.headers.update({
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Host': 'www.instagram.com',
            'Origin': 'https://www.instagram.com',
            'Referer': 'https://www.instagram.com/',
            'User-Agent': UserAgent().random,
        })
    
        r = self.s.get(self.urls["default"], timeout= 5)
        self.s.headers.update({'X-CSRFToken': r.cookies['csrftoken']})
        time.sleep(random.uniform(1, 2))

        r = self.s.post(self.urls["login"], data= {
                                                "username": self.username,
                                                "password": self.password,
                                            }, timeout= 5)
        self.s.headers.update({'X-CSRFToken': r.cookies['csrftoken']})
        self.s.cookies['ig_vw'] = '1536'
        self.s.cookies['ig_pr'] = '1.25'
        self.s.cookies['ig_vh'] = '772'
        self.s.cookies['ig_or'] = 'landscape-primary'
        if r.status_code != 200:
            raise Exception("Login error. Connection Error.")
        time.sleep(random.uniform(1, 2))

        r = self.s.get(self.urls["default"], timeout= 5)
        if r.text.find(self.username) < 0:
            raise Exception("Login error. Check login data.")
        self.logged = True

    @require_loggin
    def follow (self, user_id):
        """Follow an user by his id"""
        r = self.s.post(self.urls["follow"].format(user_id), timeout= 5)
        r.raise_for_status()
        return r

    @require_loggin
    def unfollow (self, user_id):
        """Unfollow an user by his id"""
        r = self.s.post(self.urls["unfollow"].format(user_id), timeout= 5)
        r.raise_for_status()
        return r

    @require_loggin
    def like (self, media_id):
        """Like a media by its id"""
        r = self.s.post(self.urls["like"].format(media_id), timeout= 5)
        r.raise_for_status()
    
    @require_loggin
    def unlike (self, media_id):
        """Unlike a media by its id"""
        r = self.s.post(self.urls["unlike"].format(media_id), timeout= 5)
        r.raise_for_status()

    @require_loggin
    def comment (self, media_id, text):
        """Post a comment on a media by its id and return the comment id"""
        r = self.s.post(self.urls["comment"].format(media_id), data= {
                                                                   "comment_text": text
                                                               }, timeout= 5)
        r.raise_for_status()
        return r.json()["id"]

    @require_loggin
    def removeComment (self, media_id, comment_id):
        """Remove a comment from a media by its id"""
        r = self.s.post(self.urls["remove_comment"].format(media_id, comment_id), timeout= 5)
        r.raise_for_status()

    def getUserDetails (self, username):
        """Return an user details into a dictionary from his username"""
        r = self.s.get(self.urls["user_details"].format(username), timeout= 5)
        r.raise_for_status()
        full_details = json.loads(re.search(r"window\._sharedData = (.+);</script>", r.text).group(1))
        return full_details["entry_data"]["ProfilePage"][0]["graphql"]["user"]

    def usernameToUserId (self, username):
        """From an username to an user id"""
        return self.getUserDetails(username)["id"]
    
    def userIdToUsername (self, user_id):
        """From an user id to an username"""
        r = requests.get(self.urls["api_user_details"].format(user_id), timeout= 5)
        return r.json()["user"]["username"]

    def explore (self, tag):
        """Return the most recent posted medias containing the tag in argument"""
        r = self.s.get(self.urls["explore"].format(tag), timeout= 5)
        if r.status_code != 200: 
            return [] # no madia with this tag
        return [media["node"] for media in r.json()["graphql"]["hashtag"]["edge_hashtag_to_media"]["edges"]]

    def downloadMedia (self, media_shortcode):
        """Download a media by its shortcode (not videos)"""
        r = self.s.get(self.urls["media"].format(media_shortcode), timeout= 5)
        full_details = json.loads(re.search(r"window\._sharedData = (.+);</script>", r.text).group(1))
        media_url = full_details["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"]["display_url"]
        img_data = requests.get(media_url, timeout= 10).content
        os.makedirs("downloads", exist_ok= True)
        with open("downloads/{}.jpg".format(media_shortcode), "wb") as handler:
            handler.write(img_data)


if __name__ == "__main__":
    pass

