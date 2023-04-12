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

const MyListings: FC = () => {
  const [data, setData] = useState<UserListingModel[] | null>(null);
  const [error, setError] = useState(false);
  const { user } = useUser();
  const { apiManager } = useApi();

  useEffect(() => {
    if (user?.id) {
      apiManager
        .apiV1UsersUserIdListingsGet({
          userId: user?.id as string,
        })
        .then(res => {
          setData(res);
        })
        .catch(err => {
          console.log(err);
          setError(true);
        });
    }
  }, [user]);

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
            <div key={type}>
              <h3>
                {type.charAt(0).toUpperCase() + type.slice(1) + " listings"}
              </h3>
              <div className={styles.listingsWrapper}>
                {listings.length > 0 &&
                  listings.map(listingInner => (
                    <MyListingCard
                      key={listingInner.listing.id}
                      listingInner={listingInner}
                    />
                  ))}
              </div>
            </div>
          ))}
        </>
      )}
    </div>
  );
};

export default MyListings;
