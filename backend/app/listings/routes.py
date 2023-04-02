from flask import Blueprint, Response, jsonify
from app.listings.models import AccommodationSearchParams
from app.listings.service import ListingsService
from app.util.marshmallow import get_params

from config import Config

bp = Blueprint("listings", __name__)


@bp.get(f"{Config.ROOT}/listings/accommodation")
def get_accommodation_listings(listingsService: ListingsService) -> Response:
    params = get_params(AccommodationSearchParams)

    listings = listingsService.search_accommodation_listings()

    return jsonify(listings)
