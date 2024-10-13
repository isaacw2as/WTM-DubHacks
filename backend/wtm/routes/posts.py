from flask import Blueprint, request
from backend.wtm.db import DatabaseClient
from backend.wtm.util import Responses, deserialize_request_body
from datetime import datetime
from pytz import timezone

db_client = DatabaseClient()
responses = Responses()

posts = Blueprint("posts", __name__,
                         url_prefix="/posts")

@posts.route("/create", methods=["POST"])
def create_post():
    pid = db_client.get_largest_pid() + 1
    payload = deserialize_request_body(request)
    username = payload["username"]
    eid = payload["eid"]
    filename = payload["filename"]
    event_data = db_client.get_event_info(eid)
    event_time = datetime.strptime(event_data["timestamp"], "%Y-%m-%dT%H:%M:%S")
    pacific_tz = timezone("US/Pacific")
    event_time = pacific_tz.localize(event_time)
    current_time = datetime.now(tz=pacific_tz)
    if (current_time < event_time) and (username != event_data["organizer_username"]):
        return responses.fail("Failure: Trying to create post before the event has happened.")
    success_create = db_client.create_post(pid, username, filename)
    success_associate = db_client.associate_post_with_event(eid=eid, pid=pid)
    if not (success_create and success_associate):
        return responses.fail()
    return responses.success()

@posts.route("/comment", methods=["POST"])
def add_comment():
    payload = deserialize_request_body(request)
    pid = payload["pid"]
    comment_info = {
        "username": payload["username"],
        "comment": payload["comment"]
    }
    success = db_client.add_comment(pid, comment_info)
    if not success:
        return responses.fail()
    return responses.success()
    
@posts.route("/like", methods=["POST"])
def add_like():
    payload = deserialize_request_body(request)
    pid = payload["pid"]
    success = db_client.add_like(pid)
    if not success:
        return responses.fail()
    return responses.success()