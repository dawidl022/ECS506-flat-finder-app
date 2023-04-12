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
  const [pageNumber, setPageNumber] = React.useState(0);

  React.useEffect(() => {
    getData();
  }, [pageNumber]);

  const getData = async () => {
    console.log("Started loading ", pageNumber);
    setIsLoading(true);
    apiManager
      .apiV1ListingsAccommodationGet({
        location,
        radius,
        maxPrice,
        sources,
        sortBy,
        page: pageNumber,
        size: 3,
      })
      .then(res => {
        console.log("DATA from api", res);
        setData(prev => {
          const prevIds = prev.map(listing => listing.accommodation.id);
          const finalResult = res.searchResults.filter(
            result => !prevIds.includes(result.accommodation.id)
          );
          console.log(
            `Loaded page ${pageNumber}; loaded: ${finalResult.length}`
          );

          return [...prev, ...finalResult];
        });
      })
      .finally(() => {
        setIsLoading(false);
      });
  };

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
        {isLoading ? (
          <LoadingSpinner conStyles={{ paddingTop: 60 }} />
        ) : (
          <button
            onClick={() => setPageNumber(prev => prev + 1)}
            className={styles.loadBtn}
          >
            Load more
          </button>
        )}
      </div>
    </>
  );
};

export default Listing;
