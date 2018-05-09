# insta-bot
An Insagram bot made with Python and independant from the Instagram API.

## The bot can

### src/instabot.py > class InstaBot
| Method | Definition | Argument(s)
| ------ | ---------- | -----------
| login | login to instagram | -
| follow | follow an user | user_id
| unfollow | unfollow an user | user_id
| like | like a media | media_id
| unlike | unlike a media | media_id
| comment | post a comment (return the comment_id) | media_id, text
| uncomment | delete a comment | media_id, comment_id
| explore | return a list of medias | tag
| downloadMedia | download a media | media_shortcode
| getUserDetails | return a dictionary with the user details | username
| usernameToUserId | return the user_id | username
| userIdToUsername | return the username | user_id

### src/automod.py > class InstaBotWithAutoMod > start method
| Parameter | Definition | Default value
| -------- | ---------- | -------------
| tags | list of tags to explore | ("default")
| follow_ratio | probability to follow a media owner | 1
| like_ratio | probability to like a media | 1
| comment_ratio | probability to coment a media | 0.33
| average_time_gap | average time between each media iteration | 30
| max_stack_size | number of medias to explore at each loop | 5
| comments | list of sub_comment | (("Super", "Beautiful", "Great"), ("post", "picture"), ("!", ""))
| add_to_unfollow_queue | the followed users will be unfollowed | True
| follow_duration | time before unfollowing | 600
| media_owner_max_followers | max followers for follow | 500
| media_max_likes | max likes for like | 20
| medias_posted_before_time | handle only the medias posted before time | 300
| allow_videos | are videos handled | False
| users_blacklist | these users won't be followed | ("user0")
| users_whitelist | these users won't be unfollowed | ("user1")
| start_at | starting time | dtime(hour= 7)
| end_at | ending_time | dtime(hour= 22, minute= 30)

## Installation

1. Download and install python3+ on your computer
2. `git clone` this repo or download as a ZIP and extract
3. Install dependencies `pip install -r requirements.txt`

## Warnings !

These are the approximately Instagram limits. Be worry of respecting them or you'll get a bunch of 403 HTTP errors and might get banned !
* Maximum of 800 follows / unfollows a day (200-300 for a new accounts)
* Maximum of likes a day = 1.5 \* the follow limit
* Maximum of 250-300 comments a day (100-150 for new accounts)
* 1-2 seconds between each request
