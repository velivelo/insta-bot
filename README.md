# insta-bot
An Insagram bot made with Python and independant from the Instagram API.

## The bot can

src/instabot.py > From help(InstaBot) :
```
class InstaBot(builtins.object)
 |  Methods defined here:
 |  
 |  __init__(self, username, password)
 |      Initialize self.  See help(type(self)) for accurate signature.
 |  
 |  comment(self, media_id, text)
 |      Post a comment on a media by its id and return the comment id
 |  
 |  downloadMedia(self, media_shortcode)
 |      Download a media by its shortcode (not videos)
 |  
 |  explore(self, tag)
 |      Return the most recent posted medias containing the tag in argument
 |  
 |  follow(self, user_id)
 |      Follow an user by his id
 |  
 |  getUserDetails(self, username)
 |      Return an user details into a dictionary from his username
 |  
 |  like(self, media_id)
 |      Like a media by its id
 |  
 |  login(self)
 |      Loggin to Instagram
 |  
 |  removeComment(self, media_id, comment_id)
 |      Remove a comment from a media by its id
 |  
 |  require_loggin(func)
 |  
 |  unfollow(self, user_id)
 |      Unfollow an user by his id
 |  
 |  unlike(self, media_id)
 |      Unlike a media by its id
 |  
 |  userIdToUsername(self, user_id)
 |      From an user id to an username
 |  
 |  usernameToUserId(self, username)
 |      From an username to an user id
```
It also has an autoMod function. src/automod.py > From help(InstaBot.autoMod) :
```
autoMod(self, follow_duration=300, time_gap=60, tags='default', unfollow_if_followed_back=True, unfollow_already_followed=True, follow=True, like=False, max_stack_size=5, videos=False, max_likes_for_like=20, max_followers_for_follow=500, only_medias_posted_before_timestamp=600, comment=False, comments=(('Super', 'Beautiful', 'Great'), ('post', 'picture'), ('!', '')), users_blacklist='instagram')
    follow_duration= 300, # time before unfollowing (0 for infinite)
    time_gap= 60, # time between medias treatment
    tags= ("default"), # media tags to explore
    unfollow_if_followed_back= True, # unfollow even if the user has followed back
    unfollow_already_followed= True, # the bot unfollow people already followed 
    follow= True, # follow medias owners
    like= False, # like medias 
    max_stack_size= 5, # maximum number of medias treated for a tag before recursion
    videos= False, # take care of videos
    max_likes_for_like= 20, # max likes a media can have to be liked
    max_followers_for_follow= 500, # max followers an user can have to be followed
    only_medias_posted_before_timestamp= 600, # treat only a media if posted before timestamp
    comment= False, # comment the media
    comments= (("Super", "Beautiful", "Great"), ("post", "picture"), ("!", "")), # list of comments
    users_blacklist= ("instagram"), # users blacklisted
```

## Installation

1. Download and install python3+ on your computer
2. `git clone` this repo or download as a ZIP and extract
3. Install dependencies `pip install -r requirements.txt`

## Warnings !

These are the approximately Instagram limits. Be worry of respecting them or you'll get a bunch of 403 HTTP errors and might get banned !
* Maximum of 800 follows / unfollows a day (200-300 for a new account)
* Maximum of likes a day = 1.5 \* the follow limit
* Maximum of 250-300 comments a day
* 1-2 seconds between each request
