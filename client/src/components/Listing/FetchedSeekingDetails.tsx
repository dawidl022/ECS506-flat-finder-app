import { FC, useState, useEffect } from "react";
import { DefaultApi } from "@/generated/apis/DefaultApi";
import SeekingDetails from "./SeekingDetails";
import { Seeking } from "@/generated";
import useApi from "@/hooks/useApi";

interface SeekingDetailsProps {
  listingId: string;
}

const FetchedSeekingDetails: FC<SeekingDetailsProps> = ({ listingId }) => {
  const [data, setData] = useState<Seeking | null>(null);
  const [error, setError] = useState(false);
  const { apiManager } = useApi();

  useEffect(() => {
    apiManager
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
        data && <SeekingDetails seeking={data} />
      )}
    </div>
  );
};

export default FetchedSeekingDetails;
