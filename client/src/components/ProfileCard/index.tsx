import { UserProfile } from "@/generated";
import React, { FC, useState } from "react";
import MyListings from "@/components/MyListings/MyListings";
import { useRouter } from "next/router";
import styles from "./ProfileCard.module.scss";
import AvatarPlaceholder from "../AvatarPlaceholder";
import EditingButton from "./EditingButtonComponent";
import CardData from "./CardData";
import useApi from "@/hooks/useApi";
import Link from "next/link";

interface ProfileCardProps {
  userData: UserProfile;
  isMe?: boolean;
  showLink?: boolean;
}

const ProfileCard: FC<ProfileCardProps> = ({
  userData,
  isMe = false,
  showLink = false,
}) => {
  const [user, setUser] = useState<UserProfile>(userData);
  const [isEditing, setIsEditing] = useState(false);
  const router = useRouter();
  const { apiManager } = useApi();

  const getUserProfile = () => {
    apiManager
      .apiV1UsersUserIdProfileGet({ userId: user.id })
      .then(res => setUser(res));
  };

  React.useEffect(() => {
    setUser(userData);
  }, [userData]);

  return (
    <div className={styles.wrapper}>
      <div className={styles.card}>
        {/* <p style={{ position: "absolute", left: 12 }}>
          DEBUG: <br /> is my profile: {isMe ? "True" : "False"} <br />
          is editing: {isEditing ? "True" : "False"}
        </p> */}
        {isMe && !isEditing && <EditingButton setIsEditing={setIsEditing} />}

        <div className={styles.avaCon}>
          <AvatarPlaceholder name={user.name as string} size={94} />
        </div>
        <CardData
          updateUser={getUserProfile}
          userData={user}
          isEditing={isEditing}
          setIsEditing={setIsEditing}
        />
      </div>

      {/* If user has listings */}
      {router.pathname.startsWith("/profile/") && (
        <section className={styles.listingsCon}>
          {/* <h2 className={styles.title}>Listings:</h2> */}
          <div className={styles.listings}>
            <MyListings userId={userData.id} />
          </div>
        </section>
      )}
    </div>
  );
};

export default ProfileCard;
