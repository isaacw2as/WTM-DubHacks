from flask import Flask
from backend.routes.createUser import createUser_bp
from backend.routes.login import login_bp

def register_routes(app):
    app.register_blueprint(createUser_bp)
    app.register_blueprint(login_bp)

def create_app():  
    app = Flask(__name__)

    register_routes(app)

    return app


