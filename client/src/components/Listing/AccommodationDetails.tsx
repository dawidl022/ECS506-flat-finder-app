import { FC } from "react";
import PhotoGallery from "../PhotoGallery";
import { Accommodation } from "@/generated/models/Accommodation";
import sanitizeHtml from "sanitize-html";
import styles from "./AccommodationListing.module.scss";
import ProfileCard from "../ProfileCard";
import UserProfile from "@/pages/profile/[userId]";
interface AccommodationDetailsProps {
  accommodation: Accommodation;
}

const AccommodationDetails: FC<AccommodationDetailsProps> = ({
  accommodation,
}) => {
  const setPhotoUrls = () => {
    if (accommodation.source === "internal") {
      return accommodation.photoUrls?.map(
        photo => `http://127.0.0.1:5000/${photo}`
      );
    } else {
      return accommodation.photoUrls;
    }
  };

  const user: UserProfile = {
    id: accommodation.author.userProfile?.id ?? "N/A",
    name: accommodation.author.name ?? "N/A",
    email: accommodation.contactInfo.email ?? "N/A",
    contactDetails: {
      phoneNumber: accommodation.contactInfo.phoneNumber ?? "N/A",
    },
  };

  return (
    <div className={styles.wrapper}>
      <PhotoGallery photoUrls={setPhotoUrls()} />
      <div className={styles.header}>
        <h1>{accommodation.title}</h1>
        {<h1>{`£${accommodation.price} PCM`}</h1>}
      </div>

      <div className={styles.information}>
        <h2>Information:</h2>
        {<p>Type: {accommodation.accommodationType}</p>}
        {<p>Number of rooms: {accommodation.numberOfRooms}</p>}
        <p>Source: {accommodation.source}</p>
        {accommodation.originalListingUrl && (
          <a href={accommodation.originalListingUrl}>
            View original listing on Zoopla
          </a>
        )}
        <p
          dangerouslySetInnerHTML={{
            __html: sanitizeHtml(accommodation.description),
          }}
        />
      </div>

      <div className={styles.address}>
        <h2>Address:</h2>
        {accommodation.address.line1 && <p>{accommodation.address.line1}</p>}
        {accommodation.address.line2 && <p>{accommodation.address.line2}</p>}
        <p>{accommodation.address.town}</p>
        <p>{accommodation.address.postCode}</p>
      </div>

      <div>
        <ProfileCard userData={user} />
      </div>
    </div>
  );
};

export default AccommodationDetails;
