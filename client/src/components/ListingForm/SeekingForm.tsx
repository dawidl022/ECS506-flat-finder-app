import { FC, useState, FormEvent } from "react";
import {
  Configuration,
  DefaultApi,
} from "@/generated";

const SeekingForm: FC = ({}) => {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [location, setLocation] = useState("");
  const [lat, setLatitude] = useState(0);
  const [_long, setLongitude] = useState(0);

  const handleSubmit = (e: FormEvent<HTMLElement>) => {
    e.preventDefault();
    new DefaultApi(new Configuration({ basePath: "http://127.0.0.1:5000" }))
      .apiV1ListingsSeekingPost({
        title,
        description,
        preferredLocation: {
          name: location,
          coordinates: {
            lat,
            _long,
          }
        },
      })
      .then(res => console.log(res));
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
           <input
              type="text"
              placeholder="Seeking Latitude"
              value={lat}
              onChange={e => setLatitude(parseFloat(e.target.value))}
              required
            />
            <br />
            <input
              type="text"
              placeholder="Seeking Longitude"
              value={_long}
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
