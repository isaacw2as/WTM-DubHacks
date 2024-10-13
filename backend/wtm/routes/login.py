from flask import Blueprint, request
from backend.wtm.db import DatabaseClient
from backend.wtm.util import Responses, deserialize_request_body
from datetime import datetime
from pytz import timezone

db_client = DatabaseClient()
responses = Responses()

login = Blueprint("login", __name__)

@login.route("/login", methods=["POST"])
def login_user():
    payload = deserialize_request_body(request)
    username, password= payload["username"], payload["password"]
    success = db_client.login(username, password)
    if not success:
        return responses.fail()
    return responses.success()

@login.route("/eventsUpdate", methods=["POST"])
def check_pending_events():
    payload = deserialize_request_body(request)
    username = payload["username"]
    user_info = db_client.get_user_info(username)
    pending_eids = user_info["pendingEids"]
    for eid in pending_eids:
        event_info = db_client.get_event_info(eid)
        event_time = datetime.strptime(event_info["timestamp"], "%Y-%m-%dT%H:%M:%S")
        pacific_tz = timezone("US/Pacific")
        event_time = pacific_tz.localize(event_time)
        current_time = datetime.now(tz=pacific_tz)
        if current_time > event_time:
            success = db_client.move_pending_event(username, eid)
            if not success:
                return responses.fail("Failed moving a pending event")
    return responses.success()
        

