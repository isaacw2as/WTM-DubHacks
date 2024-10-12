from gevent.pywsgi import WSGIServer
from backend.app import create_app
from backend.db import db

URL = "0.0.0.0:69420"

if __name__ == "__main__":
    app = create_app()
    http_server = WSGIServer(URL, app.wsgi_app)
    http_server.serve_forever()