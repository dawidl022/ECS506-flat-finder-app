import React, { useEffect, useRef, useState } from "react";

import styles from "./MainListing.module.scss";
import Listing from "./Listing";
import SearchComponent from "../Search/searchComponent";
import Filter from "../Filter/Filter";
import useApi from "@/hooks/useApi";
import {
  AccommodationSearchResultsInner,
  SeekingSearchResultsInner,
} from "@/generated";
import SeekingListing from "./Listing/SeekingListing";

const MainListings = () => {
  const [location, setLocation] = useState("");
  const [radius, setRadius] = useState<number>(1);
  const [sources, setSources] = useState<{ [key: string]: boolean }>({});
  const [maxPrice, setMaxPrice] = useState<number | undefined>();
  const { apiManager } = useApi();
  // const [isSubmitted, setIsSubmitted] = useState(false);

  const [selectedTab, setSelectedTab] = useState(0);
  const tabs = ["Accommodations", "Seeking list"];

  // LISTING
  const [isEnded, setIsEnded] = React.useState(false);
  const [data, setData] = useState<Array<AccommodationSearchResultsInner>>([]);
  const [seekingData, setSeekingData] = useState<
    Array<SeekingSearchResultsInner>
  >([]);

  const [pageNumber, setPageNumber] = React.useState(0);
  const [isLoading, setIsLoading] = useState(false);

  const [isFirst, setIsFirst] = useState(true);

  useEffect(() => {
    apiManager.apiV1SourcesAccommodationGet().then(sources => {
      const tmp = sources.reduce(
        (acc, source) => ({ ...acc, [source]: true }),
        {}
      );
      setSources(tmp);
    });
  }, []);

  useEffect(() => {
    if (pageNumber > 0) getData();
  }, [pageNumber]);

  const applyFilters = (
    sources: { [key: string]: boolean },
    maxPrice?: number
  ) => {
    setSources(sources);
    setMaxPrice(maxPrice);
  };

  const getData = async (setPage?: number) => {
    if (selectedTab === 0) {
      getAccData(setPage);
    } else {
      getSeekingData(setPage);
    }
  };

  const getAccData = async (setPage?: number) => {
    setIsLoading(true);
    setIsFirst(false);
    apiManager
      .apiV1ListingsAccommodationGet({
        location,
        radius: radius || 20,
        maxPrice,
        sources: Object.keys(sources).filter(s => sources[s]),
        sortBy: "newest",
        page: setPage || pageNumber,
        size: 5,
      })
      .then(res => {
        console.log(res);
        if (res.searchResults.length === 0) {
          setIsEnded(true);
        }
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

  const getSeekingData = async (setPage?: number) => {
    setIsLoading(true);
    setIsFirst(false);
    apiManager
      .apiV1ListingsSeekingGet({
        location,
        radius: radius || 20,
        page: setPage || pageNumber,
        size: 15,
      })
      .then(res => {
        console.log("MAIN", res);
        // if (res.length === 0) {
        //   setIsEnded(true);
        // }
        // setSeekingData(prev => {
        //   const prevIds = prev.map(listing => listing.seeking.id);
        //   const finalResult = res.filter(
        //     result => !prevIds.includes(result.seeking.id)
        //   );
        //   return [...prev, ...finalResult];
        // });
      })
      .finally(() => {
        setIsLoading(false);
      });
  };

  const initData = () => {
    setData([]);
    getData(0);
  };

  return (
    <div className={styles.wrapper}>
      <div className={styles.filters}>
        <div className={styles.tabs}>
          {tabs.map((tab, index) => (
            <button
              onClick={() => setSelectedTab(index)}
              key={index}
              className={
                index === selectedTab ? styles.selectedItem : styles.item
              }
            >
              {tab}
            </button>
          ))}
        </div>
        <div className={styles.content}>
          {selectedTab === 0 && (
            <Filter
              sources={sources}
              maxPrice={maxPrice}
              handleApply={applyFilters}
            />
          )}
          <SearchComponent
            location={location}
            setLocation={setLocation}
            radius={radius}
            setRadius={setRadius}
            handleSubmit={initData}
          />
        </div>
      </div>
      <main className={styles.main}>
        {selectedTab === 0 ? (
          <Listing
            isEnded={isEnded}
            data={data}
            isLoading={isLoading}
            setPageNumber={setPageNumber}
            isFirst={isFirst}
          />
        ) : (
          <SeekingListing data={seekingData} />
        )}
      </main>
    </div>
  );
};

export default MainListings;
