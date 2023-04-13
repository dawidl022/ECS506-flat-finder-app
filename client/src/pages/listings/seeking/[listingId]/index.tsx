import FetchedSeekingDetails from "@/components/Listing/FetchedSeekingDetails";
import { useRouter } from "next/router";
import React from "react";

const Listing = () => {
  const router = useRouter();
  const id = router.query.listingId as string;
  console.log(id);
  if (!id) return <h1>Loading</h1>;
  return (
    <div>
      <FetchedSeekingDetails listingId={id} />
    </div>
  );
};

export default Listing;
