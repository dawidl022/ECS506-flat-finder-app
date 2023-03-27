from flask import Blueprint

bp = Blueprint('listings', __name__)


@bp.route('/')
def index() -> str:
    return "Hello world!"
