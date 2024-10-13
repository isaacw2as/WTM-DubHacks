from flask import Blueprint, request
from backend.wtm.db import DatabaseClient
from backend.wtm.util import Responses, deserialize_request_body

db_client = DatabaseClient()
responses = Responses()

friends = Blueprint("friends", __name__,
                         url_prefix="/friends")

@friends.route("/add", methods=["POST"])
def add_friend():
    payload = deserialize_request_body(request)
    username, friend_username = payload["username"], payload["friend_username"]
    if db_client.is_friend(username, friend_username):
        return responses.fail(f"{friend_username} is already friends with the current user")
    db_client.add_friend(username, friend_username)
    db_client.add_friend(friend_username, username)
    return responses.success()

@friends.route("/get", methods=["GET"])
def get_friends_list():
    payload = deserialize_request_body(request)
    username = payload["username"]
    friends_list = db_client.get_friends(username)
    friends_dict = {
        "username": username,
        "friends": friends_list
    }
    return responses.json_data(friends_dict)