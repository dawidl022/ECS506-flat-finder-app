import { FC, useState } from "react";

const SeekingForm: FC = ({}) => {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [location, setLocation] = useState("");
  const [lat, setLatitude] = useState(0);
  const [_long, setLongitude] = useState(0);

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
          <input
            type="number"
            placeholder="Seeking Latitude"
            value={lat}
            min={-90}
            max={90}
            step="any"
            onChange={e => setLatitude(parseFloat(e.target.value))}
            required
          />
          <br />
          <input
            type="number"
            placeholder="Seeking Longitude"
            value={_long}
            min={-180}
            max={180}
            step="any"
            onChange={e => setLongitude(parseFloat(e.target.value))}
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
