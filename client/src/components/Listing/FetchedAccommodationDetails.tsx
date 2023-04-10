import { FC, useState, useEffect } from "react";
import { DefaultApi } from "@/generated/apis/DefaultApi";
import { AccommodationDetails as AccommodationDetailsModel } from "@/generated/models/AccommodationDetails";
import AccommodationDetails from "./AccommodationDetails";

interface AccommodationDetailsProps {
  listingId: string;
}

const FetchedAccommodationDetails: FC<AccommodationDetailsProps> = ({
  listingId,
}) => {
  const [data, setData] = useState<AccommodationDetailsModel | null>(null);
  const [error, setError] = useState(false);

  useEffect(() => {
    new DefaultApi()
      .apiV1ListingsAccommodationListingIdGet({
        listingId: listingId,
      })
      .then(res => setData(res))
      .catch(() => setError(true));
  }, [listingId]);

  return (
    <div>
      {error ? (
        <p>Error fetching data</p>
      ) : !data ? (
        <p>Loading</p>
      ) : (
        <AccommodationDetails accommodation={data.accommodation} />
      )}
    </div>
  );
};

export default FetchedAccommodationDetails;
