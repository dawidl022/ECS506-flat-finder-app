import { FC, useState, FormEvent, ChangeEvent } from "react";
import { useRouter } from "next/router";
import { handleFileInput } from "./handleFileInput";
import {
  AccommodationAddressCountryEnum,
  Configuration,
  DefaultApi,
} from "@/generated";

interface FormProps {
  listingId: string | "";
  editExistingListing: Boolean;
}

const AccommodationForm: FC<FormProps> = ({ listingId, editable }) => {
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

  const api = new DefaultApi(
    new Configuration({ basePath: "http://127.0.0.1:5000" })
  );

  if (editable) {
    api
      .apiV1ListingsAccommodationListingIdGet({ listingId })
      .then(res => {
        setTitle(res.accommodation.title);
        setDescription(res.accommodation.description);
        setLine1(res.accommodation.address.line1);
        //as line2 is optional, check if there is an input
        res.accommodation.address.line2
          ? setLine2(res.accommodation.address.line2)
          : setLine2("");
        setTown(res.accommodation.address.town);
        setPostCode(res.accommodation.address.postCode);
        setAccommodationType(res.accommodation.accommodationType);
        setNumberOfRooms(res.accommodation.numberOfRooms);
        setPrice(res.accommodation.price);
      })
      .catch(err => {
        alert(`Could not find listing with ID:  ${listingId} \nError:  ${err}`);
      });
  }

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
    if (!editable) {
      api
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
        .catch(err =>
          alert(
            "Accommodation listing failed to be published. \nError: " +
              err.message
          )
        )
        .then(res => router.push({ pathname: "/myListings" }));
    } else {
      api
        .apiV1ListingsAccommodationListingIdPut({
          listingId,
          accommodationFormBase: {
            title,
            description,
            address: {
              line1,
              line2,
              town,
              postCode,
              country: AccommodationAddressCountryEnum.Uk,
            },
            accommodationType,
            numberOfRooms,
            price,
          },
        })
        .then(res => {
          console.log(res);
        })
        .catch(err => {
          alert("Error whilst updating listing. \nError: " + err);
        });
    }
  };

  return (
    <div>
      Accommodation Form
      <form onSubmit={handleSubmit}>
        <label htmlFor="title">Title: </label>
        <input
          type="text"
          placeholder="Title REQUIRED"
          value={title}
          onChange={e => setTitle(e.target.value)}
          required
        />
        <br />

        <label htmlFor="description">Description</label>
        <textarea
          rows={15}
          cols={30}
          id="description"
          placeholder="Description REQUIRED"
          value={description}
          onChange={e => setDescription(e.target.value)}
          required
        />
        <br />

        <fieldset>
          <legend>Address</legend>
          <label htmlFor="line1">Address Line 1: </label>
          <input
            id="line1"
            type="text"
            placeholder="Line 1 REQUIRED"
            value={line1}
            onChange={e => setLine1(e.target.value)}
            required
          />
          <br />
          <label htmlFor="line2">Address Line 2: </label>
          <input
            type="text"
            id="line2"
            placeholder="Line 2 OPTIONAL"
            value={line2}
            onChange={e => setLine2(e.target.value)}
          />
          <br />
          <label htmlFor="town">Town: </label>
          <input
            id="town"
            type="text"
            placeholder="Town REQUIRED"
            value={town}
            onChange={e => setTown(e.target.value)}
            required
          />
          <br />
          <label htmlFor="postCode">Post Code: </label>
          <input
            type="text"
            id="postCode"
            placeholder="Post Code REQUIRED"
            value={postCode}
            onChange={e => setPostCode(e.target.value)}
            required
          />
          <br />
          <label htmlFor="country">Country: </label>
          <input
            type="text"
            id="country"
            placeholder="Country REQUIRED"
            value={country}
            readOnly
            disabled={true}
          />
        </fieldset>
        <br />
        <label htmlFor="price">Price: </label>
        <input
          type="number"
          id="price"
          placeholder="Price REQUIRED"
          value={price}
          onChange={e => setPrice(parseFloat(e.target.value))}
          min={0}
          required
        />
        <br />
        <label htmlFor="numberOfRooms">Number of Rooms: </label>
        <input
          type="number"
          id="numberOfRooms"
          placeholder="Number of Rooms REQUIRED"
          value={numberOfRooms}
          onChange={e => setNumberOfRooms(parseFloat(e.target.value))}
          min={0}
          max={10}
          required
        />
        <br />
        <label htmlFor="type">Type: </label>
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
        <label htmlFor="photos">Photos:{""}</label>
        <input
          type="file"
          onChange={handleFileInput}
          id="photos"
          accept="image/*"
          multiple
        />
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
