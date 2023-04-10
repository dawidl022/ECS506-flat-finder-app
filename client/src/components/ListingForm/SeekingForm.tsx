import { FC, useState, FormEvent, ChangeEvent, useEffect } from "react";
import { useRouter } from "next/router";
import { Configuration, DefaultApi } from "@/generated";
import { handleFileInput } from "./handleFileInput";
import useApi from "@/hooks/useApi";
import useUser from "@/hooks/useUser";

interface FormProps {
  listingId: string;
  editExistingListing: Boolean;
}

// {"author":
// {"name":"Ivan Seagull",
// "userProfile":{"contactDetails":{"phoneNumber":"13131313"},
// "email":"ivan.seagull.k@gmail.com","id":"e7cf519d-9011-45a0-9505-0861aef17444","name":"Ivan Seagull"}},
// "contactInfo":{"email":"ivan.seagull.k@gmail.com","phoneNumber":"13131313"},
// "description":"313131313","id":"internal_457498e6-0647-44da-a412-38de407626a4",
// "photoUrls":[],"preferredLocation":"london","title":"1313131"}

const SeekingForm: FC<FormProps> = ({ listingId, editExistingListing }) => {
  const router = useRouter();
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [location, setLocation] = useState("");
  const { apiManager: api } = useApi();
  const { user } = useUser();

  useEffect(() => {
    if (editExistingListing) {
      api
        .apiV1ListingsSeekingListingIdGet({ listingId })
        .then(res => {
          setTitle(res.title);
          setDescription(res.description);
          setLocation(res.preferredLocation);
        })
        .catch(err => {
          alert(
            `Could not find listing with ID:  ${listingId} \nError:  ${err}`
          );
        });
    }
  }, []);

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
        .then(() => router.push({ pathname: `/profile/${user?.id}` }))
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
        .then(() => router.push({ pathname: `/profile/${user?.id}` }))
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
