import { User } from "@/generated";
import React, { FC } from "react";

import styles from "./ProfileCard.module.scss";

interface ProfileCardProps {
  userData: User;
}

const ProfileCard: FC<ProfileCardProps> = ({ userData }) => {
  return (
    <div className={styles.wrapper}>
      <div className={styles.card}>
        <div className={styles.avaCon}>
          <div className={styles.ava}></div>
        </div>
        <h3 className={styles.name}>{userData.name}</h3>

        <div className={styles.detailsCon}>
          <div className={styles.detailsRow}>
            <p className={styles.title}>Email:</p>
            <p className={styles.value}>{userData.email}</p>
          </div>
          <div className={styles.detailsRow}>
            <p className={styles.title}>Phone:</p>
            <p className={styles.value}>+38737853</p>
          </div>
          <div className={styles.detailsRow}>
            <p className={styles.title}>More info</p>
            <p className={styles.value}>whateva</p>
          </div>
        </div>
      </div>

      {/* If user has listings */}
      <section className={styles.listingsCon}>
        <h3 className={styles.title}>Listings:</h3>
        <div className={styles.listings}>
          {/* TODO: */}
          {/* Listings card from figma */}
        </div>
      </section>
    </div>
  );
};

export default ProfileCard;
