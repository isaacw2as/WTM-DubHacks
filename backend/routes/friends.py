from flask import Blueprint, request
from backend.db import DatabaseClient
from backend.util import Responses, deserialize_request_body

db_client = DatabaseClient()
responses = Responses()

addFriend_bp = Blueprint("friends", __name__,
                         url_prefix="/friends")

@addFriend_bp.route("/addFriend/<friend_username>", methods=["POST"])
def addFriend(friend_username: str):
    payload = deserialize_request_body(request)
    username = payload["username"]
    if db_client.is_friend(username, friend_username):
        return responses.fail(f"{friend_username} is already friends with the current user")
    db_client.add_friend(username, friend_username)
    return responses.success()