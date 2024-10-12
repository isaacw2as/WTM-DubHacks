from flask import Blueprint, request
from backend.db import DatabaseClient
from backend.util import Responses, deserialize_request_body

db_client = DatabaseClient()
responses = Responses()

login_bp = Blueprint("login", __name__)

@login_bp.route("/login", methods=["POST"])
def login():
    payload = deserialize_request_body(request)
    username, password= payload["username"], payload["password"]
    success = db_client.login(username, password)
    if success:
        return responses.success()
    else: 
        return responses.fail()
