from flask import Blueprint, request
from backend.db import DatabaseClient
from backend.util import Responses

db_client = DatabaseClient()
responses = Responses()

feed = Blueprint("feed", __name__,
                    url_prefix="/feed")

@feed.route("/get", methods=["GET"])
def get_feed():