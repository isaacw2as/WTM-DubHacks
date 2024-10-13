import datetime
import json
from typing import Any, Dict
from flask import make_response, Request

class Responses:
    @staticmethod
    def success(data: Any = "success"):
        message = {"response": data}
        return make_response(str(json.dumps(message)), 200)
    
    @staticmethod
    def fail(data: Any = "failure"):
        message = {"response": data}
        return make_response(str(json.dumps(message)), 500)
    
    @staticmethod
    def json_data(data: Any = None):
        return make_response(str(json.dumps(data)), 200)

def deserialize_request_body(post_request: Request) -> Dict:
    return json.loads(post_request.data) if post_request.data else {}