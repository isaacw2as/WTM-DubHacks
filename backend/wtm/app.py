from flask import Flask
from backend.routes.users import users
from backend.routes.login import login
from backend.routes.friends import friends
from backend.routes.events import events

def register_routes(app, routes):
    for route in routes:
        app.register_blueprint(route)

def create_app():  
    app = Flask(__name__)

    register_routes(app, [users, login, friends, events])

    return app


