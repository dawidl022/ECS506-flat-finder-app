import { FC } from "react";
import SeekingForm from "./SeekingForm";
import AccommodationForm from "./AccommodationForm";
interface EditListingProps {
  listingType: boolean;
  listingId: string;
}

const EditListing: FC<EditListingProps> = (listingType, listingId) => {
  return (
    <div>
      {listingType && <SeekingForm listingId={listingId} />}
      {!listingType && <AccommodationForm listingId={listingId} />}
    </div>
  );
};
export default EditListing;
