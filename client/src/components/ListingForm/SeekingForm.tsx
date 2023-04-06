import { FC, useState, FormEvent } from "react";
import { useRouter } from "next/router";
import { Configuration, DefaultApi } from "@/generated";

const SeekingForm: FC = ({}) => {
  const router = useRouter();

  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [location, setLocation] = useState("");
  const [lat, setLatitude] = useState(0);
  const [_long, setLongitude] = useState(0);

  const preview = () => {
    router.push({
      pathname: "/SeekingPreviewPage",
      query: {
        title,
        description,
        location,
        lat,
        _long,
      },
    });
  };

  const checkInputs = () => {
    if (title && description && location && lat && _long) {
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
        preferredLocation: {
          name: location,
          coordinates: {
            lat,
            _long,
          },
        },
      })
      .then(res => (window.location.href = "/myListings"));
  };
  return (
    <div>
      <div>
        Seeking Form
        <form>
          <label htmlFor="title">Seeking Title: </label>
          <input
            type="text"
            placeholder="Seeking Title"
            value={title}
            onChange={e => setTitle(e.target.value)}
            required
          />
          <br />
          <label htmlFor="description">Seeking Description: </label>
          <input
            type="text"
            placeholder="Seeking Description"
            value={description}
            onChange={e => setDescription(e.target.value)}
            required
          />
          <br />
          <label htmlFor="location">Seeking Location: </label>
          <input
            type="text"
            placeholder="Seeking Location"
            value={location}
            onChange={e => setLocation(e.target.value)}
            required
          />
          <br />
          <label htmlFor="lat">Seeking Latitude: </label>
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
          <label htmlFor="_long">Seeking Longitude: </label>
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
          <input multiple type="file" id="photos" />
          <br />
          <button type="button" onClick={preview} disabled={!checkInputs()}>
            Preview
          </button>
          <br />
          <button onSubmit={handleSubmit}>Add</button>
        </form>
      </div>
    </div>
  );
};

export default SeekingForm;
