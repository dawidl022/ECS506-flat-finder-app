import { FC } from "react";
import { Seeking } from "@/generated/models/Seeking";
import ContactDetails from "@/components/Listing/ContactDetails";

interface SeekingDetailsProps {
  seeking: Seeking;
}

const SeekingDetails: FC<SeekingDetailsProps> = ({ seeking }) => {
  return (
    <>
      <div>
        <h1>{seeking.title}</h1>
        <p>{seeking.description}</p>
      </div>

      <div>
        <h3>Contact Details</h3>
        <ContactDetails
          phoneNumber={seeking.contactInfo?.phoneNumber ?? null}
          emailAddress={seeking.contactInfo?.email ?? null}
        />
      </div>

      <div>{/* TODO: Author details */}</div>
    </>
  );
};

export default SeekingDetails;
