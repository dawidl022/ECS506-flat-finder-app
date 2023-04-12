import React, { FC } from "react";

import styles from "../MainListing.module.scss";
import SeekingSummaryTile from "@/components/Summary/SeekingSummaryTile";
import { SeekingSearchResultsInner } from "@/generated";

interface SeekingListingProps {
  data: any[];
}

const SeekingListing: FC<SeekingListingProps> = ({ data }) => {
  return (
    <div className={styles.listingWrapper}>
      {data.map((item, index: number) => {
        return (
          <div key={index}>
            <SeekingSummaryTile seekingAccomodation={item} />
          </div>
        );
      })}
    </div>
  );
};

export default SeekingListing;
