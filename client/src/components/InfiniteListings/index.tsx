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
  sources?: string[];
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
  const [data, setData] = useState<Array<AccommodationSearchResultsInner>>([]);
  const [error, setError] = useState(false);
  var pointer = 0;

  const getMoreAccommodation = async () => {
    await new DefaultApi()
      .apiV1ListingsAccommodationGet({
        location,
        radius,
        maxPrice,
        sources,
        sortBy,
        page,
        size,
      })
      .then(res => {
        setData(res.searchResults);
      })
      .catch(() => setError(true));
    page = page + 1;
    pointer = pointer + size;
  };

  useEffect(() => {
    getMoreAccommodation();
  })

  return (
    <div>
      {error ? (
        <p>Error fetching data</p>
      ) : (
        <InfiniteScroll
          dataLength={data.length}
          next={getMoreAccommodation}
          hasMore={pointer <= data.length}
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