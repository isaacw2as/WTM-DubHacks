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
    username = request.args.get("username")
    payload = deserialize_request_body(request)
    # filename = payload["filename"]
    # success = db_client.create_post(pid, username, filename)
    return responses.success()

@posts.route("/comment", methods=["POST"])
def add_comment():
    pid = request.args.get("pid")
    payload = deserialize_request_body(request)
    comment_info = {
        "username": payload["username"],
        "comment": payload["comment"]
    }
    success = db_client.add_comment(pid, comment_info)
    if success:
        return responses.success()
    else:
        return responses.fail()
    
@posts.route("/like", methods=["POST"])
def add_like():
    pid = request.args.get("pid")
    success = db_client.add_like(pid)
    if success:
        return responses.success()
    else:
        return responses.fail()