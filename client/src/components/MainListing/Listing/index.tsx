import AccommodationSummaryTile from "@/components/Summary/AccomodationSummaryTile";
import {
  AccommodationSearchResultsInner,
  ApiV1ListingsAccommodationGetSortByEnum,
} from "@/generated";
import useApi from "@/hooks/useApi";
import React, { FC, useCallback, useEffect, useRef, useState } from "react";

import styles from "../MainListing.module.scss";
import LoadingSpinner from "@/components/LoadingSpinner";

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
  // CHANGE
  const [isLoading, setIsLoading] = useState(true);
  const { apiManager } = useApi();
  // const [pageNumber, setPageNumber] = React.useState(0);

  React.useEffect(() => {
    getData();
  }, []);

  const getData = async () => {
    setIsLoading(true);
    apiManager
      .apiV1ListingsAccommodationGet({
        location,
        radius,
        maxPrice,
        sources,
        sortBy,
        page: 0,
        size: 50,
      })
      .then(res => {
        console.log(res);
        setData(prev => {
          const prevIds = prev.map(listing => listing.accommodation.id);
          const finalResult = res.searchResults.filter(
            result => !prevIds.includes(result.accommodation.id)
          );

          return [...prev, ...finalResult];
        });
      })
      .finally(() => {
        setIsLoading(false);
      });
  };

  if (isLoading) {
    return <LoadingSpinner conStyles={{ paddingTop: 120 }} />;
  }

  return (
    <>
      <div className={styles.listingWrapper}>
        {data.map((item, index) => {
          return (
            <div key={index}>
              <AccommodationSummaryTile accommodation={item.accommodation} />
            </div>
          );
        })}
      </div>
      <div className={styles.loadBtnCon}>
        <button className={styles.loadBtn}>Load more</button>
      </div>
    </>
  );
};

export default Listing;
