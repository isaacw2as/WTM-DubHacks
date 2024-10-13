from flask import Blueprint, request
from backend.wtm.db import DatabaseClient
from backend.wtm.util import Responses, deserialize_request_body

db_client = DatabaseClient()
responses = Responses()

login = Blueprint("login", __name__)

@login.route("/login", methods=["POST"])
def login_user():
    payload = deserialize_request_body(request)
    username, password= payload["username"], payload["password"]
    success = db_client.login(username, password)
    if success:
        return responses.success()
    else: 
        return responses.fail()
