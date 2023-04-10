import { FC, useState, FormEvent, ChangeEvent } from "react";
import { useRouter } from "next/router";
import { Configuration, DefaultApi } from "@/generated";
import { handleFileInput } from "./handleFileInput";
import useApi from "@/hooks/useApi";

interface FormProps {
  listingId: string;
  editExistingListing: Boolean;
}

const SeekingForm: FC<FormProps> = ({ listingId, editExistingListing }) => {
  const router = useRouter();
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [location, setLocation] = useState("");
  const { apiManager: api } = useApi();

  if (editExistingListing) {
    api
      .apiV1ListingsSeekingListingIdGet({ listingId })
      .then(res => {
        setTitle(res.seeking.title);
        setDescription(res.seeking.description);
        setLocation(res.seeking.preferredLocation);
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
    const baseForm = {
      title,
      description,
      preferredLocation: location,
    };

    if (!editExistingListing) {
      api
        .apiV1ListingsSeekingPost({
          ...baseForm,
          photos: Array<Blob>(),
        })
        .then(() => router.push({ pathname: "/myListings" }))
        .catch(err =>
          alert(
            "Seeking listing failed to be published. \nError: " + err.message
          )
        );
    } else {
      api
        .apiV1ListingsSeekingListingIdPut({
          listingId,
          seekingFormBase: {
            ...baseForm,
          },
        })
        .then(() => router.push({ pathname: "/myListings" }))
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
          {!editExistingListing && (
            <div>
              <label htmlFor="photos">Photos:{""}</label>
              <input
                type="file"
                id="photos"
                onChange={handleFileInput}
                accept="image/*"
                multiple
              />
            </div>
          )}
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
