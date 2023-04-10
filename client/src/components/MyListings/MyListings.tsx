import { FC, useState, useEffect } from "react";
import { DefaultApi } from "@/generated/apis/DefaultApi";
import { UserListingsInner as UserListingModel, UserListingsInner, UserListingsInnerTypeEnum } from "@/generated/models/UserListingsInner";
import MyListingCard from "./MyListingCard";
  
interface ListingByType {
    [key: string]: UserListingModel[];
  }

const testData: UserListingsInner[] = [
    {
      type: UserListingsInnerTypeEnum.Accommodation,
      listing: {
        id: "1",
        title: "Luxury apartment in the city center",
        shortDescription: "Stylish and comfortable apartment in the heart of the city",
        thumbnailUrl: "https://example.com/thumbnail.jpg",
        accommodationType: "Apartment",
        numberOfRooms: 2,
        source: "Airbnb",
        price: 150,
        postCode: "12345"
      }
    },
  ];

const MyListings: FC = () => {
    const [data, setData] = useState<UserListingModel[] | null>(testData);
    const [error, setError] = useState(false);

    // useEffect(() => {
    //     new DefaultApi().apiV1UsersUserIdListingsGet({
    //         userId: "123"
    //     })
    //     .then(res => setData(res))
    //     .catch(() => setError(true)); 
    // }, [])

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
                        <h3>{type.charAt(0).toUpperCase() + type.slice(1) + " listings"}</h3>
                        {listings.length > 0 && listings.map((listingInner) => (
                            <MyListingCard 
                                key={listingInner.listing.id}
                                listingInner={listingInner}
                            />
                        ))}
                    </div>
                ))}
                </>
            )}
        </div>
    );
};

export default MyListings;



