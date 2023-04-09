import { FC } from "react";
import Tabs from "../Tabs";
import { useRouter } from "next/router";
import SeekingForm from "./SeekingForm";
import AccommodationForm from "./AccommodationForm";

const ListingForm: FC = ({}) => {
  const router = useRouter();
  const { listingType } = router.query;

  return (
    <div>
      {/* "Seeking" and "Accommodation". Based on the outcome, the appropriate form should be rendered. */}
      <Tabs tabs={["Seeking", "Accommodation"]} />

      {listingType === "seeking" && (
        <SeekingForm listingId={""} editExistingListing={false} />
      )}

      {listingType === "accommodation" && (
        <AccommodationForm listingId={""} editExistingListing={false} />
      )}
    </div>
  );
};

export default ListingForm;
