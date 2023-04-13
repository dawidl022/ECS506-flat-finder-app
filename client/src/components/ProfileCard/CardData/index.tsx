import { UserProfile, UserProfileForm } from "@/generated";
import React from "react";
import Link from "next/link";
import styles from "./CardData.module.scss";
import useApi from "@/hooks/useApi";
import { User } from "@/generated";
import { useRouter } from "next/router";
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
  const router = useRouter();
  const [users, setUsers] = React.useState<User[]>([]);
  const [newUserData, setNewUserData] = React.useState({
    name: userData.name,
    email: userData.email,
    contactDetails: userData.contactDetails,
  });

  React.useEffect(() => {
    apiManager
      .apiV1UsersGet()
      .then((users: User[]) => {
        setUsers(users);
      })
      .catch(err => console.log(err));
  }, []);

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

          {userData.email != "N/A"  && userData.email != "Dummy Email" ? (
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
          ) : userData.contactDetails.phoneNumber != "N/A"  && userData.contactDetails.phoneNumber != "Dummy Phone Number" ? (
            <a href={`tel:${userData.contactDetails.phoneNumber}`}>
              <p className={styles.value}>
                {userData.contactDetails.phoneNumber}
              </p>
            </a>
          ) : (
            <p className={styles.value} onClick={() => console.log("click")}>
              N/A
            </p>
          )}
        </div>
      </div>

      {router.pathname.startsWith("/listings/") && users.map(user => {
        if (user.id === userData.id) {
          return (
            <Link
              className={styles.blue}
              href="/profile/[userId]"
              as={`/profile/${userData.id}`}
            >
              See more listings by this user
            </Link>
          );
        }
      })}
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
