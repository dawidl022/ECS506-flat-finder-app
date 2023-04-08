from http.client import NOT_FOUND
from uuid import UUID
from flask import Blueprint, Response, abort, jsonify, make_response
from app.user.user_model import UserDTO
from app.user.user_service import BaseUserService
from app.util.encoding import CamelCaseDecoder, CamelCaseEncoder
from config import Config


bp = Blueprint("users", __name__, url_prefix=f"{Config.ROOT}/users")
bp.json_encoder = CamelCaseEncoder
bp.json_decoder = CamelCaseDecoder


@bp.get("/<uuid:user_id>/profile")
def get_user(user_id: UUID, user_service: BaseUserService) -> Response:
    user = user_service.get_user(user_id)

    if user is None:
        abort(make_response({"userId": "user not found"}, NOT_FOUND))

    return jsonify(UserDTO(user))
