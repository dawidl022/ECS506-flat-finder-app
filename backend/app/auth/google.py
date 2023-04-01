from flask import Blueprint, current_app, url_for
from flask_jwt_extended import jwt_required, get_jwt_identity
from authlib.integrations.flask_client import OAuth

from config import Config

auth_bp = Blueprint('auth', __name__, url_prefix=Config.ROOT)

# Configure OAuth with Google
oauth = OAuth(current_app)
google = oauth.register(
    name='google',
    client_id=Config.GOOGLE_AUTH_CLIENT_ID,
    client_secret=Config.GOOGLE_AUTH_CLIENT_SECRET,
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    userinfo_url='https://www.googleapis.com/oauth2/v1/userinfo',
    jwks_uri="https://www.googleapis.com/oauth2/v3/certs",
    scope='openid email',
)


@auth_bp.route('/login/google')
def google_login():
    redirect_uri = url_for('auth.google_authenticate', _external=True)
    return google.authorize_redirect(redirect_uri)


@auth_bp.route('/authenticate/google')
def google_authenticate():
    token = google.authorize_access_token()
    # TODO register user if they're not already in DB
    return token["id_token"]
    # TODO instead of returning token, redirect to frontend and save the token
    # either in query params, a cookie or in a header


# TODO remove this test endpoint
@auth_bp.route('/protected')
@jwt_required()
def protected_endpoint():
    current_user_id = get_jwt_identity()
    # Do something with the current user ID, like retrieve their data from your database
    # ...
    print(current_user_id)
    return {'message': 'This endpoint is protected with JWT authentication'}
