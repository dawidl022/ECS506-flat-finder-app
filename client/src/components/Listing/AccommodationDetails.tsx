import { FC } from "react";
import PhotoGallery from "../PhotoGallery";
import { Accommodation } from "@/generated/models/Accommodation";
import ContactDetails from "@/components/Listing/ContactDetails";
import sanitizeHtml from 'sanitize-html';

interface AccommodationDetailsProps {
  accommodation: Accommodation;
}

const AccommodationDetails: FC<AccommodationDetailsProps> = ({
  accommodation,
}) => {

  const setPhotoUrls = () => {
    if (accommodation.source === 'internal') {
      return accommodation.photoUrls.map(photo => `http://127.0.0.1:5000/${photo}`);
    } else {
      return accommodation.photoUrls;
    }
  
  }

  return (
    <>
      <div>
        {/* 
            Tags not included as this can be implemented alongside styling - eg. 
            price may not have a tag 'price', it may just display the value
            with a different font weight
        */}
        <PhotoGallery photoUrls={setPhotoUrls()}/>        
        <h1>{accommodation.title}</h1>
        <p dangerouslySetInnerHTML={{__html: sanitizeHtml(accommodation.description)}}/>
        {<p>{accommodation.accommodationType}</p>}
        {<p>{accommodation.numberOfRooms}</p>}
        <p>{accommodation.source}</p>
        {<p>{`£${accommodation.price}`}</p>}
        {<a href={accommodation.originalListingUrl}>Original Listing</a>}
      </div>
      <div>
        <h3>Address</h3>
        <p>{accommodation.address.line1}</p>
        <p>{accommodation.address.line2}</p>
        <p>{accommodation.address.town}</p>
        <p>{accommodation.address.postCode}</p>
      </div>
      <div>
        <h3>Contact Details</h3>
        <ContactDetails
          phoneNumber={accommodation.contactInfo?.phoneNumber ?? null}
          emailAddress={accommodation.contactInfo?.email ?? null}
        />
      </div>
      <div>{/* TODO: Author details */}</div>
    </>
  );
};

export default AccommodationDetails;
