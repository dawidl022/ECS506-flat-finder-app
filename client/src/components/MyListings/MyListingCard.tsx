import { FC } from "react";
import { useRouter } from "next/router";
import {
  UserListingsInnerTypeEnum,
  UserListingsInner,
} from "@/generated/models/UserListingsInner";
import { DefaultApi } from "@/generated/apis/DefaultApi";
import style from "./MyListingCard.module.scss";
import useApi from "@/hooks/useApi";

interface UserListingProps {
  listingInner: UserListingsInner;
}

const MyListingCard: FC<UserListingProps> = ({ listingInner }) => {
  const router = useRouter();
  const listing = listingInner.listing;
  const { apiManager } = useApi();

  const redirect = (success: boolean) => {
    router.replace({
      pathname: router.pathname,
      query: {
        ...router.query,
        success: success,
      },
    });
  };

  const handleDelete = () => {
    const confirmed = window.confirm(
      "Are you sure you want to delete this listing?"
    );

    confirmed &&
      apiManager
        .apiV1ListingsAccommodationListingIdDelete({
          listingId: listing.id,
        })
        .then(() => redirect(true))
        .catch(() => redirect(false));
  };

  const handleEdit = () => {
    router.push({
      pathname: "/edit-listing",
      query: {
        id: listing.id,
        type: listingInner.type,
      },
    });
  };

  return (
    <div className={style.wrapper}>
      <img src={`http://127.0.0.1:5000${listing.thumbnailUrl}`} />
      <p>{listing.id}</p>
      <p>{listing.title}</p>
      <p>{listing.postCode}</p>
      <p>{`£${listing.price}`}</p>

      <button onClick={handleEdit}>Edit</button>
      <button onClick={handleDelete}>Delete</button>
    </div>
  );
};

export default MyListingCard;

// internal_aa8fc213-2b87-4df4-95e6-7efc1fb401f1
//          aa8fc213-2b87-4df4-95e6-7efc1fb401f1
