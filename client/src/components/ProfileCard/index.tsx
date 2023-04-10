import { UserProfile } from "@/generated";
import React, { FC, useState } from "react";

import styles from "./ProfileCard.module.scss";
import AvatarPlaceholder from "../AvatarPlaceholder";
import EditingButton from "./EditingButtonComponent";
import CardData from "./CardData";
import useApi from "@/hooks/useApi";

interface ProfileCardProps {
  userData: UserProfile;
  isMe?: boolean;
}

const ProfileCard: FC<ProfileCardProps> = ({ userData, isMe = false }) => {
  const [user, setUser] = useState<UserProfile>(userData);
  const [isEditing, setIsEditing] = useState(false);

  const { apiManager } = useApi();

  const getUserProfile = () => {
    apiManager
      .apiV1UsersUserIdProfileGet({ userId: user.id })
      .then(res => setUser(res));
  };

  return (
    <div className={styles.wrapper}>
      <div className={styles.card}>
        <p style={{ position: "absolute", left: 12 }}>
          DEBUG: <br /> is my profile: {isMe ? "True" : "False"} <br />
          is editing: {isEditing ? "True" : "False"}
        </p>
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
      <section className={styles.listingsCon}>
        <h2 className={styles.title}>Listings:</h2>
        <div className={styles.listings}>
          {/* TODO: */}
          {/* Listings card from figma */}
        </div>
      </section>
    </div>
  );
};

export default ProfileCard;
