import React from "react";

import styles from "./FinishAuth.module.scss";
import Input from "@/components/Input";
import useUser from "@/hooks/useUser";
import useApi from "@/hooks/useApi";
import { useRouter } from "next/router";

interface UserInput {
  firstName: string;
  lastName: string;
  phone: string;
}

const FinishAuth = () => {
  const router = useRouter();
  const [userProfile, setUserProfile] = React.useState<UserInput>({
    firstName: "",
    lastName: "",
    phone: "",
  });

  const { user, refetchUser } = useUser();

  const { apiManager } = useApi();

  const handleFinishRegistration = () => {
    // TODO: handle error
    if (!userProfile.firstName || !userProfile.lastName || !userProfile.phone)
      return;
    console.log(userProfile.firstName + " " + userProfile.lastName);

    apiManager
      .apiV1UsersUserIdProfilePut({
        userId: user?.id as string,
        userProfileForm: {
          name:
            userProfile.firstName.trim() + " " + userProfile.lastName.trim(),
          contactDetails: {
            phoneNumber: userProfile.phone.trim(),
          },
        },
      })
      .then(res => {
        refetchUser();
        router.push("/");
      })
      .catch(err => console.log(err));
  };

  return (
    <div className="container">
      <div className={styles.wrapper}>
        <div className={styles.card}>
          <h2>Complete your profile</h2>
          <div className={styles.row}>
            <Input
              label="First name"
              placeholder="Enter your first name"
              isRequired
              value={userProfile.firstName}
              setValue={(val: string) =>
                setUserProfile(prev => {
                  return { ...prev, firstName: val };
                })
              }
            />

            <Input
              label="Last name"
              placeholder="Enter your last name"
              isRequired
              value={userProfile.lastName}
              setValue={(val: string) =>
                setUserProfile(prev => {
                  return { ...prev, lastName: val };
                })
              }
            />
          </div>

          <Input
            label="Phone"
            placeholder="Enter your phone"
            isRequired
            value={userProfile.phone}
            setValue={(val: string) =>
              setUserProfile(prev => {
                return { ...prev, phone: val };
              })
            }
          />

          <div className={styles.btnCon}>
            <button
              className={styles.btn}
              onClick={() => handleFinishRegistration()}
            >
              Submit
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default FinishAuth;
