import FetchedAccommodationDetails from "@/components/Listing/FetchedAccommodationDetails";
import { useRouter } from "next/router";
import React from "react";

const Listing = () => {
  const router = useRouter();
  const id = router.query.listingId as string;
  console.log(id);
  if (!id) return <h1>Loading</h1>;
  return (
    <div>
      <FetchedAccommodationDetails listingId={id} />
    </div>
  );
};

export default Listing;
