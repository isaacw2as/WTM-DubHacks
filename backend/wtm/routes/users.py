from flask import Blueprint, request
from backend.wtm.db import DatabaseClient
from backend.wtm.util import Responses, deserialize_request_body

db_client = DatabaseClient()
responses = Responses()

users = Blueprint("users", __name__,
                          url_prefix="/users")

@users.route("/create", methods=["POST"])
def create_user():
    payload = deserialize_request_body(request)
    username, password, interests = payload["username"], payload["password"], payload["interests"]
    if db_client.user_exists(username):
        return responses.fail("Failure: Username exists. Please try again with a different username.")
    db_client.register_new_user(username, password, interests)
    return responses.success()

@users.route("/friends", methods=["GET"])
def get_friends_list():
    payload = deserialize_request_body(request)
    username = payload["username"]
    friends_list = db_client.get_friends(username)
    if friends_list is None: friends_list = []
    friends_dict = {
        "username": username,
        "friends": friends_list
    }
    return responses.json_data(friends_dict)
