import { FC, useState, useEffect } from "react";
import { DefaultApi } from "@/generated/apis/DefaultApi";
import {
  UserListingsInner as UserListingModel,
  UserListingsInner,
  UserListingsInnerTypeEnum,
} from "@/generated/models/UserListingsInner";
import MyListingCard from "./MyListingCard";
import useUser from "@/hooks/useUser";
import useApi from "@/hooks/useApi";

import styles from "./MyListings.module.scss";

interface ListingByType {
  [key: string]: UserListingModel[];
}

interface MyListingsProps {
  userId: string;
}

const MyListings: FC<MyListingsProps> = ({ userId }) => {
  const [data, setData] = useState<UserListingModel[] | null>(null);
  const [error, setError] = useState(false);
  const { apiManager } = useApi();

  useEffect(() => {
    fetchData();
  }, [userId]);

  const fetchData = () => {
    if (userId) {
      apiManager
        .apiV1UsersUserIdListingsGet({
          userId: userId,
        })
        .then(res => {
          setData(res);
        })
        .catch(err => {
          console.log(err);
          setError(true);
        });
    }
  };

  const listingByType: ListingByType | null =
    data &&
    data.reduce((acc, item) => {
      if (!acc[item.type]) {
        acc[item.type] = [];
      }
      acc[item.type].push(item);
      return acc;
    }, {} as ListingByType);

  return (
    <div>
      {error ? (
        <p>Error fetching data</p>
      ) : !data ? (
        <p>Loading</p>
      ) : (
        <>
          {Object.entries(listingByType || {}).map(([type, listings]) => (
            <section className={styles.section} key={type}>
              <h3 className={styles.sectionTitle}>
                {type.charAt(0).toUpperCase() + type.slice(1) + " listings"}
              </h3>
              <div className={styles.listingsWrapper}>
                {listings.length > 0 &&
                  listings.map(listingInner => (
                    <MyListingCard
                      fetchData={fetchData}
                      key={listingInner.listing.id}
                      listingInner={listingInner}
                    />
                  ))}
              </div>
            </section>
          ))}
        </>
      )}
    </div>
  );
};

export default MyListings;
