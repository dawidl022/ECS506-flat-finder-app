import { FC, useState, FormEvent, ChangeEvent } from "react";
import { useRouter } from "next/router";
import { Configuration, DefaultApi } from "@/generated";

const SeekingForm: FC = ({}) => {
  const router = useRouter();

  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [location, setLocation] = useState("");

  function handleFileInput(e: ChangeEvent<HTMLInputElement>) {
    const files = e.target.files;
    //check if there are more than 15 files selected
    if (files && files.length > 0) {
      if (files.length > 15) {
        alert("You can upload up to 15 files");
        e.target.value = '';
        return;
      }

      //check if the file size is greater than 5MB
      for (let i = 0; i < files.length; i++) {
        if (files[i].size > 5242880) {
          alert(`The maximum file size is 5MB`);
          e.target.value = ''; 
          return;
        }
      }
    } 
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
    new DefaultApi(new Configuration({ basePath: "http://127.0.0.1:5000" }))
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
            placeholder="Seeking Title REQUIRED"
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
            placeholder="Seeking Description REQUIRED"
            value={description}
            onChange={e => setDescription(e.target.value)}
            required
          />
          <br />
          <label htmlFor="location">Location: </label>
          <input
            type="text"
            id="location"
            placeholder="Seeking Location REQUIRED"
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
