import { FC, FormEvent, useState } from "react";

interface FilterProps {
  sources: { [key: string]: boolean };
  maxPrice: number | null;
  handleApply: (
    source: { [key: string]: boolean },
    maxPrice: number | null
  ) => void;
}

const Filter: FC<FilterProps> = ({ sources, maxPrice, handleApply }) => {
  const [chooseSources, setSource] = useState(sources);
  //set the max price to blank if the prop is null
  const [price, setPrice] = useState(maxPrice ? maxPrice.toString() : "");

  const checkIfOneSourceIsSelected = () => {
    return Object.values(chooseSources).some(value => value);
  };

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    if (!checkIfOneSourceIsSelected()) {
      alert("Please select at least one source.");
      setSource(sources);
    } else {
      //confirm button if price is 0
      if (parseInt(price) === 0) {
        if (confirm("Are you sure you want to set the max price to 0?")) {
          handleApply(chooseSources, parseInt(price) || 0);
        } else {
          handleApply(chooseSources, parseInt(price) || null);
        }
      } else {
        handleApply(chooseSources, parseInt(price));
      }
    }
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <label htmlFor="maxPrice">Max Price: </label>
        <input
          type="number"
          name="maxPrice"
          id="maxPrice"
          value={price}
          min={0}
          onChange={e => setPrice(e.target.value)}
        />

        <fieldset>
          <legend>Sources</legend>
          {sources &&
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
            })}
        </fieldset>
        <button>Apply</button>
      </form>
    </div>
  );
};

export default Filter;
