import { FC } from "react";

import { UserListingsInnerListing as UserListingModel } from "@/generated/models/UserListingsInnerListing";

interface UserListingProps {
    listing: UserListingModel;
}

const MyListingItem: FC<UserListingProps> = ({listing}) => {
    return (
        <div>
            {listing.id}
        </div>
    );
};

export default MyListingItem;
