import { FC } from "react";

import { UserListingsInnerListing as UserListingModel } from "@/generated/models/UserListingsInnerListing";
import style from "./MyListingCard.module.scss"

interface UserListingProps {
    listing: UserListingModel;
}

const MyListingCard: FC<UserListingProps> = ({listing}) => {
    return (
        <div className={style.wrapper}>
            <img src={listing.thumbnailUrl} />
            <p>{listing.title}</p>
            <p>{listing.postCode}</p>
            <p>{`£${listing.price}`}</p>
            
            <button>Edit</button>
            <button>Delete</button>
        </div>
    );
};

export default MyListingCard;
