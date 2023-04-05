import { FC, useState, useEffect } from "react";
import { DefaultApi } from "@/generated/apis/DefaultApi";
import { SeekingDetails as SeekingDetailsModel } from "@/generated/models/SeekingDetails";
import SeekingDetails from "./SeekingDetails";

interface SeekingDetailsProps {
  listingId: string;
}

const FetchedSeekingDetails: FC<SeekingDetailsProps> = ({ listingId }) => {
  const [data, setData] = useState<SeekingDetailsModel | null>(null);
  const [error, setError] = useState(false);

  useEffect(() => {
    new DefaultApi()
      .apiV1ListingsSeekingListingIdGet({
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
        data.seeking && <SeekingDetails seeking={data.seeking} />
      )}
    </div>
  );
};

export default FetchedSeekingDetails;