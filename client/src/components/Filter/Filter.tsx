import { FC, FormEvent, useEffect, useState } from "react";

import styles from "./Filter.module.scss";

interface FilterProps {
  sources: { [key: string]: boolean };
  maxPrice?: number;
  handleApply: (sources: { [key: string]: boolean }, maxPrice?: number) => void;
}

const Filter: FC<FilterProps> = ({ sources, maxPrice, handleApply }) => {
  const [chooseSources, setSource] = useState<{ [key: string]: boolean }>({});
  //set the max price to blank if the prop is null
  const [price, setPrice] = useState(maxPrice ? maxPrice.toString() : "");

  useEffect(() => {
    handleApply(chooseSources, parseInt(price) || undefined);
  }, [chooseSources, price]);

  useEffect(() => {
    if (Object.keys(sources).length > 0) {
      setSource(sources);
    }
  }, [sources]);

  return (
    <div className={styles.wrapper}>
      <form onSubmit={e => e.preventDefault()}>
        <label className={styles.maxPriceLabel} htmlFor="maxPrice">
          Max Price:{" "}
        </label>
        <input
          className={styles.maxPriceInput}
          type="number"
          name="maxPrice"
          id="maxPrice"
          value={price}
          min={0}
          onChange={e => setPrice(e.target.value)}
        />

        <fieldset>
          <legend>Sources</legend>
          {chooseSources &&
            Object.keys(chooseSources).map((source, index) => {
              return (
                <div key={index}>
                  <label htmlFor={source}>{source} </label>
                  <input
                    type="checkbox"
                    name={source}
                    id={source}
                    checked={chooseSources[source]}
                    className={styles.checkbox}
                    onChange={() =>
                      setSource({
                        ...chooseSources,
                        [source]: !chooseSources[source],
                      })
                    }
                  />
                </div>
              );
            })}
        </fieldset>
      </form>
    </div>
  );
};

export default Filter;
