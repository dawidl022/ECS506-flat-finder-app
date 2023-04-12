import { FC } from "react";
import { useRouter } from "next/router";
import {
  UserListingsInnerTypeEnum,
  UserListingsInner,
} from "@/generated/models/UserListingsInner";
import { DefaultApi } from "@/generated/apis/DefaultApi";
import styles from "./MyListingCard.module.scss";
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
    <div className={styles.wrapper}>
      <img src={`http://127.0.0.1:5000${listing.thumbnailUrl}`} />
      <div className={styles.content}>
        <div className={styles.header}>
          <p className={styles.title}>{listing.title}</p>
          {listingInner.type !== "seeking" && (
            <p className={styles.price}>{`£${listing.price}`}</p>
          )}
        </div>
        {listingInner.type !== "seeking" && (
          <p className={styles.value}>
            <span>postcode: </span>
            {listing.postCode}
          </p>
        )}

        <p className={styles.value}>
          <span>description: </span> {listing.shortDescription}
        </p>

        <div className={styles.btnCon}>
          <button className={styles.editBtn} onClick={handleEdit}>
            Edit
          </button>
          <button className={styles.deleteBtn} onClick={handleDelete}>
            Delete
          </button>
        </div>
      </div>
    </div>
  );
};

export default MyListingCard;

// internal_aa8fc213-2b87-4df4-95e6-7efc1fb401f1
//          aa8fc213-2b87-4df4-95e6-7efc1fb401f1
