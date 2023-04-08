import { FC, useState } from "react";
import { Configuration, DefaultApi } from "@/generated";

interface FilterProps {
  sources: { [key: string]: boolean };
  maxPrice: number | null;
  handleApply: (source: { [key: string]: boolean }, maxPrice: number) => void;
}

const Filter: FC<FilterProps> = ({ sources, maxPrice, handleApply }) => {
  const [chooseSources, setSource] = useState(sources);
  //set the max price to 0 if the prop is null
  const [price, setPrice] = useState(maxPrice || 0);
  return (
    <div>
      <input
        type="number"
        name="maxPrice"
        id="maxPrice"
        value={price}
        min={0}
        onChange={e => setPrice(parseInt(e.target.value))}
      />
      {
        /* creating a checkbox per source by mapping the dictionary */ sources &&
          Object.keys(sources).map((source, index) => {
            return (
              <div key={index}>
                <label htmlFor={source}>{source} </label>
                <input
                  type="checkbox"
                  name={source}
                  id={source}
                  checked={chooseSources[source]}
                  onChange={() =>
                    setSource({
                      ...chooseSources,
                      [source]: !chooseSources[source],
                    })
                  }
                />
              </div>
            );
          })
      }

      <button onClick={() => handleApply(chooseSources, price)}>Apply</button>
    </div>
  );
};

export default Filter;
