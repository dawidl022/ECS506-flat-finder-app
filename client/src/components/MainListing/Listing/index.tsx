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
const Listing: FC<any> = ({ data, isLoading }) => {
  // const [data, setData] = useState<Array<AccommodationSearchResultsInner>>([]);
  // CHANGE
  // const [isLoading, setIsLoading] = useState(true);
  // const { apiManager } = useApi();
  const [pageNumber, setPageNumber] = React.useState(0);
  const [isEnded, setIsEnded] = React.useState(false);

  // React.useEffect(() => {
  //   getData();
  // }, [pageNumber]);

  // React.useEffect(() => {
  //   setPageNumber(0);
  //   setIsEnded(false);
  // }, [location, radius, maxPrice, sources, sortBy]);

  // const getData = async () => {
  //   setIsLoading(true);
  //   apiManager
  //     .apiV1ListingsAccommodationGet({
  //       location,
  //       radius,
  //       maxPrice,
  //       sources,
  //       sortBy,
  //       page: pageNumber,
  //       size: 15,
  //     })
  //     .then(res => {
  //       if (res.searchResults.length === 0) {
  //         // alert("No");
  //         setIsEnded(true);
  //       }
  //       setData(prev => {
  //         const prevIds = prev.map(listing => listing.accommodation.id);
  //         const finalResult = res.searchResults.filter(
  //           result => !prevIds.includes(result.accommodation.id)
  //         );
  //         return [...prev, ...finalResult];
  //       });
  //     })
  //     .finally(() => {
  //       setIsLoading(false);
  //     });
  // };

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
          <p>No more data</p>
        ) : (
          <button
            // onClick={() => setPageNumber(prev => prev + 1)}
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
