import { FC } from "react";
import SeekingForm from "../ListingForm/SeekingForm";
import AccommodationForm from "../ListingForm/AccommodationForm";
import { UserListingsInnerTypeEnum } from "@/generated";

interface EditListingProps {
  listingType: UserListingsInnerTypeEnum;
  listingId: string;
}

const EditListing: FC<EditListingProps> = ({ listingType, listingId }) => {
  return (
    <div>
      {listingType === "seeking" && (
        <SeekingForm listingId={listingId} editExistingListing={true} />
      )}

      {listingType === "accommodation" && (
        <AccommodationForm listingId={listingId} editExistingListing={true} />
      )}
    </div>
  );
};
export default EditListing;
