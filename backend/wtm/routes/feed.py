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
    pids = []
    if user_friends:
        for i in range(3):
            friend = random.choice(user_friends)
            friend_data = db_client.get_user_info(friend)
            friend_pending = friend_data["pendingEids"]
            if friend_pending:
                friend_eid = random.choice(friend_pending)
                current_event_info = db_client.get_event_info(friend_eid)
                pids.append(random.choice(current_event_info["associated_posts"]))

    while len(pids) < 5:
        event = db_client.get_event_info(latest_eid)
        if not event:
            latest_eid = 0
            continue

        if set(user_data["interests"]) & set(event['interests']):
            pids.append(random.choice(event["associated_posts"]))

        latest_eid += 1

    # convert pids to posts
    posts = list(map(lambda pid: db_client.get_post_info(pid), pids))

    # cleanup user state
    db_client.set_latest_eid(username, latest_eid)

    return posts
    
