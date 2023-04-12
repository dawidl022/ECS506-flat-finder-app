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

// const Listing: FC<AccommodationDetailsProps> = ({
//   location,
//   radius,
//   maxPrice,
//   sources,
//   sortBy,
//   size = 9,
// })
const Listing: FC<any> = ({
  data,
  isLoading,
  setPageNumber,
  isEnded,
  isFirst,
}) => {
  // const [isEnded, setIsEnded] = React.useState(false);

  return (
    <>
      <div className={styles.listingWrapper}>
        {data.map((item: any, index: number) => {
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
        ) : isEnded ? (
          data.length > 0 ? (
            <p>No more data</p>
          ) : (
            <p>No data</p>
          )
        ) : !isFirst ? (
          <button
            onClick={() => setPageNumber((prev: number) => prev + 1)}
            className={styles.loadBtn}
          >
            Load more
          </button>
        ) : (
          // TODO: Frontend
          <p>Start searching</p>
        )}
      </div>
    </>
  );
};

export default Listing;
