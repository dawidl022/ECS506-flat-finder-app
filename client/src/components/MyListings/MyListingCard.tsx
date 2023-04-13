"use client";
import Link from "next/link";
import { FC, useState } from "react";
import { useRouter } from "next/router";
import {
  UserListingsInnerTypeEnum,
  UserListingsInner,
} from "@/generated/models/UserListingsInner";
import { DefaultApi } from "@/generated/apis/DefaultApi";
import styles from "./MyListingCard.module.scss";
import useApi from "@/hooks/useApi";
import Popup from "../Popup";

import { toast } from "react-toastify";
interface UserListingProps {
  listingInner: UserListingsInner;
  fetchData: () => void;
  isMe?: boolean;
}

const MyListingCard: FC<UserListingProps> = ({
  listingInner,
  fetchData,
  isMe = false,
}) => {
  const router = useRouter();
  const listing = listingInner.listing;
  const { apiManager } = useApi();

  const notify = () => {
    toast.success("Listing is deleted", {
      position: "top-right",
      autoClose: 5000,
      hideProgressBar: true,
      closeOnClick: true,
      pauseOnHover: true,
      draggable: true,
      progress: undefined,
      theme: "light",
    });
  };

  const notifyUnsuccess = () => {
    toast.error("Something went wrong", {
      position: "top-right",
      autoClose: 5000,
      hideProgressBar: true,
      closeOnClick: true,
      pauseOnHover: true,
      draggable: true,
      progress: undefined,
      theme: "light",
    });
  };

  const handleDelete = () => {
    const confirmed = window.confirm(
      "Are you sure you want to delete this listing?"
    );

    confirmed && listingInner.type !== "seeking"
      ? apiManager
          .apiV1ListingsAccommodationListingIdDelete({
            listingId: listing.id,
          })
          .then(() => {
            notify();
            fetchData();
          })
          .catch(() => notifyUnsuccess())
      : apiManager
          .apiV1ListingsSeekingListingIdDelete({ listingId: listing.id })
          .then(() => {
            notify();
            fetchData();
          })
          .catch(() => notifyUnsuccess());
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
      <Link href={`/listings/${listingInner.type}/${listing.id}`}>
        {listing.thumbnailUrl && listing.thumbnailUrl !== null ? (
          <img src={`http://127.0.0.1:5000${listing.thumbnailUrl}`} />
        ) : (
          <img src="/placeholder.webp" />
        )}
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

          {isMe && (
            <div className={styles.btnCon}>
              <button className={styles.editBtn} onClick={handleEdit}>
                Edit
              </button>
              <button
                className={styles.deleteBtn}
                onClick={() => {
                  handleDelete();
                }}
              >
                Delete
              </button>
            </div>
          )}
        </div>
      </Link>
    </div>
  );
};

export default MyListingCard;

// internal_aa8fc213-2b87-4df4-95e6-7efc1fb401f1
//          aa8fc213-2b87-4df4-95e6-7efc1fb401f1
