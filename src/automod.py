

from instabotV2 import InstaBot, LoginError
from requests.exceptions import ConnectionError, ReadTimeout
from datetime import time as dtime, datetime as ddtime
from time import time, strftime, localtime
from signal import signal, SIGINT, SIGTERM
from os import path, makedirs
from pickle import load, dump
from random import uniform, choice
import sys


def probability (proba):
    return uniform(0, 1) >= 1 - proba
def formatedDate ():
    return strftime("%H:%M:%S", localtime())


class InstaBotWithAutoMod (InstaBot):

    def __init__ (self,
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
                  users_blacklist= ("user0",),
                  users_whitelist= ("user1",),
                  medias_posted_before_time= 300,
                  allow_videos= False,
                  start_at= dtime(hour= 10, minute= 30),
                  end_at= dtime(hour= 20),
                 ):
        InstaBot.__init__(self)
        [setattr(self, name, value) for name, value in locals().items() if name != "self"]
        self.kill_now = False
        self._ConnectionResetErrors = 0
        signal(SIGINT, self.stop)
        signal(SIGTERM, self.stop)

    def stop (self, signum, frame):
        self.kill_now = True

    def sleep (self, seconds= 0):
        if not seconds:
            seconds = uniform(self.average_time_gap * .5, self.average_time_gap * 1.5)
        started_time = time()
        while time() < started_time + seconds:
            if self.kill_now:
                raise KeyboardInterrupt

    def waitTillStartTime (self, gap_time= 30):
        while dtime(hour= ddtime.now().hour, minute= ddtime.now().minute) < self.start_at:
            self.sleep(gap_time)

    def login (self, username, password):
        super().login(username, password)
        self.unfollow_queue_dir = path.join(path.dirname(__file__), "data", "{}-unfollow-queue.txt".format(self.username))
        self.loadUnfollowQueue()

    def loadUnfollowQueue (self):
        try:
            self.unfollow_queue = load(open(self.unfollow_queue_dir, "rb"))
        except:
            self.unfollow_queue = {}

    def saveUnfollowQueue (self):
        makedirs("data", exist_ok= True)
        dump(self.unfollow_queue, open(self.unfollow_queue_dir, "wb"))

    def unfollowProtocol (self):
        for user_id, unfollow_at_time in self.unfollow_queue.copy().items():
            try:
                username = self.userIdToUsername(user_id)
                assert not username in self.users_whitelist
            except (AssertionError, KeyError): # in whitelist or account deleted
                del self.unfollow_queue[user_id]
            else:
                if time() > unfollow_at_time:
                    self.unfollow(user_id)
                    del self.unfollow_queue[user_id]
                    sys.stdout.write("{} UNFOLLOW @{}\n".format(formatedDate(), username))
                    self.sleep()

    def mainLoop (self):
        self.unfollowProtocol()
        for media in self.explore(choice(self.tags))[:self.max_stack_size]:
            if time() - media["taken_at_timestamp"] > self.medias_posted_before_time:
                break 
            if media["is_video"] and not self.allow_videos:
                continue
            try:
                media_owner = self.getUserDetails(self.userIdToUsername(media["owner"]["id"]))
            except KeyError:
                continue
            if media_owner["username"] in self.users_blacklist:
                continue
            if media_owner["follows_viewer"] or media_owner["has_requested_viewer"] or \
               media_owner["followed_by_viewer"] or media_owner["requested_by_viewer"]:
                continue
            if media_owner["edge_followed_by"]["count"] > self.media_owner_max_followers or \
               media["edge_liked_by"]["count"] > self.media_max_likes:
                continue
            if probability(self.follow_ratio):
                self.sleep(uniform(1, 2))
                self.follow(media_owner["id"])
                sys.stdout.write("{} FOLLOW @{}\n".format(formatedDate(), media_owner["username"]))
                if self.add_to_unfollow_queue:
                    self.unfollow_queue[media_owner["id"]] = time() + self.follow_duration
            if probability(self.like_ratio):
                self.sleep(uniform(1, 2))
                self.like(media["id"])
                sys.stdout.write("{} LIKE media shortcode {}\n".format(formatedDate(), media["shortcode"]))
            if probability(self.comment_ratio):
                if media["comments_disabled"]:
                    continue
                comment = " ".join([choice(sub_comment) for sub_comment in self.comments])
                self.sleep(uniform(1, 2))
                comment_id = self.comment(media["id"], comment)
                sys.stdout.write("{} COMMENT media shortcode {}, comment id {}\n".format(formatedDate(), media["shortcode"], comment_id))
            self.sleep()

    def start (self):
        self.waitTillStartTime()
        try:
            self.mainLoop()
        except (ConnectionError, ReadTimeout):
            sys.stdout.write("{} Connection error, freezing for 15 seconds\n".format(formatedDate()))
            self.sleep(15)
        except ConnectionResetError: # never tested 
            sys.stdout.write("{} Connection aborted, freezing for {} seconds\n".format(formatedDate(), 4 * 2 ** self._ConnectionResetErrors))
            self.sleep(4 * 2 ** self._ConnectionResetErrors)
        except KeyboardInterrupt:
            sys.stdout.write("{} Exit message received\n".format(formatedDate()))
            return
        except LoginError:
            raise
        except Exception as e:
            sys.stdout.write("{} Exception : {} : {}\n".format(formatedDate(), type(e).__name__), e)
        else:
            pass
        finally:
            self.saveUnfollowQueue()
        self.start()


if __name__ == "__main__":
    bot = InstaBotWithAutoMod (
                               start_at= dtime(hour= 7, minute= 30), 
                               tags= ("draw", "drawing"),
                               end_at= dtime(hour= 22),
                              )
    bot.login("username", "password")
    bot.start()

    
