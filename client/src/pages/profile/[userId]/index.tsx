import ProfileCard from "@/components/ProfileCard";
import { GetServerSideProps, GetServerSidePropsContext, NextPage } from "next";
import { useRouter } from "next/router";
import { useState, useEffect } from "react";
import { User } from "@/generated";

interface UserProfileProps {
  userData: User;
}

const UserProfile: NextPage<UserProfileProps> = ({ userData }) => {
  const router = useRouter();
  const [success, setSuccess] = useState<boolean | undefined>(false);
  const [error, setError] = useState<boolean | undefined>(false);

  useEffect(() => {
    const query = router.query.success;
    if (query === "true") { setSuccess(true) };
    if (query === "false") { setError(true) };
  }, [router.query]);
  
  return (
    <div className="container">
      {success && <p>Successfully deleted listing</p>}
      {error && <p>Error: could not delete listing</p>}
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
