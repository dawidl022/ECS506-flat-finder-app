from app.listings import bp


@bp.route('/')
def index() -> str:
    return "Hello world!"
