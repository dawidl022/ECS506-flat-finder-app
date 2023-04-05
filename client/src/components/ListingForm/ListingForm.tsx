import { FC, FormEvent, useState } from "react";
import Tabs from "../Tabs";
import { useRouter } from "next/router";
import AccommodationDetails from "../Listing/AccommodationDetails";
import { Configuration, DefaultApi } from "@/generated";
const ListingForm: FC = ({}) => {
  const router = useRouter();
  const { listingType } = router.query;
  const [title, setTitle] = useState("");
  const [location, setLocation] = useState("");
  const [description, setDescription] = useState("");
  const [address, setAddress] = useState("");
  const [accommodationType, setAccommodationType] = useState("");
  const [noOfRooms, setNoOfRooms] = useState(0);
  const [price, setPrice] = useState(0);

  const previewFunc = () => {
    //redirect to preview page and render the AccomodationDetails componen
  };

  const handleSubmit = (e: FormEvent<HTMLElement>) => {
    e.preventDefault();
    new DefaultApi(new Configuration({ basePath: "http://127.0.0.1:5000" }))
      .apiV1ListingsAccommodationPost({
        title,
        description,
        photos: Array<Blob>(),
        accommodationType,
        numberOfRooms: noOfRooms,
        price,
        address: {
          line1: address,
          town: "London",
          postCode: "E1 8QW",
        },
      })
      .then(res => console.log(res));
  };

  return (
    <div>
      {/* "Seeking" and "Accommodation". Based on the outcome, the appropriate form should be rendered. */}
      <Tabs tabs={["Seeking", "Accommodation"]} />

      {listingType === "seeking" && (
        <div>
          Seeking Form
          <form>
            <input
              type="text"
              placeholder="Seeking Title"
              value={title}
              onChange={e => setTitle(e.target.value)}
              required
            />
            <br />
            <input
              type="text"
              placeholder="Seeking Description"
              value={description}
              onChange={e => setDescription(e.target.value)}
              required
            />
            <br />
            <input
              type="text"
              placeholder="Seeking Location"
              value={location}
              onChange={e => setLocation(e.target.value)}
              required
            />
            <br />
            <input type="file" id="photos" />
            <br />
            <button type="button" onClick={previewFunc}>
              Preview
            </button>
            <br />
            <button type="button">Add</button>
          </form>
        </div>
      )}

      {listingType === "accommodation" && (
        <div>
          Accommodation Form
          <form onSubmit={handleSubmit}>
            <input
              type="text"
              placeholder="Accommodation Title"
              value={title}
              onChange={e => setTitle(e.target.value)}
              required
            />
            <br />
            <input
              type="text"
              placeholder="Accommodation Description"
              value={description}
              onChange={e => setDescription(e.target.value)}
              required
            />
            <br />
            <input
              type="text"
              placeholder="Accommodation Address"
              value={address}
              onChange={e => setAddress(e.target.value)}
              required
            />
            <br />
            <input
              type="number"
              placeholder="Accommodation Price"
              value={price}
              onChange={e => setPrice(parseFloat(e.target.value))}
              required
            />
            <br />
            <input
              type="number"
              min="0"
              max="10"
              placeholder="Accommodation Number of Rooms"
              value={noOfRooms}
              onChange={e => setNoOfRooms(parseFloat(e.target.value))}
              required
            />
            <br />
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
            <button type="button" onClick={previewFunc}>
              Preview
            </button>
            <br />
            <button>Add</button>
          </form>
        </div>
      )}
    </div>
  );
};

export default ListingForm;
