from http import HTTPStatus
from flask import Blueprint, Response

healthz_bp = Blueprint("healthz", __name__)

@healthz_bp.route("/healthz", methods=["GET"])
def healthz() -> Response:
    return Response(
        "ok",
        status=HTTPStatus.OK,
    )