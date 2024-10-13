from flask import Blueprint, request
from backend.wtm.db import DatabaseClient
from backend.wtm.util import Responses

db_client = DatabaseClient()
responses = Responses()

feed = Blueprint("feed", __name__,
                    url_prefix="/feed")

@feed.route("/get", methods=["GET"])
def get_feed():
