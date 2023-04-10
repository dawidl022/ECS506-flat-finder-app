from http.client import FORBIDDEN, NO_CONTENT, NOT_FOUND
from uuid import UUID
from flask import Blueprint, Response, abort, make_response
from flask_jwt_extended import jwt_required
from app.auth.jwt import get_current_user_id
from app.user.user_exceptions import UserNotFoundError
from app.user.user_routes import check_logged_in_user_is_admin, get_user
from app.user.user_service import AdminService, BaseUserService
from config import Config
from app.util.encoding import CamelCaseDecoder, CamelCaseEncoder


bp = Blueprint("admins", __name__, url_prefix=f"{Config.ROOT}/admins")
bp.json_encoder = CamelCaseEncoder
bp.json_decoder = CamelCaseDecoder


@bp.get("/<uuid:user_id>")
@jwt_required()
def check_if_admin(user_id: UUID, user_service: BaseUserService) -> Response:
    logged_in_user = get_user(user_service, get_current_user_id())

    if not (logged_in_user.id == user_id or logged_in_user.is_admin):
        abort(make_response({"user": "user not authorised"}, FORBIDDEN))

    user = user_service.get_user(user_id)
    if user is not None and user.is_admin:
        return make_response("", NO_CONTENT)
    else:
        return make_response(
            {"user": "user has no admin privileges or does not exist"},
            NOT_FOUND
        )


@bp.put("/<uuid:user_id>")
@jwt_required()
def grant_admin(user_id: UUID, user_service: BaseUserService,
                admin_service: AdminService) -> Response:
    check_logged_in_user_is_admin(user_service)

    try:
        admin_service.grant_admin(user_id)
    except UserNotFoundError:
        abort(make_response({"userId": "user not found"}, NOT_FOUND))

    return make_response("", NO_CONTENT)


@bp.delete("/<uuid:user_id>")
@jwt_required()
def revoke_admin(user_id: UUID, user_service: BaseUserService,
                 admin_service: AdminService) -> Response:
    check_logged_in_user_is_admin(user_service)

    try:
        admin_service.revoke_admin(user_id)
    except UserNotFoundError:
        abort(make_response({"userId": "user not found"}, NOT_FOUND))

    return make_response("", NO_CONTENT)
