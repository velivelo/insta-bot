# insta-bot
An Insagram bot made with Python and independant from the Instagram API.

## The bot can

From help(InstaBot) :
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
It also has an autoMod function.

## Installation

1. Download and install python3+ on your computer
2. `git clone` this repo or download as a ZIP and extract
3. Install dependencies `pip install -r requirements.txt`
