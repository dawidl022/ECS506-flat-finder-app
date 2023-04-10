import { FC, useState, useEffect } from "react";
import InfiniteScroll from "react-infinite-scroll-component";
import {
  ApiV1ListingsAccommodationGetSortByEnum,
  DefaultApi,
} from "@/generated/apis/DefaultApi";
import AccommodationSummaryTile from "@/components/Summary/AccomodationSummaryTile";
import { AccommodationSearchResultsInner } from "@/generated/models/AccommodationSearchResultsInner";

interface AccommodationDetailsProps {
  location: string;
  radius: number;
  maxPrice?: number;
  sources?: Array<string>;
  sortBy?: ApiV1ListingsAccommodationGetSortByEnum;
  page?: number;
  size?: number;
}

const InfiniteListings: FC<AccommodationDetailsProps> = ({
  location,
  radius,
  maxPrice,
  sources,
  sortBy,
  page = 0,
  size = 6,
}) => {
  const [data, setData] = useState(Array<AccommodationSearchResultsInner>);
  const [error, setError] = useState(false);

  const getMoreAccommodation = async () => {
    await new DefaultApi()
      .apiV1ListingsAccommodationGet({
        location: location,
        radius: radius,
        maxPrice: maxPrice,
        sources: sources,
        sortBy: sortBy,
        page: page,
        size: size,
      })
      .then(res => {
        setData(data.concat(res));
      })
      .catch(() => setError(true));
    page = page + 1;
  };

  return (
    <div>
      {error ? (
        <p>Error fetching data</p>
      ) : (
        <InfiniteScroll
          dataLength={data.length}
          next={getMoreAccommodation}
          hasMore={data.length !== 10}
          loader={<h4>Loading...</h4>}
          endMessage={
            <p style={{ textAlign: "center" }}>
              <b>End of results</b>
            </p>
          }
        >
          {data.map((data, index) => (
            <div key={index}>
              <AccommodationSummaryTile accommodation={data.accommodation} />
            </div>
          ))}
        </InfiniteScroll>
      )}
    </div>
  );
};

export default InfiniteListings;
