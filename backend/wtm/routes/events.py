from flask import Blueprint, request
from datetime import datetime
from backend.wtm.db import DatabaseClient
from backend.wtm.util import Responses, deserialize_request_body

db_client = DatabaseClient()
responses = Responses()

events = Blueprint("events", __name__,
                     url_prefix="/events")

@events.route("/create", methods=["POST"])
def create_event():
    eid = db_client.get_largest_eid() + 1
    payload = deserialize_request_body(request)
    username = payload["username"]
    event_name = payload["event_name"]
    location = payload["location"]
    start_timestamp = payload["start_timestamp"]
    description = payload["description"]
    associated_interests = payload["interests"]
    db_client.register_event_under_user(eid=eid,
                                        name=event_name,
                                        loc=location,
                                        start_timestamp=start_timestamp,
                                        description=description,
                                        associated_interests=associated_interests,
                                        organizer_username=username,
                                        )
    return responses.success()

@events.route("/show", methods=["GET"])
def show_event():
    payload = deserialize_request_body(request)
    eid = payload["eid"]
    event_info = db_client.get_event_info(eid)
    relevant_info = {
        "name": event_info["name"],
        "location": event_info["loc"],
        "start_timestamp": event_info["start_timestamp"],
        "end_timestamp": event_info["end_timestamp"],
        "description": event_info["description"],
        "associated_posts": event_info["associated_posts"],
        "organizer_username": event_info["organizer_username"]
    }
    return responses.json_data(relevant_info)