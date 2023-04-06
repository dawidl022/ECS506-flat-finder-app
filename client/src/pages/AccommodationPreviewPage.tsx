import { FC } from "react";
import { useRouter } from "next/router";

const AccommodationPreviewPage: FC = ({}) => {
  const router = useRouter();

  const title = router.query.title;
  const description = router.query.description;
  const line1 = router.query.line1;
  const line2 = router.query.line2;
  const town = router.query.town;
  const postCode = router.query.postCode;
  const country = router.query.country;
  const accommodationType = router.query.accommodationType;
  const numberOfRooms = router.query.numberOfRooms;
  const price = router.query.price;

  return (
    <div>
      <h1>Preview of Accommodation Listing</h1>
      <p>Title: {title}</p>
      <p>Description: {description}</p>
      <p>Line 1: {line1}</p>
      {line2 && <p>Line 2: {line2}</p>}
      <p>Town: {town}</p>
      <p>Post Code: {postCode}</p>
      <p>Country: {country}</p>
      <p>Accommodation Type: {accommodationType}</p>
      <p>Number of Rooms: {numberOfRooms}</p>
      <p>Price: {price}</p>
    </div>
  );
};

export default AccommodationPreviewPage;
