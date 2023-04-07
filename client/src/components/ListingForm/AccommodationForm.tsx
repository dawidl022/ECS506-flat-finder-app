import { FC, useState } from "react";

const AccommodationForm: FC = ({}) => {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [line1, setLine1] = useState("");
  const [line2, setLine2] = useState("");
  const [town, setTown] = useState("");
  const [postCode, setPostCode] = useState("");
  const [country] = useState("United Kingdom");

  const [accommodationType, setAccommodationType] = useState("");
  const [numberOfRooms, setNumberOfRooms] = useState(0);
  const [price, setPrice] = useState(0);

  return (
    <div>
      Accommodation Form
      <form>
        <label htmlFor="title">Title</label>
        <input
          type="text"
          placeholder="Accommodation Title"
          value={title}
          onChange={e => setTitle(e.target.value)}
          required
        />
        <br />
        <label htmlFor="description">Description</label>
        <textarea
          rows={15}
          cols={30}
          placeholder="Accommodation Description"
          value={description}
          onChange={e => setDescription(e.target.value)}
          required
        />
        <br />
        <label htmlFor="line1">Address Line 1: </label>
        <fieldset>
          <input
            type="text"
            placeholder="Accommodation Line 1"
            value={line1}
            onChange={e => setLine1(e.target.value)}
            required
          />
          <br />
          <label htmlFor="line2">Address Line 2: </label>
          <input
            type="text"
            placeholder="Accommodation Line 2"
            value={line2}
            onChange={e => setLine2(e.target.value)}
          />
          <br />
          <label htmlFor="town">Town: </label>
          <input
            type="text"
            placeholder="Accommodation Town"
            value={town}
            onChange={e => setTown(e.target.value)}
            required
          />
          <br />
          <label htmlFor="postCode">Post Code: </label>
          <input
            type="text"
            placeholder="Accommodation Post Code"
            value={postCode}
            onChange={e => setPostCode(e.target.value)}
            required
          />
          <br />
          <label htmlFor="country">Country: </label>
          <input
            type="text"
            placeholder="Accommodation Country"
            value={country}
            readOnly
          />
        </fieldset>
        <br />
        <label htmlFor="price">Price: </label>
        <input
          type="number"
          placeholder="Accommodation Price"
          value={price}
          onChange={e => setPrice(parseFloat(e.target.value))}
          min={0}
          required
        />
        <br />
        <label htmlFor="numberOfRooms">Number of Rooms: </label>
        <input
          type="number"
          placeholder="Accommodation Number of Rooms"
          value={numberOfRooms}
          onChange={e => setNumberOfRooms(parseFloat(e.target.value))}
          min={0}
          max={10}
          required
        />
        <br />
        <label htmlFor="type">Accommodation Type: </label>
        <select
          id="type"
          value={accommodationType}
          onChange={e => setAccommodationType(e.target.value)}
        >
          <option value={"Detached"}>Detached House</option>
          <option value={"Semi-detached"}>Semi-detached House</option>
          <option value={"Terraced"}>Terraced House</option>
          <option value={"Flats"}>Flats</option>
          <option value={"Bungalows"}>Bungalows</option>
        </select>
        <br />
        <input type="file" id="photos" />
        <br />
        <button>Preview</button>
        <br />
        <button>Add</button>
      </form>
    </div>
  );
};

export default AccommodationForm;
