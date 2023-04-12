import { UserProfile, UserProfileForm } from "@/generated";
import React from "react";

import styles from "./CardData.module.scss";
import useApi from "@/hooks/useApi";

interface CardDataProps {
  userData: UserProfile;
  isEditing: boolean;
  setIsEditing: (v: boolean) => void;
  updateUser: () => void;
}

const CardData: React.FC<CardDataProps> = ({
  userData,
  isEditing,
  setIsEditing,
  updateUser,
}) => {
  const { apiManager } = useApi();
  const [newUserData, setNewUserData] = React.useState({
    name: userData.name,
    email: userData.email,
    contactDetails: userData.contactDetails,
  });

  const onCancelClickHandle = () => {
    setIsEditing(false);
  };

  const onSaveClickHandle = () => {
    console.log(newUserData);
    apiManager
      .apiV1UsersUserIdProfilePut({
        userId: userData.id as string,
        userProfileForm: newUserData as UserProfileForm,
      })
      .then(res => {
        // TODO: popup or some msg of success
        // TODO: for now, just turn of editing mode
        setIsEditing(false);
        updateUser();
      });
  };

  return (
    <>
      {isEditing ? (
        <input
          placeholder={userData.name}
          value={newUserData.name}
          onChange={e => {
            setNewUserData(prev => {
              return {
                ...prev,
                name: e.target.value,
              };
            });
          }}
          className={styles.nameInput}
        />
      ) : (
        <h1 className={styles.name}>{userData.name}</h1>
      )}

      <div className={styles.detailsCon}>
        <div className={styles.detailsRow}>
          <p className={styles.title}>Email:</p>

          {userData.email ? (
            <a href={`mailto:${userData.email}`}>
              <p className={styles.value}>{userData.email}</p>
            </a>
          ) : (
            <p className={styles.value}>N/A</p>
          )}

          {/* TODO: user can not change his mail, right? */}
          {/* {isEditing ? (
            <input className={styles.valueInput} placeholder={userData.email} />
          ) : (
            <p className={styles.value}>{userData.email}</p>
          )} */}
        </div>
        <div className={styles.detailsRow}>
          <label htmlFor="phone" className={styles.title}>
            Phone:
          </label>
          {isEditing ? (
            <input
              id="phone"
              className={styles.valueInput}
              placeholder={userData.contactDetails.phoneNumber}
              value={newUserData.contactDetails.phoneNumber}
              onChange={e => {
                setNewUserData(prev => {
                  return {
                    ...prev,
                    contactDetails: {
                      ...prev.contactDetails,
                      phoneNumber: e.target.value,
                    },
                  };
                });
              }}
            />
          ) : (
            <a href={`tel:${userData.contactDetails.phoneNumber}`}>
              <p className={styles.value}>
                {userData.contactDetails.phoneNumber}
              </p>
            </a>
          )}
        </div>
      </div>
      {isEditing && (
        <div className={styles.btnRow}>
          <button
            className={styles.saveBtn}
            onClick={() => onSaveClickHandle()}
          >
            Save
          </button>
          <button
            className={styles.cancelBtn}
            onClick={() => onCancelClickHandle()}
          >
            Cancel
          </button>
        </div>
      )}
    </>
  );
};

export default CardData;
