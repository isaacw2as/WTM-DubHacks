from flask import Flask
from backend.wtm.routes.users import users
from backend.wtm.routes.login import login
from backend.wtm.routes.friends import friends
from backend.wtm.routes.events import events

def register_routes(app, routes):
    for route in routes:
        app.register_blueprint(route)

def create_app():  
    app = Flask(__name__)

    register_routes(app, [users, login, friends, events])

    return app


