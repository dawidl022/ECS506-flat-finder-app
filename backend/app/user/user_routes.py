from http.client import FORBIDDEN, NO_CONTENT, NOT_FOUND
from uuid import UUID
from flask import Blueprint, Response, abort, jsonify, make_response
from flask_jwt_extended import jwt_required
from app.auth.jwt import get_current_user_id
from app.user.user_dtos import UserDTO, UserProfileForm
from app.user.user_service import BaseUserService, UserNotFoundError
from app.util.encoding import CamelCaseDecoder, CamelCaseEncoder
from app.util.marshmallow import get_body
from config import Config


bp = Blueprint("users", __name__, url_prefix=f"{Config.ROOT}/users")
bp.json_encoder = CamelCaseEncoder
bp.json_decoder = CamelCaseDecoder


@bp.get("/<uuid:user_id>/profile")
@jwt_required()
def get_user(user_id: UUID, user_service: BaseUserService) -> Response:
    user = user_service.get_user(user_id)

    if user is None:
        abort(make_response({"userId": "user not found"}, NOT_FOUND))

    return jsonify(UserDTO(user))


@bp.put("/<uuid:user_id>/profile")
@jwt_required()
def put_user(user_id: UUID, user_service: BaseUserService) -> Response:
    requester_id = get_current_user_id()

    if user_id != requester_id:
        abort(make_response(
            {"userId": "user not owner of profile"}, FORBIDDEN))

    profile = get_body(UserProfileForm)

    try:
        user_service.update_user(user_id, profile)
    except UserNotFoundError:
        abort(make_response(
            {"userId": "user not found"}, NOT_FOUND))

    return make_response("", NO_CONTENT)
