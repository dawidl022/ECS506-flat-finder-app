import { FC, FormEvent } from "react";

import styles from "./Search.module.scss";

interface Search {
  // handleSubmit: (location: string, radius: number) => void;
  location: string;
  setLocation: (v: string) => void;
  radius: number;
  setRadius: (v: number) => void;
  handleSubmit: () => void;
}

const SearchComponent: FC<Search> = ({
  location,
  setLocation,
  radius,
  setRadius,
  handleSubmit,
}) => {
  const submitInputs = (e: FormEvent) => {
    e.preventDefault();
    handleSubmit();
  };

  return (
    <div className={styles.wrapper}>
      <form onSubmit={submitInputs}>
        <label htmlFor="loc">Location:</label>
        <input
          className={styles.locationInput}
          id="loc"
          type="text"
          placeholder="location"
          value={location}
          onChange={e => setLocation(e.target.value)}
          required
        />
        <label htmlFor="radius">Radius:</label>
        <select
          className={styles.select}
          id="radius"
          value={radius}
          onChange={e => setRadius(parseFloat(e.target.value))}
        >
          <option value={0}>This postcode only</option>
          <option value={0.25}>Within 1/4 km</option>
          <option value={0.5}>Within 1/2 km</option>
          <option defaultChecked value={1}>
            Within 1 km
          </option>
          <option value={3}>Within 3 km</option>
          <option value={5}>Within 5 km</option>
          <option value={10}>Within 10 km</option>
          <option value={15}>Within 15 km</option>
          <option value={20}>Within 20 km</option>
          <option value={30}>Within 30 km</option>
          <option value={40}>Within 40 km</option>
        </select>

        <button type="submit">Search</button>
      </form>
    </div>
  );
};

export default SearchComponent;
