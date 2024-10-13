from gevent.pywsgi import WSGIServer
from backend.wtm.app import create_app

URL = "0.0.0.0"
PORT = 42069

if __name__ == "__main__":
    app = create_app()
    http_server = WSGIServer((URL, PORT), app.wsgi_app)
    http_server.serve_forever()