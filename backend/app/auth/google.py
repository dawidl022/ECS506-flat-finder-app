import datetime
import time
from uuid import UUID
from flask import Blueprint, current_app, make_response, redirect, url_for
from authlib.integrations.flask_client import OAuth
import jwt
from app.user.user_service import BaseUserService

from config import Config

auth_bp = Blueprint('auth', __name__, url_prefix=Config.ROOT)

# Configure OAuth with Google
oauth = OAuth(current_app)
google = oauth.register(
    name='google',
    client_id=Config().GOOGLE_AUTH_CLIENT_ID,
    client_secret=Config().GOOGLE_AUTH_CLIENT_SECRET,
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    userinfo_url='https://www.googleapis.com/oauth2/v1/userinfo',
    jwks_uri="https://www.googleapis.com/oauth2/v3/certs",
    scope='openid email',
)


@auth_bp.post('/login/google')
def google_login():
    redirect_uri = url_for('auth.google_authenticate', _external=True)
    return google.authorize_redirect(redirect_uri)


@auth_bp.route('/authenticate/google')
def google_authenticate(user_service: BaseUserService):
    # TODO check for errors, handle gracefully with redirect to frontend
    token = google.authorize_access_token()

    user_email = token["userinfo"]["email"]
    user_id = user_service.get_user_id_for_email(user_email)

    response = make_response(redirect(Config().FRONTEND_URL))
    response.set_cookie(
        "token", create_jwt_token(user_email=user_email, user_id=user_id)
    )  # can set explicit domain if frontend/backend domains differ
    return response


def create_jwt_token(user_email: str, user_id: UUID) -> str:
    payload = {
        "sub": str(user_id),
        "email": user_email,
    }

    return jwt.encode(payload, Config().JWT_SECRET_KEY)
