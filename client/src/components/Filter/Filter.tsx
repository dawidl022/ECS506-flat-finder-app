import { FC, FormEvent, useState } from "react";
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

  const checkIfOneSourceIsSelected = () => {
    const selected = Object.values(chooseSources).some(value => value);
    return selected;
  };

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    if (!checkIfOneSourceIsSelected()) {
      alert("Please select at least one source.");
      //reset form
      setSource(sources);
    } else {
      // form submission
      handleApply(chooseSources, price);
    }
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <input
          type="number"
          name="maxPrice"
          id="maxPrice"
          value={price}
          min={0}
          onChange={e => setPrice(parseInt(e.target.value))}
        />

        <fieldset>
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
        </fieldset>
        <button>Apply</button>
      </form>
    </div>
  );
};

export default Filter;
