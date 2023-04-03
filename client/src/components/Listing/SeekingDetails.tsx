import { FC, useState, useEffect } from "react";
import { DefaultApi } from "@/generated/apis/DefaultApi";
import { SeekingDetails as SeekingDetailsModel } from "@/generated/models/SeekingDetails";
import ContactDetails from "@/components/Listing/ContactDetails";

interface SeekingDetailsProps {
  listingId: string;
}

const SeekingDetails: FC<SeekingDetailsProps> = ({ listingId }) => {
  const [data, setData] = useState<SeekingDetailsModel | null>(null);
  const [error, setError] = useState(false);
  const { title, description, contactInfo } = data?.accommodation ?? {};

  useEffect(() => {
    new DefaultApi()
      .apiV1ListingsSeekingListingIdGet({
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

export default SeekingDetails;
