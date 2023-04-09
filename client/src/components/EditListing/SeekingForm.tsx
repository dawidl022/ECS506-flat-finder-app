import { FC, useState, FormEvent } from "react";
import { Configuration, DefaultApi } from "@/generated";
interface SeekingProps {
  listingId: string;
}
const SeekingForm: FC<SeekingProps> = ({ listingId }) => {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [location, setLocation] = useState("");

  const api = new DefaultApi(
    new Configuration({ basePath: "http://127.0.0.1:5000" })
  );
  api
    .apiV1ListingsSeekingListingIdGet({ listingId })
    .then(res => {
      setTitle(res.seeking.title);
      setDescription(res.seeking.description);
      setLocation(res.seeking.preferredLocation.name);
    })
    .catch(err => {
      alert(`Could not find listing with ID:  ${listingId} \nError:  ${err}`);
    });

  const handleSubmit = (e: FormEvent<HTMLElement>) => {
    e.preventDefault();

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
          <button>Add</button>
        </form>
      </div>
    </div>
  );
};

export default SeekingForm;
