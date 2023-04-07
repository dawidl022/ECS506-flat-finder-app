import { FC, useState, FormEvent, ChangeEvent } from "react";
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

  function handleFileInput(e: ChangeEvent<HTMLInputElement>) {
    const files = e.target.files;
    //check if there are more than 15 files selected
    if (files && files.length > 0) {
      if (files.length > 15) {
        alert("You can upload up to 15 files");
        e.target.value = "";
        return;
      }

      //check if the file size is greater than 5MB
      for (let i = 0; i < files.length; i++) {
        if (files[i].size > 5242880) {
          alert(`The maximum file size is 5MB`);
          e.target.value = "";
          return;
        }
      }
    }
  }

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
      .catch(err =>
        alert(
          "Accommodation listing failed to be published. \nError: " +
            err.message
        )
      )
      .then(res => (window.location.href = "/myListings"));
  };

  return (
    <div>
      Accommodation Form
      <form onSubmit={handleSubmit}>
        <label htmlFor="title">Title: </label>
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
          id="description"
          placeholder="Accommodation Description REQUIRED"
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
            placeholder="Accommodation Line 1 REQUIRED"
            value={line1}
            onChange={e => setLine1(e.target.value)}
            required
          />
          <br />
          <label htmlFor="line2">Address Line 2: </label>
          <input
            type="text"
            id="line2"
            placeholder="Accommodation Line 2 OPTIONAL"
            value={line2}
            onChange={e => setLine2(e.target.value)}
          />
          <br />
          <label htmlFor="town">Town: </label>
          <input
            id="town"
            type="text"
            placeholder="Accommodation Town REQUIRED"
            value={town}
            onChange={e => setTown(e.target.value)}
            required
          />
          <br />
          <label htmlFor="postCode">Post Code: </label>
          <input
            type="text"
            id="postCode"
            placeholder="Accommodation Post Code REQUIRED"
            value={postCode}
            onChange={e => setPostCode(e.target.value)}
            required
          />
          <br />
          <label htmlFor="country">Country: </label>
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
        <label htmlFor="price">Price: </label>
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
        <label htmlFor="numberOfRooms">Number of Rooms: </label>
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
