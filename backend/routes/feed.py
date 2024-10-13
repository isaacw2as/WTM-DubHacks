from flask import Blueprint, request
from backend.db import DatabaseClient
from backend.util import Responses

db_client = DatabaseClient()
responses = Responses()

feed_bp = Blueprint("feed", __name__,
                    url_prefix="/feed")

@feed_bp.route("/feed", methods=["GET"])
def feed():