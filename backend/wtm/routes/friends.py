from flask import Blueprint, request
from backend.wtm.db import DatabaseClient
from backend.wtm.util import Responses, deserialize_request_body

db_client = DatabaseClient()
responses = Responses()

friends = Blueprint("friends", __name__,
                         url_prefix="/friends")

@friends.route("/add", methods=["POST"])
def add_friend():
    friend_username = request.args.get("friend_username")
    payload = deserialize_request_body(request)
    username = payload["username"]
    if db_client.is_friend(username, friend_username):
        return responses.fail(f"{friend_username} is already friends with the current user")
    db_client.add_friend(username, friend_username)
    db_client.add_friend(friend_username, username)
    return responses.success()