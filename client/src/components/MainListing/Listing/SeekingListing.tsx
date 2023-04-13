import React, { FC } from "react";

import styles from "../MainListing.module.scss";
import SeekingSummaryTile from "@/components/Summary/SeekingSummaryTile";
import { SeekingSearchResultsInner } from "@/generated";
import LoadingSpinner from "@/components/LoadingSpinner";

interface SeekingListingProps {
  data: SeekingSearchResultsInner[];
  isEnded: boolean;
  isLoading: boolean;
  isFirst: boolean;
  setPageNumber: any;
}

const SeekingListing: FC<SeekingListingProps> = ({
  data,
  isEnded,
  isLoading,
  isFirst,
  setPageNumber,
}) => {
  return (
    <>
      <div className={styles.listingWrapper}>
        {data.map((item, index: number) => {
          return (
            <div key={index}>
              <SeekingSummaryTile seekingAccomodation={item.seeking} />
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
          <div className={styles.txtCon}>
            <h1>Press search to get results</h1>
          </div>
        )}
      </div>
    </>
  );
};

export default SeekingListing;
