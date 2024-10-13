from flask import Blueprint, request
from backend.wtm.db import DatabaseClient
from backend.wtm.util import Responses, deserialize_request_body

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
    return responses.fail()
    
@posts.route("/like", methods=["POST"])
def add_like():
    payload = deserialize_request_body(request)
    pid = payload["pid"]
    success = db_client.add_like(pid)
    if not success:
        return responses.fail()
    return responses.success()