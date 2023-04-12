import ProfileCard from "@/components/ProfileCard";
import { GetServerSideProps, GetServerSidePropsContext, NextPage } from "next";
import { useRouter } from "next/router";
import { useState, useEffect } from "react";
import { Configuration, DefaultApi, UserProfile } from "@/generated";
import useApi from "@/hooks/useApi";

import * as cookie from "cookie";
import useUser from "@/hooks/useUser";
import Popup from "@/components/Popup";

interface UserProfileProps {
  userData: UserProfile;
}

const UserProfile: NextPage<UserProfileProps> = ({ userData }) => {
  const { user } = useUser();
  const isMe = user?.id === userData.id;
  const router = useRouter();
  const [success, setSuccess] = useState<boolean | undefined>(false);
  const [error, setError] = useState<boolean | undefined>(false);

  const [isPopup, setIsPopup] = useState(false);

  useEffect(() => {
    const query = router.query.success;
    if (query === "true") {
      setSuccess(true);
    }
    if (query === "false") {
      setError(true);
    }
  }, [router.query]);

  return (
    <div className="container">
      {success && <p>Successfully deleted listing</p>}
      {error && <p>Error: could not delete listing</p>}

      <p style={{ marginTop: 70 }} onClick={() => setIsPopup(true)}>
        TEST
      </p>
      <Popup visible={isPopup} setVisible={setIsPopup}>
        <h1>123</h1>
      </Popup>
      {userData.id ? (
        <ProfileCard isMe={isMe} userData={userData} />
      ) : (
        // TODO: nice message
        <p>No such a user</p>
      )}
    </div>
  );
};

export default UserProfile;

export const getServerSideProps: GetServerSideProps = async (
  context: GetServerSidePropsContext
) => {
  // hooks dont work in getServerSideProps
  const { userId }: any = context.params;

  const token = cookie.parse(context.req.headers.cookie as string).token;
  const basePath = "http://127.0.0.1:5000";
  const config = new Configuration({ basePath, accessToken: token });

  const api = new DefaultApi(config);

  let result;
  try {
    const res = await api.apiV1UsersUserIdProfileGet({ userId });
    result = res;
  } catch (error) {}

  return {
    props: {
      userData: {
        ...result,
      },
    },
  };
};
