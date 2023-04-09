from http.client import UNAUTHORIZED
from uuid import UUID
from flask import abort, make_response
from flask_jwt_extended import get_jwt, get_jwt_identity


def get_current_user_email() -> str:
    """
    get user email from JWT token in header of request
    """
    current_user_email = get_jwt().get("email")

    if current_user_email is None:
        abort(make_response(
            {'token': "invalid bearer token"}, UNAUTHORIZED))

    return current_user_email


def get_current_user_id() -> UUID:
    """
    get user id from JWT token in header of request
    """
    current_user_id = get_jwt_identity()

    if current_user_id is None:
        abort(make_response(
            {'token': "invalid bearer token"}, UNAUTHORIZED))

    return UUID(current_user_id)
