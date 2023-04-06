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
            type="text"
            placeholder="Seeking Title"
            value={title}
            onChange={e => setTitle(e.target.value)}
            required
          />
          <br />
          <label htmlFor="description">Description: </label>
          <input
            type="text"
            placeholder="Seeking Description"
            value={description}
            onChange={e => setDescription(e.target.value)}
            required
          />
          <br />
          <label htmlFor="location">Location: </label>
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
          <button>Preview</button>
          <br />
          <button>Add</button>
        </form>
      </div>
    </div>
  );
};

export default SeekingForm;
