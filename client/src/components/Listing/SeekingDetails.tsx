import { FC } from "react";
import { Seeking } from "@/generated/models/Seeking";
import PhotoGallery from "../PhotoGallery";
import ProfileCard from "../ProfileCard";
import styles from "./AccommodationListing.module.scss";
import UserProfile from "@/pages/profile/[userId]";
interface SeekingDetailsProps {
  seeking: Seeking;
}

const SeekingDetails: FC<SeekingDetailsProps> = ({ seeking }) => {
  const setPhotoUrls = () => {
    return (
      seeking.photoUrls?.map(photo => `http://127.0.0.1:5000/${photo}`) ?? []
    );
  };

  return (
    <div className={styles.wrapper}>
      <PhotoGallery photoUrls={setPhotoUrls()} />
      <div className={styles.information}>
        <h1>{seeking.title}</h1>
        <p>{seeking.description}</p>
      </div>

      <div>
        {seeking.author.userProfile?.id ? (
          <ProfileCard userData={seeking.author.userProfile} />
        ) : null}
      </div>
    </div>
  );
};

export default SeekingDetails;
