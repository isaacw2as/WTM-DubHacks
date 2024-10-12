from flask import Blueprint, request
from backend.db import DatabaseClient
from backend.util import Responses

db_client = DatabaseClient()
responses = Responses()

createUser_bp = Blueprint("createUser", __name__)

@createUser_bp.route("/createUser", methods=["POST"])
def createUser(username: str, password: str, interests: list):
    while db_client.user_exists(username):
        # pull new set of username 
        pass
    db_client.register_new_user(username, password, interests)
    return responses.success()
