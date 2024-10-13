from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
import logging
import gridfs

logger = logging.getLogger(__name__)
class DatabaseClient:
  def __init__(self):
    DB_PASS = os.environ.get("DB_PASSWORD", "WTMPassword")
    uri = f"mongodb+srv://olegianch:{DB_PASS}@wtm-cluster.bl2wm.mongodb.net/?retryWrites=true&w=majority&appName=wtm-cluster"
    db_client = MongoClient(uri, server_api=ServerApi("1"))
    self.db = db_client.get_database("WTM")
    self.fs = gridfs.GridFS(self.db)

  #######################################################
  ### USER HELPERS ######################################
  #######################################################
  def user_exists(self, username):
    try:
      user_collection = self.db.get_collection("USERS")
      res = user_collection.find_one({"username": username})
      return res != None

    except Exception as e:
      logger.error(f"DB: User exists error: {e}")

    return False

  def register_new_user(self, username: str, password: str, interest_ids: list):
    try:
      users_collection = self.db.get_collection("USERS")
      res = users_collection.insert_one(
        {
          "username": username,
          "password": password,
          "friends": [],
          "pastEids": [],
          "pendingEids": [],
          "interests": interest_ids,
          "latestEid": 0,
        }
      )
      logger.info(f"DB: registered new user: {username}")
      
    except Exception as e:
      logger.error(f"DB: User register: {e}")

  def login(self, username, password):
    try:
      users_collection = self.db.get_collection("USERS")
      res = users_collection.find_one({"username": username})
      if res == None:
        logger.warning(f"DB: login with non existant user: {username}")
        return False
      
      logger.info(f"DB: logged in: {username}")
      return res['password'] == password
      
    except Exception as e:
      logger.error(f"DB: Login error: {e}")
    
    return False

  def is_friend(self, my_username, friends_username):
    try:
      users_collection = self.db.get_collection("USERS")
      res = users_collection.find_one({"username": my_username})
      if res == None:
        logger.warning(f"DB: is friend of non-existent user: {my_username}")
        return False

      return friends_username in res['friends']
    except Exception as e:
      logger.error(f"DB: is friend error: {e}")
    
    return False

  def add_friend(self, my_username, friends_username):
    try:
      users_collection = self.db.get_collection("USERS")
      res = users_collection.find_one({ "username": my_username })
      if friends_username in res["friends"]:
        return False

      res = users_collection.find_one_and_update({ "username": my_username }, {"$push": {"friends": friends_username}})

      logger.info(f"DB: add friend {friends_username=} of user {my_username=}")
      return res != None

    except Exception as e:
      logger.error(f"DB: Add friend error for: {my_username}")
    
    return False
  
  def get_friends(self, my_username):
    try:
      users_collection = self.db.get_collection("USERS")
      res = users_collection.find_one({"username": my_username})
      if res == None:
        logger.warning(f"Non-existent user: {my_username}")
        return None
      
      return res["friends"]
    except Exception as e:
      logger.error(f"DB: Get friends list error for: {my_username}")
    
    return None

  def is_pending_event(self, username, event_id):
    try:
      users_collection = self.db.get_collection("USERS")
      res = users_collection.find_one({ "username": username })
      if res == None:
        logger.warning(f"DB: checking pending event for non existant user {username}")
        return False
      
      return event_id in res['pendingEids']
      
    except Exception as e:
      logger.error(f"DB: is pending event error: {e}")
      
    return False

  def add_pending_event(self, username, event_id):
    try:
      users_collection = self.db.get_collection("USERS")
      res = users_collection.find_one_and_update({ "username": username }, {"$push": {"pendingEids": event_id}})
      logger.info(f"DB: added event {event_id} to user pending events of {username}")

      return res != None

    except Exception as e:
      logger.error(f"DB: Add pending event error: {username=}, {event_id=}")
    
    return False
  
  def set_latest_eid(self, username, latest_eid):
    try:
      users_collection = self.db.get_collection("USERS")
      res = users_collection.find_one_and_update({"username": username}, {"$set": {"latestEid": latest_eid}})
      logger.info(f"DB: set user {username} latest eid to: {latest_eid}")

      return res != None
    
    except Exception as e:
      logger.error(f"DB: Set latest eid error: {username=}, {latest_eid=}")

    return False

  def move_pending_event(self, username, event_id):
    try:
      users_collection = self.db.get_collection("USERS")
      res = users_collection.find_one_and_update({ "username": username }, {"$pull": {"pendingEids": event_id}})
      if res == None:
        logger.warning(f"DB: Not supposed to happen1")
        return False

      res = users_collection.find_one_and_update({"username": username}, {"$push": {"pastEids": event_id}})
      if res == None:
        logger.warning(f"DB: Not supposed to happen2")
        return False

      return True
    except Exception as e:
      logger.error(f"DB: move pending event error: {e}")
    
    return False

  def get_user_info(self, username):
    try:
      users_collection = self.db.get_collection("USERS")
      res = users_collection.find_one({ "username": username })
      if res == None:
        logger.warning(f"DB: Username {username} does not exist.")
      return res

    except Exception as e:
      logger.error(f"DB: Error getting user {username}")
    
    return None

  #######################################################
  ### EVENT HELPERS #####################################
  #######################################################
  def get_largest_eid(self) -> int:
    try:
      events_collection = self.db.get_collection("EVENTS")
      res = events_collection.find().sort({"eid": -1}).limit(1)
      res = res.to_list()

      if not res:
        logger.error("DB: No events in DB")
        return -1
      
      return res[0]['eid']
      
    except Exception as e:
      logger.error(f"Error in finding largest eid: {e}")
    
    return -1

  def register_event_under_user(self, eid, name, loc, 
                                timestamp, description: dict, 
                                associated_interests: list, organizer_username):
    try:
      users_collection = self.db.get_collection("USERS")
      res = users_collection.find_one_and_update({"username": organizer_username}, {"$push": {"pendingEids": eid}})
      if res == None:
        logger.warning(f"Registered event to unknown user {organizer_username}")
        return
      
      events_collection = self.db.get_collection("EVENTS")
      res = events_collection.insert_one(
        {
          "eid": eid,
          "name": name,
          "loc": loc,
          "timestamp": timestamp,
          "description": description,
          "interests": associated_interests,
          "associated_posts": [],  # new event, no posts under it
          "organizer_username": organizer_username,
        }
      )
      logger.info(f"DB: registered new event {name} under {organizer_username}")
      
    except Exception as e:
      logger.error(f"DB: Event register: {e}")
    
  def get_event_info(self, eid):
    try:
      events_collection = self.db.get_collection("EVENTS")
      res = events_collection.find_one({"eid": int(eid)})
      if res == None:
        logger.warning(f"DB: Event with eid {eid} does not exist.")
        return None
      
      return res
      
    except Exception as e:
      logger.error(f"DB: Get event failed: {e}")
    
    return None
  
  def associate_post_with_event(self, pid, eid):
    try:
      users_collection = self.db.get_collection("EVENTS")
      res = users_collection.find_one_and_update({"eid": eid}, {"$push": {"associated_posts": pid}})
      if res == None:
        logger.warning(f"Associating post with unknown eid {eid}")
        return False
      
      return True
    
    except Exception as e:
      logger.error(f"DB: Error associate post {pid} with event {eid}: {e} ")
    
    return False
    
  #######################################################
  ### POST HELPERS #####################################
  #######################################################
  def create_post(self, pid, username, filename: str):
    try:
      posts_collection = self.db.get_collection("POSTS")
      posts_collection.insert_one({
        "pid": pid,
        "username": username,
        "filename": filename,
        "n_likes": 0,
        "comments": [],
      })

      return True
      
    except Exception as e:
      logger.error(f"DB: Get event failed: {e}")
    
    return False
  
  def add_comment(self, pid, comment_info):
    try:
      posts_collection = self.db.get_collection("POSTS")
      res = posts_collection.find_one_and_update({"pid": pid}, {"$push": {"comments": comment_info}})
      if res == None:
        logger.warning(f"DB: Adding post to non-existent post: {pid}")
        return False
      
      return True
    except Exception as e:
      logger.error(f"DB: Add comment failed: {e}")
    
    return False
  
  def add_like(self, pid):
    try:
      posts_collection = self.db.get_collection("POSTS")
      res = posts_collection.find_one_and_update({"pid": pid}, {"$inc": {"n_likes": 1}})
      if res == None:
        logger.warning(f"DB: Adding like to non-existent post: {pid}")
      
      return True
    except Exception as e:
      logger.error(f"DB: Add like failed: {e}")
    
    return False
  
  def get_largest_pid(self) -> int:
    try:
      posts_collection = self.db.get_collection("POSTS")
      res = posts_collection.find().sort({"pid": -1}).limit(1)
      res = res.to_list()

      if not res:
        logger.error("DB: No events in DB")
        return -1
      
      return res[0]['pid']
      
    except Exception as e:
      logger.error(f"DB: Error in finding largest pid: {e}")
    
    return -1
  
  def get_post_info(self, pid):
    try:
      post_collection = self.db.get_collection("POSTS")
      res = post_collection.find_one({"pid": pid})
      if res is None:
        logger.warning(f"DB: Pid {pid} does not exist.")
        return None
      
      del res["_id"]

      return res
      
    except Exception as we:
      logger.error(f"DB: Error in getting post info: {pid=}")
      
    return None
      

if __name__ == "__main__":
  # art music gaming nature culture sports fitness travel food
  d = DatabaseClient()

  users = ["CarlSearle", "OlegIanchenko", "IsaacYun", "MadelynLee", "EliBrown", "SamuelVirji", "DominicDollar", "JohnathanSummitSchuster", "ToveLo", "BeltranUK"]

  content = {
    "Nightmare on Deck": "65585857229c13334-6815-4f5a-8921-8b3b9d4bc939.png",
    "Cristoph @Q": "11931821image_1721771985764_1ns1etu0h.png",
    "Kobuta and Ookami": "830126366v12044gd0000cn6ma6nog65radqm7ul0.mov",
    "Thursday Night Football": "96025325841v12025gd0000cs5cecvog65nodi34v7g.mov",
    "Dreamland Bar": "89596789258v12044gd0000ci8gsb3c77u2omeun3dg.mov",
    "CID Block Party": "38973220854v12044gd0000cjegbibc77ucd147vu60.mov",
    "Day Hike": "74690201846v12044gd0000ckcoufjc77u45k9o6jv0.mov",
    "Yoga": "92720655045v12044gd0000cp1ucffog65jrk2lak6g.mov",
    "Boat Party": "46909413613v12044gd0000cpvo5rvog65sjmoosp1g.mov",
    "Pioneer Square Art Walk": "39839557909v12044gd0000crdqdsvog65ns1ghrrc0.mov",
    "Together as One": "89019066081v12044gd0000crq6kjvog65mm04tmghg.mov",
    "Ballard Farmers Market": "49724969767v12044gd0000cs2lm5nog65l75k4upf0.mov",
    "Boo": "16901042940v12044gd0000cs4ppfnog65gjf2pcqo0.mov",
    "Inside Passage": "19968106548v12300gd0001cj5ar4rc77ubmnv64au0.mov",
    "Shakespeare in the Park": "20472420027v15044gf0000cqp50a7og65gnm3ba68g.mov",
  }

  interests = {
    "Nightmare on Deck": ["music", "culture"],
    "Cristoph @Q": ["music", "art"],
    "Kobuta and Ookami": ["food", "culture", "travel"],
    "Thursday Night Football": ["gaming", "sports", "fitness"],
    "Dreamland Bar": ["art", "food", "music"],
    "CID Block Party": ["music", "culture"],
    "Day Hike": ["nature", "travel", "fitness"],
    "Yoga": ["fitness"],
    "Boat Party": ["music", "culture", "travel"],
    "Pioneer Square Art Walk": ["art", "culture"],
    "Together as One": ["music", "nature"],
    "Ballard Farmers Market": ["travel", "food", "culture"],
    "Boo": ["music", "gaming", "culture"],
    "Inside Passage": ["culture", "food", "art"],
    "Shakespeare in the Park": ["art", "gaming", "nature"],
  }

  from datetime import datetime, timedelta
  import random

  # for i, event_name in enumerate(content):
  #   # organizer_id = random.choice(users)
  #   # file_name = content[event_name]

  #   # delta = timedelta(days=random.randint(0, 10), hours=random.randint(0, 5), minutes=random.randint(0, 59), seconds=random.randint(0, 59))
  #   # now = datetime.now()
  #   # then = now + delta

  #   # next_eid = d.get_largest_eid() + 1

  #   # d.register_event_under_user(
  #   #   next_eid,
  #   #   event_name,
  #   #   "Seattle, WA",
  #   #   then.strftime("%Y-%m-%dT%H:%M:%S"),
  #   #   "",
  #   #   interests[event_name],
  #   #   organizer_id
  #   # )

  #   events = d.db.get_collection("EVENTS")
  #   event = events.find_one({"name": event_name})

  #   posts = d.db.get_collection("POSTS")
  #   post = posts.find_one({"filename": content[event_name]})

  #   d.associate_post_with_event(post["pid"], event["eid"])

  for user in users:
    d.set_latest_eid(user, 1)