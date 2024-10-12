import datetime
import json
from typing import Any
from flask import make_response, request

class Responses:
    @staticmethod
    def success(data: Any = "success"):
        message = {"error": "",
                   "response": data}
        return make_response(str(json.dumps(message)), 200)
        