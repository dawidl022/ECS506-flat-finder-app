import {FC} from 'react';

interface EditListingProps {
    listingType: "seeking" | "accommodation";
    listingId: string;
}

const EditListing: FC<EditListingProps> = (listingType, listingId) => {
    return (
        <div>
        </div>
    )
}
export default EditListing;