import ProfileCard from "@/components/ProfileCard";
import { GetServerSideProps, GetServerSidePropsContext, NextPage } from "next";

import React from "react";
import { Configuration, DefaultApi, UserProfile } from "@/generated";
import useApi from "@/hooks/useApi";

import * as cookie from "cookie";
import useUser from "@/hooks/useUser";

interface UserProfileProps {
  userData: UserProfile;
}

const UserProfile: NextPage<UserProfileProps> = ({ userData }) => {
  const { user } = useUser();
  const isMe = user?.id === userData.id;
  return (
    <div className="container">
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
