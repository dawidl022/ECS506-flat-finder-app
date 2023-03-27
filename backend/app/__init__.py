from flask import Flask
from config import Config


def create_app(config_class=Config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Flask extensions here

    # Register blueprints
    from app.listings import bp as listings_bp
    app.register_blueprint(listings_bp)

    return app
