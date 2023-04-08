import { FC, FormEvent, useState } from "react";
import { Configuration, DefaultApi } from "@/generated";

interface FilterProps {
  sources: { [key: string]: boolean };
  maxPrice: number | null;
  handleApply: (source: { [key: string]: boolean }, maxPrice: number) => void;
}

const Filter: FC<FilterProps> = ({ sources, maxPrice, handleApply }) => {
  const [chooseSources, setSource] = useState(sources);
  //used to ensure that there is always 1 source selected
  const [selectOneSource, setSelected] = useState(false);
  //set the max price to 0 if the prop is null
  const [price, setPrice] = useState(maxPrice || 0);

  const checkIfOneSourceIsSelected = () => {
    const selected = Object.values(chooseSources).some(value => value);
    setSelected(selected);
    return selected;
  };
  
  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    if (!checkIfOneSourceIsSelected()) {
        alert("Please select at least one source.");
        //reset form
        setSource(sources);
    }
    // form submission
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

            <button>Apply</button>
        </form>
    </div>
  );
};

export default Filter;
