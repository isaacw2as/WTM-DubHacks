from flask import Blueprint, request
from backend.db import DatabaseClient
from backend.util import Responses, deserialize_request_body

db_client = DatabaseClient()
responses = Responses()

event_bp = Blueprint("events", __name__,
                     url_prefix="/events")

@event_bp.route("/create", methods=["GET"])
def create_event():
    db_client.
    payload = deserialize_request_body(request)