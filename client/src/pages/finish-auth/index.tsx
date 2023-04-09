import React from "react";

import styles from "./FinishAuth.module.scss";
import Input from "@/components/Input";
import useApiConfig from "@/hooks/useApiConfig";
import { Configuration, DefaultApi } from "@/generated";
import useUser from "@/hooks/useUser";

interface UserInput {
  firstName: string;
  lastName: string;
  phone: string;
}

const FinishAuth = () => {
  const [userData, setUser] = React.useState<UserInput>({
    firstName: "",
    lastName: "",
    phone: "",
  });

  const { user } = useUser();

  const { config } = useApiConfig();

  const handleFinishRegistration = () => {
    // TODO: handle error
    if (!userData.firstName || !userData.lastName || !userData.phone) return;
    console.log(userData.firstName + " " + userData.lastName);

    // FIX:
    new DefaultApi(new Configuration(config))
      .apiV1UsersUserIdProfilePut({
        userId: user?.id as string,
        userProfileForm: {
          name: userData.firstName + " " + userData.lastName,
          contactDetails: {},
        },
      })
      .then(res => console.log(res));
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
              value={userData.firstName}
              setValue={(val: string) =>
                setUser(prev => {
                  return { ...prev, firstName: val };
                })
              }
            />

            <Input
              label="Last name"
              placeholder="Enter your last name"
              isRequired
              value={userData.lastName}
              setValue={(val: string) =>
                setUser(prev => {
                  return { ...prev, lastName: val };
                })
              }
            />
          </div>

          <Input
            label="Phone"
            placeholder="Enter your phone"
            isRequired
            value={userData.phone}
            setValue={(val: string) =>
              setUser(prev => {
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
