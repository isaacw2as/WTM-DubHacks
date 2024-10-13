from flask import Blueprint, request, send_file
from backend.wtm.db import DatabaseClient
from backend.wtm.util import Responses, deserialize_request_body
import random

db_client = DatabaseClient()
responses = Responses()

upload_files = Blueprint("upload_files", __name__, url_prefix="/upload_files")

@upload_files.route("/upload", methods=["POST"])
def upload():
    file = request.files['file']
    if not file:
        return responses.fail()
    
    filename = str(random.randint(0, 99999999999)) + file.filename
    print(filename)
    with db_client.fs.new_file(filename=filename) as f:
        f.write(file.stream.read())

    return responses.success()

@upload_files.route("/download")
def download():
    filename = request.args.get("filename")
    file = db_client.fs.find_one({"filename": filename})
    print(file)
    if file:
        return file
    
    return "file not found"

