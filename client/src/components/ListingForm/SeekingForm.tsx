import { FC, useState, FormEvent, ChangeEvent } from "react";
import { useRouter } from "next/router";
import { Configuration, DefaultApi } from "@/generated";
import { handleFileInput } from "./handleFileInput";

interface FormProps {
  listingId: string | "";
  editable: Boolean;
}

const SeekingForm: FC<FormProps> = ({listingId, editable}) => {
  const router = useRouter();

  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [location, setLocation] = useState("");

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
    const api = new DefaultApi(new Configuration({ basePath: "http://127.0.0.1:5000" }))
    e.preventDefault();
    if(editable){
     api
        .apiV1ListingsSeekingPost({
          title,
          description,
          photos: Array<Blob>(),
          preferredLocation: location,
        })
        .catch(err =>
          alert("Seeking listing failed to be published. \nError: " + err.message)
        )
        .then(res => (window.location.href = "/myListings"));
    } else {
      api
      .apiV1ListingsSeekingListingIdPut({
        listingId,
        seekingFormBase: {
          title,
          description,
          preferredLocation: location,
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
