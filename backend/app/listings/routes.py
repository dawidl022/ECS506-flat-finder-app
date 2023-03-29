from flask import Blueprint, jsonify
from app.listings.models import AccommodationSearchParams, AccommodationSearchResult
from app.util.marshmallow import get_params

from config import Config

bp = Blueprint("listings", __name__)


@bp.route(f"{Config.ROOT}/listings/accommodation")
def get_accommodation_listings():
    params = get_params(AccommodationSearchParams)

    params.location

    return jsonify(AccommodationSearchResult())
