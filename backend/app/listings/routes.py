from flask import Blueprint, Response, jsonify
from app.listings.models import AccommodationSearchParams, AccommodationSearchResult, AccommodationSummary
from app.util.marshmallow import get_params

from config import Config

bp = Blueprint("listings", __name__)


@bp.route(f"{Config.ROOT}/listings/accommodation")
def get_accommodation_listings() -> Response:
    params = get_params(AccommodationSearchParams)

    return jsonify([
        AccommodationSearchResult(
            distance=1.2,
            is_favourite=True,
            accommodation=AccommodationSummary(
                id="internal-1",
                title="Flat",
                short_description="A very nice flat to live in, beautiful views",
                thumbnail_url="https://fastly.picsum.photos/id/308/1200/1200.jpg?hmac=2c1705rmBMgsQTZ1I9Uu74cRpA4Fxdl0THWV8wfV5VQ",
                accommodation_type="flat",
                number_of_rooms=2,
                source="internal",
                price=1020,
                post_code="EA1 7UP"
            )
        ),
        AccommodationSearchResult(
            distance=1.2,
            is_favourite=False,
            accommodation=AccommodationSummary(
                id="zoopla-1",
                title="Room",
                short_description="A small cozy room, perfect for students",
                thumbnail_url="https://fastly.picsum.photos/id/163/1200/1200.jpg?hmac=ZOvAYvHz98oGUbqnNC_qldUszdxrzrNdmZjkyxzukt8",
                accommodation_type="room",
                number_of_rooms=1,
                source="zoopla",
                price=455.50,
                post_code="ZO1 8N"
            )
        )
    ])
