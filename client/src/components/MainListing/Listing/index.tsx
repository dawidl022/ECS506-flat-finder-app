import AccommodationSummaryTile from "@/components/Summary/AccomodationSummaryTile";
import {
  AccommodationSearchResultsInner,
  ApiV1ListingsAccommodationGetSortByEnum,
} from "@/generated";
import useApi from "@/hooks/useApi";
import React, { FC, useCallback, useEffect, useRef, useState } from "react";

import styles from "../MainListing.module.scss";

interface AccommodationDetailsProps {
  location: string;
  radius: number;
  maxPrice?: number;
  sources?: string[];
  sortBy?: ApiV1ListingsAccommodationGetSortByEnum;
  size?: number;
}

const Listing: FC<AccommodationDetailsProps> = ({
  location,
  radius,
  maxPrice,
  sources,
  sortBy,
  size = 9,
}) => {
  const [data, setData] = useState<Array<AccommodationSearchResultsInner>>([]);
  const [isLoading, setIsLoading] = useState(true);
  const { apiManager } = useApi();
  const [pageNumber, setPageNumber] = React.useState(0);
  const [attempts, setAttempts] = React.useState(3);

  const intObserver = useRef<any>(null);
  const hasNextPage = true;

  const lastPostRef = useCallback(
    (item: any) => {
      //   console.log(data);
      if (isLoading) return;

      if (intObserver.current) intObserver.current.disconnect();

      intObserver.current = new IntersectionObserver(data => {
        if (data[0].isIntersecting && hasNextPage) {
          //   console.log("We are near the last post!");
          setPageNumber((prev: number) => prev + 1);
        }
      });

      if (item) intObserver.current.observe(item);
    },
    [isLoading, hasNextPage]
  );

  const getMoreAccommodation = async () => {
    setIsLoading(true);
    // console.log("START LOADING");
    apiManager
      .apiV1ListingsAccommodationGet({
        location,
        radius,
        maxPrice,
        sources,
        sortBy,
        page: pageNumber,
        size,
      })
      .then(res => {
        setData(prev => {
          const prevIds = prev.map(listing => listing.accommodation.id);
          const finalResult = res.searchResults.filter(
            result => !prevIds.includes(result.accommodation.id)
          );
          if (finalResult.length < 3) {
            setPageNumber((prev: number) => prev + 1);
            setAttempts(prev => prev - 1);
          } else {
            setAttempts(3);
          }

          return [...prev, ...finalResult];
        });
      })
      .catch(err => setAttempts(prev => prev - 1))
      .finally(() => {
        setIsLoading(false);
        // console.log("STOP LOADING");
      });
  };

  useEffect(() => {
    if (attempts > 0) {
      //   console.log(attempts);
      getMoreAccommodation();
    }
  }, [pageNumber]);

  if (isLoading) {
    return <h1>Loading...</h1>;
  }

  return (
    <div className={styles.listingWrapper}>
      {data.map((item, index) => {
        return (
          <div key={index}>
            <AccommodationSummaryTile accommodation={item.accommodation} />
          </div>
        );
      })}

      <p ref={lastPostRef}></p>
      {attempts <= 0 && <p>End of results</p>}
    </div>
  );
};

export default Listing;
