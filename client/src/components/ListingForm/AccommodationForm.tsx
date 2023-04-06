import { FC, useState, FormEvent } from "react";
import { useRouter } from "next/router";
import {
  AccommodationAddressCountryEnum,
  Configuration,
  DefaultApi,
} from "@/generated";

const AccommodationForm: FC = ({}) => {
  const router = useRouter();

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

  const preview = () => {
    router.push({
      pathname: "/AccommodationPreviewPage",
      query: {
        title,
        description,
        line1,
        line2,
        town,
        postCode,
        country,
        accommodationType,
        numberOfRooms,
        price,
      },
    });
  };

  const checkInputs = () => {
    if (
      title &&
      description &&
      line1 &&
      town &&
      postCode &&
      price &&
      numberOfRooms
    ) {
      return true;
    } else {
      return false;
    }
  };

  const handleSubmit = (e: FormEvent<HTMLElement>) => {
    e.preventDefault();
    new DefaultApi(new Configuration({ basePath: "http://127.0.0.1:5000" }))
      .apiV1ListingsAccommodationPost({
        title,
        description,
        photos: Array<Blob>(),
        accommodationType,
        numberOfRooms,
        price,
        address: {
          line1,
          line2,
          town,
          postCode,
          country: AccommodationAddressCountryEnum.Uk,
        },
      })
      .then(res => (window.location.href = "/myListings"));
  };

  return (
    <div>
      Accommodation Form
      <form onSubmit={handleSubmit}>
        <label htmlFor="title">Accommodation Title: </label>
        <input
          type="text"
          placeholder="Accommodation Title"
          value={title}
          onChange={e => setTitle(e.target.value)}
          required
        />
        <br />
        <label htmlFor="description">Accommodation Description: </label>
        <input
          type="text"
          placeholder="Accommodation Description"
          value={description}
          onChange={e => setDescription(e.target.value)}
          required
        />
        <br />
        <label htmlFor="address">Accommodation Address: </label>
        <input
          type="text"
          placeholder="Accommodation Line 1"
          value={line1}
          onChange={e => setLine1(e.target.value)}
          required
        />
        <br />
        <label htmlFor="address">Accommodation Line 2: </label>
        <input
          type="text"
          placeholder="Accommodation Line 2"
          value={line2}
          onChange={e => setLine2(e.target.value)}
        />
        <br />
        <label htmlFor="address">Accommodation Town: </label>
        <input
          type="text"
          placeholder="Accommodation Town"
          value={town}
          onChange={e => setTown(e.target.value)}
          required
        />
        <br />
        <label htmlFor="address">Accommodation Post Code: </label>
        <input
          type="text"
          placeholder="Accommodation Post Code"
          value={postCode}
          onChange={e => setPostCode(e.target.value)}
          required
        />
        <br />
        <label htmlFor="address">Accommodation Country: </label>
        <input
          type="text"
          placeholder="Accommodation Country"
          value={country}
          readOnly
        />
        <br />
        <label htmlFor="price">Accommodation Price: </label>
        <input
          type="number"
          placeholder="Accommodation Price"
          value={price}
          onChange={e => setPrice(parseFloat(e.target.value))}
          min={0}
          required
        />
        <br />
        <label htmlFor="numberOfRooms">Accommodation Number of Rooms: </label>
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
        <input multiple type="file" id="photos" />
        <br />
        {/* disable the button if all required fields are not filled in */}
        <button type="button" onClick={preview} disabled={!checkInputs()}>
          Preview
        </button>
        <br />
        <button>Add</button>
      </form>
    </div>
  );
};

export default AccommodationForm;
