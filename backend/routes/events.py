from flask import Blueprint, request
from backend.db import DatabaseClient
from backend.util import Responses, deserialize_request_body

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
    datetimestamp = payload["time"]
    description = payload["description"]
    associated_interests = payload["associated_interests"]
    db_client.register_event_under_user(eid=eid,
                                        name=event_name,
                                        loc=location,
                                        datetimestamp=datetimestamp,
                                        description=description,
                                        associated_interests=associated_interests,
                                        organizer_username=username)
    return responses.success()

@events.route("/show", methods=["GET"])
def show_event():
    eid = request.args.get("eid")
    event_info = db_client.get_event_info(eid)
    relevant_info = {
        "name": event_info["name"],
        "location": event_info["loc"],
        "time": event_info["time"],
        "description": event_info["description"],
        "associated_posts": event_info["associated_posts"],
        "organizer_username": event_info["organizer_username"]
    }
    return responses.event_data(relevant_info)