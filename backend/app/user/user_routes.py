from http.client import FORBIDDEN, NO_CONTENT, NOT_FOUND
from uuid import UUID
from flask import Blueprint, Response, abort, jsonify, make_response
from flask_jwt_extended import jwt_required
from app.auth.jwt import get_current_user_id
from app.listings.dtos import ListingSummaryDTO
from app.listings.service import BaseListingsService
from app.user.user_dtos import UserDTO, UserProfileForm, UserSummaryDTO
from app.user.user_models import User
from app.user.user_service import BaseUserService, UserNotFoundError
from app.util.encoding import CamelCaseDecoder, CamelCaseEncoder
from app.util.marshmallow import get_body
from config import Config


bp = Blueprint("users", __name__, url_prefix=f"{Config.ROOT}/users")
bp.json_encoder = CamelCaseEncoder
bp.json_decoder = CamelCaseDecoder


@bp.get("")
@jwt_required()
def get_users(user_service: BaseUserService) -> Response:
    check_logged_in_user_is_admin(user_service)

    return jsonify([
        UserSummaryDTO(user)
        for user in user_service.get_all_users()
    ])


@bp.delete("/<uuid:user_id>")
@jwt_required()
def delete_user(user_id: UUID, user_service: BaseUserService) -> Response:
    check_logged_in_user_is_admin(user_service)

    try:
        user_service.deregister_user(user_id)
    except UserNotFoundError:
        abort(make_response(
            {"userId": "user not found"}, NOT_FOUND))

    return make_response("", NO_CONTENT)


def check_logged_in_user_is_admin(user_service) -> None:
    user = get_user(user_service, get_current_user_id())

    if not user.is_admin:
        abort(make_response({"user": "user not authorised"}, FORBIDDEN))


@bp.get("/<uuid:user_id>/profile")
@jwt_required()
def get_user_profile(user_id: UUID, user_service: BaseUserService) -> Response:
    user = get_user(user_service, user_id)

    return jsonify(UserDTO(user))


@bp.put("/<uuid:user_id>/profile")
@jwt_required()
def put_user_profile(user_id: UUID, user_service: BaseUserService) -> Response:
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


@bp.get("/<uuid:user_id>/listings")
@jwt_required()
def get_user_listings(
    user_id: UUID, listings_service: BaseListingsService,
    user_service: BaseUserService
) -> Response:
    user = get_user(user_service, user_id)

    listings = listings_service.get_listings_authored_by(user.email)

    return jsonify([
        ListingSummaryDTO(listing)
        for listing in listings
    ])


def get_user(user_service, user_id) -> User:
    user = user_service.get_user(user_id)

    if user is None:
        abort(make_response({"userId": "user not found"}, NOT_FOUND))

    return user
