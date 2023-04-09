import { FC, useState, FormEvent, ChangeEvent } from "react";
import { useRouter } from "next/router";
import { Configuration, DefaultApi } from "@/generated";
import { handleFileInput } from "./handleFileInput";

interface FormProps {
  listingId: string | "";
  editExistingListing: Boolean;
}

const SeekingForm: FC<FormProps> = ({ listingId, editExistingListing }) => {
  const router = useRouter();
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [location, setLocation] = useState("");
  const api = new DefaultApi(
    new Configuration({ basePath: "http://127.0.0.1:5000" })
  );

  const baseForm = {
    title,
    description,
    preferredLocation: location
  };

  if (editExistingListing) {
    api
      .apiV1ListingsSeekingListingIdGet({ listingId })
      .then(res => {
        setTitle(res.seeking.title);
        setDescription(res.seeking.description);
        setLocation(res.seeking.preferredLocation.name);
      })
      .catch(err => {
        alert(`Could not find listing with ID:  ${listingId} \nError:  ${err}`);
      });
  }
  const preview = () => {
    router.push({
      pathname: "/SeekingPreviewPage",
      query: {
        title,
        description,   
        location,
      },
    });
  };

  const checkInputs = () => {
    if (title && description && location) {
      return true;
    } else {
      return false;
    }
  };

  const handleSubmit = (e: FormEvent<HTMLElement>) => {
    e.preventDefault();
    if (!editExistingListing) {
      api
        .apiV1ListingsSeekingPost({
          ...baseForm,
          photos: Array<Blob>(),
        })
        .catch(err =>
          alert(
            "Seeking listing failed to be published. \nError: " + err.message
          )
        )
        .then(res => (window.location.href = "/myListings"));
    } else {
      api
        .apiV1ListingsSeekingListingIdPut({
          listingId,
          seekingFormBase: {
            ...baseForm,
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
      <div>
        Seeking Form
        <form onSubmit={handleSubmit}>
          <label htmlFor="title">Title: </label>
          <input
            id="title"
            type="text"
            placeholder="Title REQUIRED"
            value={title}
            onChange={e => setTitle(e.target.value)}
            required
          />
          <br />
          <label htmlFor="description">Description: </label>

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
          <label htmlFor="location">Location: </label>
          <input
            type="text"
            id="location"
            placeholder="Location REQUIRED"
            value={location}
            onChange={e => setLocation(e.target.value)}
            required
          />

          <br />
          <label htmlFor="photos">Photos:{""}</label>
          <input
            type="file"
            id="photos"
            onChange={handleFileInput}
            accept="image/*"
            multiple
          />
          <br />
          <button type="button" onClick={preview} disabled={!checkInputs()}>
            Preview
          </button>
          <br />
          <button>Add</button>
        </form>
      </div>
    </div>
  );
};

export default SeekingForm;
