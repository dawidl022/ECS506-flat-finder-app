import ProfileCard from "@/components/ProfileCard";
import { GetServerSideProps, GetServerSidePropsContext, NextPage } from "next";

import React from "react";
import { User } from "@/generated";

interface UserProfileProps {
  userData: User;
}

const UserProfile: NextPage<UserProfileProps> = ({ userData }) => {
  console.log(userData);
  return (
    <div className="container">
      <ProfileCard userData={userData} />
    </div>
  );
};

export default UserProfile;

export const getServerSideProps: GetServerSideProps = async (
  context: GetServerSidePropsContext
) => {
  const { userId }: any = context.params;
  return {
    props: {
      userData: {
        id: userId,
        name: userId,
        email: "somegmail@gmail.com",
        phone: "+2924242",
        somethingelse: "smth",
      },
    },
  };
};
