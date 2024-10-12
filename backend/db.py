from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
import logging

logger = logging.getLogger(__name__)
class DatabaseClient:
  def __init__(self):
    DB_PASS = os.environ.get("DB_PASSWORD", "WTMPassword")
    uri = f"mongodb+srv://olegianch:{DB_PASS}@wtm-cluster.bl2wm.mongodb.net/?retryWrites=true&w=majority&appName=wtm-cluster"
    db_client = MongoClient(uri, server_api=ServerApi("1"))
    self.db = db_client.get_database("WTM")

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
        logger.warning(f"DB: is friend of nonexistant user: {my_username}")
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
      logger.error(f"DB: Add friend error: {my_username}")
    
    return False

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
      logger.error(f"DB: Add pending event error: {username=}, {event_id}=")
    
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
    
    

if __name__ == "__main__":
  d = DatabaseClient()
  print(d.move_pending_event("username0", "event0"))