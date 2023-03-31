from app.listings.models import AccommodationSearchResult, AccommodationSummary


class ListingsService():

    def search_accommodation_listings(self) -> list[AccommodationSearchResult]:
        """
        TODO take filters as parameters
        TODO implement business logic
        :returns stub response
        """
        thumbnail_urls = [
            "https://fastly.picsum.photos/id/308/1200/1200"
            ".jpg?hmac=2c1705rmBMgsQTZ1I9Uu74cRpA4Fxdl0THWV8wfV5VQ",
            "https://fastly.picsum.photos/id/163/1200/1200"
            ".jpg?hmac=ZOvAYvHz98oGUbqnNC_qldUszdxrzrNdmZjkyxzukt8",
        ]
        return [
            AccommodationSearchResult(
                distance=1.2,
                is_favourite=True,
                accommodation=AccommodationSummary(
                    id="internal-1",
                    title="Flat",
                    short_description="Very nice beautiful flat to live in",
                    thumbnail_url=thumbnail_urls[0],
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
                    short_description="A small cozy room perfect for students",
                    thumbnail_url=thumbnail_urls[1],
                    accommodation_type="room",
                    number_of_rooms=1,
                    source="zoopla",
                    price=455.50,
                    post_code="ZO1 8N"
                )
            )
        ]
