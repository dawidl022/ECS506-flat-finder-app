from flask import Flask
from app.util.encoding import CamelCaseEncoder
from config import Config


def create_app(config_class=Config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.json_encoder = CamelCaseEncoder

    # Initialize Flask extensions here

    # Register blueprints
    from app.listings import listings_bp
    app.register_blueprint(listings_bp)

    return app
