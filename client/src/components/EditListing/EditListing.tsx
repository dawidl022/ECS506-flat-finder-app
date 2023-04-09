import { FC } from "react";
import SeekingForm from "./SeekingForm";
import AccommodationForm from "./AccommodationForm";

interface EditListingProps {
  listingType: "seeking" | "accommodation";
  listingId: string;
}

const EditListing: FC<EditListingProps> = (listingType, listingId) => {
  return (
    <div>
      {listingType.toString() === "seeking" && <SeekingForm listingId={listingId} />}
      {listingType.toString() === "accommodation" && <AccommodationForm listingId={listingId} />}
    </div>
  );
};
export default EditListing;
