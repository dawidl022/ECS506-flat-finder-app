import { FC, useState, useEffect } from "react";
import AccommodationDetails from "./AccommodationDetails";
import { Accommodation } from "@/generated";
import useApi from "@/hooks/useApi";
import styles from './AccommodationListing.module.scss';
interface AccommodationDetailsProps {
  listingId: string;
}

const FetchedAccommodationDetails: FC<AccommodationDetailsProps> = ({
  listingId,
}) => {
  const [data, setData] = useState<Accommodation | null>(null);
  const [error, setError] = useState(false);
  const { apiManager } = useApi();

  useEffect(() => {
    apiManager
      .apiV1ListingsAccommodationListingIdGet({
        listingId: listingId,
      })
      .then(res => setData(res))
      .catch(() => setError(true));
  }, [listingId]);

  return (
    <div className={styles.wrapper}>
      {error ? (
        <p>Error fetching data</p>
      ) : !data ? (
        <p>Loading</p>
      ) : (
        <AccommodationDetails accommodation={data} />
      )}
    </div>
  );
};

export default FetchedAccommodationDetails;
