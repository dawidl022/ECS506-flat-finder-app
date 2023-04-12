import { FC } from "react";
import { Seeking } from "@/generated/models/Seeking";
import ContactDetails from "@/components/Listing/ContactDetails";
import ProfileCard from "../ProfileCard";
import styles from './AccommodationListing.module.scss';
import UserProfile from "@/pages/profile/[userId]";
interface SeekingDetailsProps {
  seeking: Seeking;
}

const SeekingDetails: FC<SeekingDetailsProps> = ({ seeking }) => {
  const user : UserProfile = {
    id: seeking.author.userProfile?.id ?? "N/A",
    name: seeking.author.name ?? "N/A",
    email: seeking.contactInfo.email ?? "N/A",
    contactDetails: {
      phoneNumber: seeking.contactInfo.phoneNumber ?? "N/A",
    }
  }
  return (
    <div className={styles.wrapper}>
      <div className={styles.information}>
        <h1>{seeking.title}</h1>
        <p>{seeking.description}</p>
      </div>

      <div className={styles.author}>      
        {seeking.author.userProfile?.id ? (
        <ProfileCard userData={seeking.author.userProfile}/>
      ) : null} 
      </div>

    </div>
  );
};

export default SeekingDetails;
