from flask import Blueprint, request
from backend.wtm.db import DatabaseClient
from backend.wtm.util import Responses, deserialize_request_body
import random

db_client = DatabaseClient()
responses = Responses()

feed = Blueprint("feed", __name__,
                    url_prefix="/feed")

@feed.route("/get", methods=["GET"])
def get_feed():
    payload = deserialize_request_body(request)
    username = payload["username"]
    user_data = db_client.get_user_info(username)
    latest_eid = user_data["latestEid"]
    user_friends = user_data["friends"]
    posts = []
    if user_friends:
        for i in range(3):
            friend = random.choice(user_friends)
            friend_data = db_client.get_user_info(friend)
            friend_pending = friend_data["pendingEids"]
            if friend_pending:
                friend_eid = random.choice(friend_pending)
                current_event_info = db_client.get_event_info(friend_eid)
                posts.append(random.choice(current_event_info["associated_posts"]))
    while len(posts) < 10:
