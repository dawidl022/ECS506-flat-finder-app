import React, { useEffect, useRef, useState } from "react";
import Pagination from "../Pagination";

import styles from "./MainListing.module.scss";
import Listing from "./Listing";
import SearchComponent from "../Search/searchComponent";
import Filter from "../Filter/Filter";
import useApi from "@/hooks/useApi";

const MainListings = () => {
  const [location, setLocation] = useState("");
  const [radius, setRadius] = useState<number | null>(null);
  const [sources, setSources] = useState<{ [key: string]: boolean }>({});
  const [maxPrice, setMaxPrice] = useState<number | undefined>();
  const { apiManager } = useApi();
  const [isSubmitted, setIsSubmitted] = useState(false);

  useEffect(() => {
    apiManager.apiV1SourcesAccommodationGet().then(sources => {
      const tmp = sources.reduce(
        (acc, source) => ({ ...acc, [source]: true }),
        {}
      );
      setSources(tmp);
    });
  }, []);

  const search = (location: string, radius: number) => {
    setLocation(location);
    setRadius(radius);
    setIsSubmitted(true);
  };

  const applyFilters = (
    sources: { [key: string]: boolean },
    maxPrice?: number
  ) => {
    setSources(sources);
    setMaxPrice(maxPrice);
  };

  return (
    <div className={styles.wrapper}>
      <div className={styles.filters}>
        <Filter
          sources={sources}
          maxPrice={maxPrice}
          handleApply={applyFilters}
        />
        <SearchComponent handleSubmit={search} />
      </div>
      <main className={styles.main}>
        {isSubmitted && (
          <Listing
            sources={Object.keys(sources).filter(s => sources[s])}
            size={9}
            location={location}
            radius={radius ?? 20}
            maxPrice={maxPrice}
          />
        )}
      </main>
    </div>
  );
};

export default MainListings;