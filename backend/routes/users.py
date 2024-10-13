from flask import Blueprint, request
from backend.db import DatabaseClient
from backend.util import Responses, deserialize_request_body

db_client = DatabaseClient()
responses = Responses()

createUser_bp = Blueprint("users", __name__,
                          url_prefix="/users")

@createUser_bp.route("/createUser", methods=["POST"])
def createUser():
    payload = deserialize_request_body(request)
    username, password, interests = payload["username"], payload["password"], payload["interests"]
    if db_client.user_exists(username):
        return responses.fail("Username exists. Please try again with a different username.")
    db_client.register_new_user(username, password, interests)
    return responses.success()
