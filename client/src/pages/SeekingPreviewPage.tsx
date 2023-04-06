import { FC } from "react";
import { useRouter } from "next/router";

const SeekingPreviewPage: FC = ({}) => {
  const router = useRouter();
  const title = router.query.title;
  const description = router.query.description;
  const location = router.query.location;
  const lat = router.query.lat;
  const _long = router.query._long;

  return (
    <div>
      <h1>Preview of Seeking Listing</h1>
      <p>Title: {title}</p>
      <p>Description: {description}</p>
      <p>Location: {location}</p>
      <p>Latitude: {lat}</p>
      <p>Longitude: {_long}</p>
    </div>
  );
};

export default SeekingPreviewPage;
