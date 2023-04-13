import { FC, useState, useEffect } from "react";
import InfiniteScroll from "react-infinite-scroll-component";
import {
  ApiV1ListingsAccommodationGetSortByEnum,
  DefaultApi,
} from "@/generated/apis/DefaultApi";
import AccommodationSummaryTile from "@/components/Summary/AccomodationSummaryTile";
import { AccommodationSearchResultsInner } from "@/generated/models/AccommodationSearchResultsInner";
import useApi from "@/hooks/useApi";

interface AccommodationDetailsProps {
  location: string;
  radius: number;
  maxPrice?: number;
  sources?: string[];
  sortBy?: ApiV1ListingsAccommodationGetSortByEnum;
  page?: number;
  size?: number;
}
// 35263013 - 0
// 29646891 - 5
// 38454096 - 11

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
  const [pointer, setPointer] = useState(0);
  const [actualPage, setPage] = useState(page);
  const [endOfResults, setEndOfResults] = useState(false);

  const { apiManager } = useApi();

  const getMoreAccommodation = async () => {
    console.log(`FETCHING: page:${actualPage}, pointer: ${pointer}`);
    apiManager
      .apiV1ListingsAccommodationGet({
        location,
        radius,
        maxPrice,
        sources,
        sortBy,
        page: actualPage,
        size,
      })
      .then(res => {
        if (res.searchResults.length === 0) {
          console.log("end of results");
          setEndOfResults(true);
        }
        setData(prev => {
          const prevIds = prev.map(listing => listing.accommodation.id);
          return [
            ...prev,
            ...res.searchResults.filter(
              result => !prevIds.includes(result.accommodation.id)
            ),
          ];
        });
        setPointer(prev => prev + size);
        setPage(prev => prev + 1);
        console.log("GET FOR PAGE ", actualPage);
      })
      .catch(() => setError(true));
    // page = page + 1;
    // // pointer = pointer + size;
    // setPointer(prev => prev + size);
  };

  useEffect(() => {
    getMoreAccommodation();
  }, []);

  return (
    <div>
      {error ? (
        <p>Error fetching data</p>
      ) : (
        <InfiniteScroll
          dataLength={40000}
          next={getMoreAccommodation}
          hasMore={!endOfResults}
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
