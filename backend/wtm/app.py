from flask import Flask
from flask_cors import CORS
from gevent.pywsgi import WSGIServer
from backend.wtm.routes.users import users
from backend.wtm.routes.login import login
from backend.wtm.routes.friends import friends
from backend.wtm.routes.events import events
from backend.wtm.routes.upload_files import upload_files

URL = "0.0.0.0"
PORT = 42069

def register_routes(app, routes):
    for route in routes:
        app.register_blueprint(route)

def create_app():  
    app = Flask(__name__)
    CORS(app)

    register_routes(app, [users, login, friends, events, upload_files])

    return app

if __name__ == "__main__":
    app = create_app()
    http_server = WSGIServer((URL, PORT), app.wsgi_app)
    print(f"Started server on port {PORT}")
    http_server.serve_forever()

