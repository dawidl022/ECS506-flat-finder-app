import { FC } from "react";
import SeekingForm from "../ListingForm/SeekingForm";
import AccommodationForm from "../ListingForm/AccommodationForm";
interface EditListingProps {
  listingType: "seeking" | "accommodation";
  listingId: string;
}

const EditListing: FC<EditListingProps> = (listingType, listingId) => {
  return (
    <div>
      {listingType.toString() === "seeking" && (
        <SeekingForm listingId={listingId} editExistingListing={true} />
      )}
      {listingType.toString() === "accommodation" && (
        <AccommodationForm listingId={listingId} editExistingListing={true} />
      )}
    </div>
  );
};
export default EditListing;
