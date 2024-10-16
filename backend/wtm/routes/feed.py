from flask import Blueprint, request
from backend.wtm.db import DatabaseClient
from backend.wtm.util import Responses, deserialize_request_body
from datetime import datetime
import random

db_client = DatabaseClient()
responses = Responses()

feed = Blueprint("feed", __name__,
                    url_prefix="/feed")

@feed.route("/get", methods=["GET"])
def get_feed():
    username = request.args.get("username")
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
                if current_event_info["associated_posts"]:
                    to_add = random.choice(current_event_info["associated_posts"])
                    if to_add in pids:
                        continue
                    pids.append(to_add)

    while len(pids) < 4:
        event = db_client.get_event_info(latest_eid)
        if not event:
            latest_eid = 1
            continue

        try:
            event_time = datetime.strptime(event["timestamp"], "%Y-%m-%dT%H:%M")
        except ValueError as e:
            event_time = datetime.strptime(event["timestamp"], "%Y-%m-%dT%H:%M:%S")

        if datetime.now() > event_time:
            latest_eid += 1
            continue

        if set(user_data["interests"]) & set(event['interests']):
            if not event["associated_posts"]:
                latest_eid += 1
                continue

            to_add = random.choice(event["associated_posts"])
            if to_add in pids:
                latest_eid += 1
                continue
            pids.append(to_add)

        latest_eid += 1

    # convert pids to posts
    posts = list(map(lambda pid: db_client.get_post_info(pid), pids))
    random.shuffle(posts)

    # cleanup user state
    db_client.set_latest_eid(username, latest_eid)

    return responses.json_data(posts)
    
