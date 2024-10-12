from flask import Blueprint, request
from backend.db import DatabaseClient
from backend.util import Responses

db_client = DatabaseClient()
responses = Responses()

login_bp = Blueprint("login", __name__)

@login_bp.route("/login", methods=["GET"])
def login(username: str, password: str, interests: list):
    db_client.login(username)
    return responses.success()
