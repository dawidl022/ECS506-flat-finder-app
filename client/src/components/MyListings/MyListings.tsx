import { FC, useState, useEffect } from "react";
import { DefaultApi } from "@/generated/apis/DefaultApi";
import { UserListingsInner as UserListingModel, UserListingsInner, UserListingsInnerTypeEnum } from "@/generated/models/UserListingsInner";
import MyListingItem from "./MyListingItem";
  
interface ListingByType {
    [key: string]: UserListingModel[];
  }

const MyListings: FC = () => {
    const [data, setData] = useState<UserListingModel[] | null>(null);
    const [error, setError] = useState(false);

    useEffect(() => {
        new DefaultApi().apiV1UsersUserIdListingsGet({
            userId: "123"
        })
        .then(res => setData(res))
        .catch(() => setError(true)); 
    }, [])

    /*
        Divides the incoming data into two arrays for 'seeking' and 
        'accommodation' type listings
    */
    const listingByType: ListingByType | null = data && data.reduce((acc, item) => {
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
                        <h3>{type.charAt(0).toUpperCase() + type.slice(1)}</h3>
                        {listings.length > 0 ? listings.map((listingInner) => (
                                <MyListingItem 
                                    key={listingInner.listing.id}
                                    listing={listingInner.listing}
                                />
                            ))
                        : (
                            <p>No results found</p>
                        )}
                    </div>
                ))}
                </>
            )}
        </div>
    );
};

export default MyListings;



