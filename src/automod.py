

import time
from instabot import InstaBot
import datetime
import random
import sys
import pickle
import os
from requests.exceptions import *


def probability (proba):
    return random.uniform(0, 1) >= 1 - proba
def formatedDate ():
    return time.strftime("%H:%M:%S", time.localtime())


class InstaBotWithAutoMod (InstaBot):

    def __init__ (self, username, password):
        InstaBot.__init__(self, username, password)
        self.kill_now = False
        self._ConnectionResetErrors = 0
        self.unfollow_queue_file_name = "{}_unfollow_queue.txt".format(self.username)
        try:
            self.unfollow_queue = pickle.load(open("{}/{}".format(os.path.dirname(__file__), self.unfollow_queue_file_name), "rb"))
        except:
            self.unfollow_queue = {}
        import signal
        signal.signal(signal.SIGINT, self.stop)
        signal.signal(signal.SIGTERM, self.stop)

    def stop (self, signum, frame):
        self.kill_now = True

    def sleep (self, seconds):
        started_time = time.time()
        while time.time() < started_time + seconds:
            if self.kill_now:
                raise KeyboardInterrupt

    def start (self, 
               tags= ("default"), 
               max_stack_size= 5,
               average_time_gap= 30,
               follow_ratio= 1,
               like_ratio= 1,
               comment_ratio= .33,
               follow_duration= 300,
               comments= (("Super", "Beautiful", "Great"), ("post", "picture"), ("!", "")),
               add_to_unfollow_queue= True,
               media_owner_max_followers= 500,
               media_max_likes= 20,
               users_blacklist= ("user0"),
               users_whitelist= ("user1"),
               medias_posted_before_time= 300,
               allow_videos= False,
               start_at= datetime.time(hour= 10, minute= 30),
               end_at= datetime.time(hour= 20),
              ):
        saved_args = locals()
        try:
            while start_at < datetime.time(hour= datetime.datetime.now().hour, minute= datetime.datetime.now().minute) < end_at:
                # UNFOLLOW loop
                for user_id, unfollow_at_time in self.unfollow_queue.copy().items():
                    try:
                        username = self.userIdToUsername(user_id)
                        assert not username in users_whitelist
                    except (AssertionError, KeyError): # in whitelist or account deleted
                        del self.unfollow_queue[user_id]
                    else:
                        if time.time() > unfollow_at_time:
                            self.unfollow(user_id)
                            del self.unfollow_queue[user_id]
                            sys.stdout.write("{} UNFOLLOW @{}\n".format(formatedDate(), username))
                            self.sleep(random.uniform(average_time_gap * .5, average_time_gap * 1.5))
                # SAVE UNFOLLOW_QUEUE (insurance for exemple if the computer power goes out)
                pickle.dump(self.unfollow_queue, open("{}/{}".format(os.path.dirname(__file__), self.unfollow_queue_file_name), "wb"))
                # FOLLOW, LIKE, COMMENT loop
                for media in self.explore(random.choice(tags))[:max_stack_size]:
                    if time.time() - media["taken_at_timestamp"] > medias_posted_before_time:
                        break 
                    if media["is_video"] and not allow_videos:
                        continue
                    try:
                        media_owner = self.getUserDetails(self.userIdToUsername(media["owner"]["id"]))
                    except KeyError:
                        continue
                    if media_owner["username"] in users_blacklist:
                        continue
                    if media_owner["follows_viewer"] or media_owner["has_requested_viewer"] or \
                       media_owner["followed_by_viewer"] or media_owner["requested_by_viewer"]:
                        continue
                    if media_owner["edge_followed_by"]["count"] > media_owner_max_followers or \
                       media["edge_liked_by"]["count"] > media_max_likes:
                        continue
                    if probability(follow_ratio):
                        self.sleep(random.uniform(1, 2))
                        self.follow(media_owner["id"])
                        sys.stdout.write("{} FOLLOW @{}\n".format(formatedDate(), media_owner["username"]))
                        if add_to_unfollow_queue:
                            self.unfollow_queue[media_owner["id"]] = time.time() + follow_duration
                    if probability(like_ratio):
                        self.sleep(random.uniform(1, 2))
                        self.like(media["id"])
                        sys.stdout.write("{} LIKE media shortcode {}\n".format(formatedDate(), media["shortcode"]))
                    if probability(comment_ratio):
                        if media["comments_disabled"]:
                            continue
                        comment = " ".join([random.choice(sub_comment) for sub_comment in comments])
                        self.sleep(random.uniform(1, 2))
                        comment_id = self.comment(media["id"], comment)
                        sys.stdout.write("{} COMMENT media shortcode {}, comment id {}\n".format(formatedDate(), media["shortcode"], comment_id))
                    self.sleep(random.uniform(average_time_gap * .5, average_time_gap * 1.5))
        except ConnectionError:
            self.sleep(60)
        # instagram warning
        except ConnectionResetError:
            sys.stdout.write("{} Connection aborted, freezing for {} seconds\n".format(formatedDate(), 4 * 2 ** self._ConnectionResetErrors))
            self.sleep(4 * 2 ** self._ConnectionResetErrors)
        except KeyboardInterrupt:
            sys.stdout.write("{} Exit message received\n".format(formatedDate()))
            return
        # account / media deleted
        except HTTPError as e:
            sys.stdout.write("{} {}\n".format(formatedDate(), e))
        # bot not logged in
        except RuntimeError:
            raise
        except Exception as e:
            sys.stdout("{} Error {}".format(formatedDate(), e))
        else:
            self.sleep(60)
        finally:
            pickle.dump(self.unfollow_queue, open("{}/{}".format(os.path.dirname(__file__), self.unfollow_queue_file_name), "wb"))
        self.start(saved_args)


if __name__ == "__main__": 
    bot = InstaBotWithAutoMod ("username", "password")
    bot.login()
    bot.start(**{
                    "tags": ("draw", "drawing"),
                    "start_at": datetime.time(),
                    "end_at": datetime.time(hour=19, minute=15),
                })

    
