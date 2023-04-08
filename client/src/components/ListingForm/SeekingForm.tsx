import { FC, useState } from "react";

const SeekingForm: FC = ({}) => {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [location, setLocation] = useState("");

  return (
    <div>
      <div>
        Seeking Form
        <form>
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
            placeholder="Import Photos OPTIONAL"
            accept="image/png, image/jpeg"
            multiple
          />
          <br />
          <button>Preview</button>
          <br />
          <button>Add</button>
        </form>
      </div>
    </div>
  );
};

export default SeekingForm;