

from instabot import *
import sys
import pickle
import os
import datetime


class GracefulKiller ():
    kill_now = False

    def __init__(self):
        import signal
        signal.signal(signal.SIGINT, self.exitGracefully)
        signal.signal(signal.SIGTERM, self.exitGracefully)

    def exitGracefully (self, signum, frame):
        """Handle exits signals"""
        self.kill_now = True

    def freezeProgram (self, seconds):
        """Acts like time.sleep(x) but return True as soon as kill_now is True"""
        freeze_start = time.time()
        while time.time() - freeze_start < seconds:
            if self.kill_now:
                return True
        return False


def formatedDate ():
    return time.strftime("%H:%M:%S", time.localtime())


# All times are exprimed in seconds
def autoMod (self, follow_duration= 300, time_gap= 60, tags= ("default"), unfollow_if_followed_back= True, unfollow_already_followed= False,
             follow= True, like= False, max_stack_size= 5, videos= False, max_likes_for_like= 20, max_followers_for_follow= 500,
             only_medias_posted_before_timestamp= 600, comment= False, comments= (("Super", "Beautiful", "Great"), ("post", "picture"), ("!", "")),
             users_blacklist= ("instagram"), comment_ratio= .33, unfollow= True, start_at= datetime.datetime.now(), end_at= datetime.datetime.max,
            ):
    """
    follow_duration= 300,                                                        # time before unfollowing (0 for infinite)
    time_gap= 60,                                                                # time between medias treatment
    tags= ("default"),                                                           # media tags to explore
    unfollow_if_followed_back= True,                                             # unfollow even if the user has followed back
    unfollow_already_followed= False,                                            # can the bot unfollow people already followed 
    follow= True,                                                                # follow medias owners
    like= False,                                                                 # like medias 
    max_stack_size= 5,                                                           # maximum number of medias treated for a tag
    videos= False,                                                               # take care of videos
    max_likes_for_like= 20,                                                      # max likes a media can have to be liked
    max_followers_for_follow= 500,                                               # max followers an user can have to be followed
    only_medias_posted_before_timestamp= 600,                                    # treat only a media if posted before timestamp
    comment= False,                                                              # comment the media
    comments= (("Super", "Beautiful", "Great"), ("post", "picture"), ("!", "")), # list of comments
    users_blacklist= ("instagram"),                                              # users blacklisted
    comment_ratio= .33,                                                          # probability of posting a comment even if comment set to True
    unfollow= True,                                                              # the bot add acounts to the unfollow queue after followed
    start_at= datetime.datetime.now(),                                           # the bot start at
    end_at= datetime.datetime.max,                                               # the bot end at
    """
    if datetime.datetime.now() < start_at:
        sys.stdout("{} Waiting till its time to start\n".format(formatedDate()))
    while datetime.datetime.now() < start_at:
        if killer.freezeProgram(10):
            raise KeyboardInterrupt("") 
    try:
        while True:
            i = 0
            tag = random.choice(tags)
            medias = self.explore(tag)
            sys.stdout.write("{} EXPLORE > medias with tag #{}, {} medias founded\n".format(formatedDate(), tag, len(medias)))
            for media in medias:

                # UNFOLLOW LOOP
                for user_id, unfollow_at_time in unfollow_queue.copy().items():
                    if time.time() > unfollow_at_time:
                        self.unfollow(user_id)
                        del unfollow_queue[user_id]
                        sys.stdout.write("{} UNFOLLOW > user id : {}\n".format(formatedDate(), user_id))
                        if killer.freezeProgram(random.uniform(time_gap * .5, time_gap * 1.5)):
                            raise KeyboardInterrupt("")
                        assert end_at > datetime.datetime.now()

                # FOLLOW, LIKE, COMMENT LOOP
                owner_details = self.getUserDetails(self.userIdToUsername(media["owner"]["id"]))
                if time.time() - media["taken_at_timestamp"] > only_medias_posted_before_timestamp:
                    break 
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
                    self.follow(owner_details["id"])
                    if unfollow and follow_duration:
                        unfollow_queue[owner_details["id"]] = time.time() + follow_duration
                    sys.stdout.write("{} FOLLOW > user : @{}\n".format(formatedDate(), owner_details["username"]))
                if like:
                    time.sleep(random.uniform(1, 2))
                    if media["edge_liked_by"]["count"] > max_likes_for_like:
                        continue
                    self.like(media["id"])
                    sys.stdout.write("{} LIKE > media shortcode : {}\n".format(formatedDate(), media["shortcode"]))
                if comment and random.uniform(0, 1) >= 1 - comment_ratio:
                    time.sleep(random.uniform(1, 2))
                    if media["comments_disabled"]:
                        continue
                    comment_id = self.comment(media["id"], " ".join([random.choice(sub_comment) for sub_comment in comments]))
                    sys.stdout.write("{} COMMENT > media shortcode : {}, comment id : {}\n".format(formatedDate(), media["shortcode"], comment_id))

                i += 1
                if i == max_stack_size:
                    break
                if killer.freezeProgram(random.uniform(time_gap * .5, time_gap * 1.5)):
                    raise KeyboardInterrupt("")
                assert end_at > datetime.datetime.now()
    except:
        raise
    finally: # kind of insurance (for exemple if the computer power goes out)
        pickle.dump(unfollow_queue, open("{}/unfollow_queue.txt".format(os.path.dirname(__file__)), "wb"))


InstaBot.autoMod = autoMod


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
    freezing_time = 4
    for i in range(10): # 10 is the maximum number of errors
        try:

            bot.autoMod(**{
                "time_gap": 30,
                "tags": ["drawing", "draw"],
                "like": True,
                "comment": True, 
                #"end_at": datetime.datetime(2018, 4, 27, hour=11, minute=30)
            })

        except (KeyboardInterrupt, AssertionError) as e:
            sys.stdout.write("EXIT\n".format(e))
            break
        except ConnectionResetError:
            sys.stdout.write("Connection aborted, freezing for {} seconds".format(freezing_time))
            killer.freezeProgram(freezing_time)
            freezing_time *= 2
        except Exception as e:
            sys.stdout.write("{}\n".format(e))
    sys.stdout.write("{} BOT LOGGED OUT, {} users in unfollow_queue\n".format(formatedDate(), len(unfollow_queue)))

