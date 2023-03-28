import { FC, useState, useEffect } from "react";
import { DefaultApi } from "@/generated/apis/DefaultApi";
import { AccommodationDetails as AccommodationDetailsModel } from "@/generated/models/AccommodationDetails";
import ContactDetails from "@/components/Listing/ContactDetails";

interface AccommodationDetailsProps {
  listingId: string;
}

const AccommodationDetails: FC<AccommodationDetailsProps> = ({ listingId }) => {
  const [data, setData] = useState<AccommodationDetailsModel | null>(null);
  const [error, setError] = useState(false);
  const {
    title,
    description,
    accommodationType,
    numberOfRooms,
    source,
    price,
    address,
    originalListingUrl,
    contactInfo,
  } = data?.accommodation ?? {};

  useEffect(() => {
    new DefaultApi()
      .apiV1ListingsAccommodationListingIdGet({
        listingId: listingId,
      })
      .then(res => setData(res))
      .catch(() => setError(true));
  }, [listingId]);

  return (
    <div>
      {error ? (
        <p>Error fetching data</p>
      ) : !data ? (
        <p>Loading</p>
      ) : (
        <>
          <div>
            {/* TODO: Photo gallery component */}

            {/* 
                Tags not included as this can be implemented alongside styling - eg. 
                price may not have a tag 'price', it may just display the value
                with a different font weight
            */}
            <h1>{title}</h1>
            {description && <p>{description}</p>}
            {accommodationType && <p>{accommodationType}</p>}
            {numberOfRooms && <p>{numberOfRooms}</p>}
            {source && <p>{source}</p>}
            {price && <p>{`£${price}`}</p>}
            {originalListingUrl && (
              <a href={originalListingUrl}>Original Listing</a>
            )}
          </div>
          <div>
            <h3>Address</h3>
            {address && <p>{address.line1}</p>}
            {address && <p>{address.line2}</p>}
            {address && <p>{address.town}</p>}
            {address && <p>{address.postCode}</p>}
          </div>
          <div>
            <h3>Contact Details</h3>
            <ContactDetails
              phoneNumber={contactInfo?.phoneNumber ?? null}
              emailAddress={contactInfo?.email ?? null}
            />
          </div>
          <div>{/* TODO: Author details */}</div>
        </>
      )}
    </div>
  );
};

export default AccommodationDetails;
