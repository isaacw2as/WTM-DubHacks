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
      
      return res
      
    except Exception as we:
      logger.error(f"DB: Error in getting post info: {pid=}")
      
    return None
      

if __name__ == "__main__":
  d = DatabaseClient()