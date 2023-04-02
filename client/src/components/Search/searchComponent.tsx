import { FC, useState, FormEvent } from 'react';

interface Search {
  handleSubmit: (location: string, radius: number) => void;
}

const SearchComponent: FC<Search> = ({ handleSubmit }) => {
  const [location, setTargetLocation] = useState("");
  const [radius, setTargetRadius] = useState(0);
 
  const submitInputs = (e: FormEvent) => {
    e.preventDefault();
    handleSubmit(location, radius);
  };

  return (
    <div>
      <form onSubmit={submitInputs}>
        <label htmlFor="loc">Location:</label>
        <input id="loc" type="text" placeholder="location" value={location} onChange={e => setTargetLocation(e.target.value)} required/>
        <label htmlFor="radius">Radius:</label>
        <select id="radius" value={radius} onChange={e => setTargetRadius(parseFloat(e.target.value))}>
          <option value={0}>This postcode only</option>
          <option value={0.25}>Within 1/4 km</option>
          <option value={0.5}>Within 1/2 km</option>
          <option value={1}>Within 1 km</option>
          <option value={3}>Within 3 km</option>
          <option value={5}>Within 5 km</option>
          <option value={10}>Within 10 km</option>
          <option value={15}>Within 15 km</option>
          <option value={20}>Within 20 km</option>
          <option value={30}>Within 30 km</option>
          <option value={40}>Within 40 km</option>
          <option value={50}>Within 50 km</option>
        </select>

        <button type="submit">Search</button>
      </form>

    </div>
  );
};

export default SearchComponent;
