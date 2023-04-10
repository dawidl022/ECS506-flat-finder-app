from flask import Blueprint, Response, jsonify
from flask_jwt_extended import jwt_required
from config import Config
from app.listings.service import BaseListingsService
from app.util.encoding import CamelCaseDecoder, CamelCaseEncoder

bp = Blueprint("sources", __name__, url_prefix=f"{Config.ROOT}/sources")
bp.json_encoder = CamelCaseEncoder
bp.json_decoder = CamelCaseDecoder

@bp.get("/accommodation")
@jwt_required()
def get_available_sources(location_query : str, listings_service: BaseListingsService
                        ) -> Response:
    
    sources = listings_service.get_available_sources(location_query)

    return jsonify(sources)