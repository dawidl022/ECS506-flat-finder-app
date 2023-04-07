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
        <label htmlFor="title" id="titleText">
          Title
        </label>
        <input
          type="text"
          id="title"
          placeholder="Accommodation Title REQUIRED"
          value={title}
          onChange={e => setTitle(e.target.value)}
          required
        />
        <br />
        <label htmlFor="description" id="descriptionText">
          Description
        </label>
        <textarea
          rows={15}
          cols={30}
          id="description"
          placeholder="Accommodation Description REQUIRED"
          value={description}
          onChange={e => setDescription(e.target.value)}
          required
        />
        <br />
        <fieldset>
          <legend>Address</legend>
          <label htmlFor="line1" id="line1Text">
            Address Line 1:{" "}
          </label>
          <input
            id="line1"
            type="text"
            placeholder="Accommodation Line 1 REQUIRED"
            value={line1}
            onChange={e => setLine1(e.target.value)}
            required
          />
          <br />
          <label htmlFor="line2" id="line2Text">
            Address Line 2:{" "}
          </label>
          <input
            type="text"
            id="line2"
            placeholder="Accommodation Line 2 OPTIONAL"
            value={line2}
            onChange={e => setLine2(e.target.value)}
          />
          <br />
          <label htmlFor="town" id="townText">
            Town:{" "}
          </label>
          <input
            id="town"
            type="text"
            placeholder="Accommodation Town REQUIRED"
            value={town}
            onChange={e => setTown(e.target.value)}
            required
          />
          <br />
          <label htmlFor="postCode" id="postCodeText">
            Post Code:{" "}
          </label>
          <input
            type="text"
            id="postCode"
            placeholder="Accommodation Post Code REQUIRED"
            value={postCode}
            onChange={e => setPostCode(e.target.value)}
            required
          />
          <br />
          <label htmlFor="country" id="countryText">
            Country:{" "}
          </label>
          <input
            type="text"
            id="country"
            placeholder="Accommodation Country REQUIRED"
            value={country}
            readOnly
            disabled={true}
          />
        </fieldset>
        <br />
        <label htmlFor="price" id="priceText">
          Price:{" "}
        </label>
        <input
          type="number"
          id="price"
          placeholder="Accommodation Price REQUIRED"
          value={price}
          onChange={e => setPrice(parseFloat(e.target.value))}
          min={0}
          required
        />
        <br />
        <label htmlFor="numberOfRooms" id="roomsText">
          Number of Rooms:{" "}
        </label>
        <input
          type="number"
          id="numberOfRooms"
          placeholder="Accommodation Number of Rooms REQUIRED"
          value={numberOfRooms}
          onChange={e => setNumberOfRooms(parseFloat(e.target.value))}
          min={0}
          max={10}
          required
        />
        <br />
        <label htmlFor="type" id="typeText">
          Accommodation Type:{" "}
        </label>
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
        <label htmlFor="photos" id="photosText">
          Photos:{" "}
        </label>
        <input type="file" placeholder="Import Photos REQUIRED" id="photos" />
        <br />
        <button>Preview</button>
        <br />
        <button>Add</button>
      </form>
    </div>
  );
};

export default AccommodationForm;
