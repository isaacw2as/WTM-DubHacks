from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os

DB_PASS = os.environ.get("DB_PASSWORD", "WTMPassword")
uri = f"mongodb+srv://olegianch:{DB_PASS}@wtm-cluster.bl2wm.mongodb.net/?retryWrites=true&w=majority&appName=wtm-cluster"
db_client = MongoClient(uri, server_api=ServerApi("1"))
db = db_client.get_database("WTM")

def user_exists(username):
  try:
    user_collection = db.get_collection("USERS")
    res = user_collection.find_one({"username": username})
    return res != None

  except Exception as e:
    print(e)

  return False

def register_new_user(username: str, password: str, interest_ids: list):
  try:
    users_collection = db.get_collection("USERS")
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
    


if __name__ == "__main__":
  print(user_exists("username1"))