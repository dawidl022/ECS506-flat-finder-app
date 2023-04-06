import { FC, useState } from "react";

const SeekingForm: FC = ({}) => {
  const [title, setTitle] = useState("");
  const [location, setLocation] = useState("");
  const [description, setDescription] = useState("");

  const previewFunc = () => {
    //redirect to preview page and render the AccomodationDetails componen
  };

  return (
    <div>

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

    </div>
  );
};

export default SeekingForm;
