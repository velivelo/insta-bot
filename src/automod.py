
from instabot import *
import sys
import pickle
import os


class GracefulKiller ():
    kill_now = False

    def __init__(self):
        import signal
        signal.signal(signal.SIGINT, self.exitGracefully)
        signal.signal(signal.SIGTERM, self.exitGracefully)

    def exitGracefully (self, signum, frame):
        self.kill_now = True


def formatedDate ():
    return time.strftime("%H:%M:%S", time.localtime())


# All times are exprimed in seconds
def autoMod (follow_duration= 300, # time before unfollowing (0 for infinite)
             time_gap= 60, # time between medias treatment
             tags= ("default"), # media tags to explore
             log= True, # sys.stdout.write the logs (RECOMENDED)
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
             iterations= 5, # number of times the function is recalled
            ):
    saved_args = locals()
    i = 0
    for media in bot.explore(random.choice(tags)):
        for user_id, unfollow_at_time in unfollow_queue.copy().items():
            if time.time() > unfollow_at_time:
                try:
                    bot.unfollow(user_id)
                except Exception as e:
                    print(e)
                del unfollow_queue[user_id]
                if log:
                    sys.stdout.write("{} UNFOLLOW > user id : {}\n".format(formatedDate(), user_id))
                time.sleep(random.uniform(time_gap * .5, time_gap * 1.5))
                if killer.kill_now:
                    return

        owner_details = bot.getUserDetails(bot.userIdToUsername(media["owner"]["id"]))
        if time.time() - media["taken_at_timestamp"] > only_medias_posted_before_timestamp:
            break # bot.explore list is chronological
        if media["is_video"] and not videos:
            continue
        if owner_details["username"] in users_blacklist:
            continue
        if follow:
            if owner_details["follows_viewer"]:
                continue
            if owner_details["edge_followed_by"]["count"] > max_followers_for_follow:
                continue
            if unfollow_already_followed and (owner_details["followed_by_viewer"] or owner_details["requested_by_viewer"]):
                continue
            try:
                bot.follow(owner_details["id"])
            except Exception as e:
                print(e)
            if follow_duration:
                unfollow_queue[owner_details["id"]] = time.time() + follow_duration
            if log:
                sys.stdout.write("{} FOLLOW > user : @{}\n".format(formatedDate(), owner_details["username"]))
            time.sleep(random.uniform(1, 2))
        if like:
            if media["edge_liked_by"]["count"] > max_likes_for_like:
                continue
            try:
                bot.like(media["id"])
            except Exception as e:
                print(e)
            if log:
                sys.stdout.write("{} LIKE > media shortcode : {}\n".format(formatedDate(), media["shortcode"]))
            time.sleep(random.uniform(1, 2))
        if comment:
            if media["comments_disabled"]:
                continue
            try:
                comment_id = bot.comment(media["id"], " ".join([random.choice(sub_comment) for sub_comment in comments]))
                if log:
                    sys.stdout.write("{} COMMENT > media shortcode : {}, comment id : {}\n".format(formatedDate(), media["shortcode"], comment_id))
            except Exception as e:
                print(e)

        i += 1
        if i == max_stack_size:
            break
        time.sleep(random.uniform(time_gap * .5, time_gap * 1.5))
        if killer.kill_now:
            return
    saved_args["iterations"] -= 1
    if saved_args["iterations"]: 
        autoMod(**saved_args)
        

if __name__ == "__main__":
    bot = InstaBot ("keyzerd", "cerise")
    sys.stdout.write("{} BOT INITIALIZED\n".format(formatedDate()))
    bot.login()
    sys.stdout.write("{} BOT LOGGED\n".format(formatedDate()))
    
    try:
        unfollow_queue = pickle.load(open("{}/unfollow_queue.txt".format(os.path.dirname(__file__)), "rb"))
    except:
        unfollow_queue = {}
    
    killer = GracefulKiller()
    try:


        autoMod(**{
            "time_gap": 30,
            "iterations": 10,
            "tags": ["drawing", "draw"],
            "like": True,
            "comment": True,
        })


    except Exception as e:
        print(e)
    pickle.dump(unfollow_queue, open("{}/unfollow_queue.txt".format(os.path.dirname(__file__)), "wb"))
    sys.stdout.write("{} BOT LOGGED OUT, {} users in unfollow_queue\n".format(formatedDate(), len(unfollow_queue)))


