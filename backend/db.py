from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os

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
      print(e)

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
      print(res)
      
    except Exception as e:
      print(e)

  def login(self, username, password):
    try:
      users_collection = self.db.get_collection("USERS")
      res = users_collection.find_one({"username": username})
      if res == None:
        return False
      
      return res['password'] == password
      
    except Exception as e:
      print(e)
    
    return False

  def is_friend(self, my_username, friends_username):
    try:
      users_collection = self.db.get_collection("USERS")
      res = users_collection.find_one({"username": my_username})
      if res == None:
        return False

      return friends_username in res['friends']
    except Exception as e:
      print(e)
    
    return False


  def add_friend(self, my_username, friends_username):
    try:
      users_collection = self.db.get_collection("USERS")
      res = users_collection.find_one_and_update({ "username": my_username }, {"$push": {"friends": friends_username}})

      return res != None

    except Exception as e:
      print(e)
    
    return False
    

if __name__ == "__main__":
  d = DatabaseClient()
  print(d.is_friend("username0", "username1"))