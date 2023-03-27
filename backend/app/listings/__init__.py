from flask import Blueprint

bp = Blueprint('listings', __name__)

from app.listings import routes