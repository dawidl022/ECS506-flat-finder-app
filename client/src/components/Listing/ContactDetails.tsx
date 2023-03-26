import { FC } from "react";

interface ContactDetailsProps {
  phoneNumber: string | null;
  emailAddress: string | null;
}

const ContactDetails: FC<ContactDetailsProps> = ({
  phoneNumber,
  emailAddress,
}) => {
  return (
    <div>
      {phoneNumber && (
        <p>
          Phone number: <a href={`tel:${phoneNumber}`}>{phoneNumber}</a>
        </p>
      )}
      {emailAddress && (
        <p>
          Email address: <a href={`mailto:${emailAddress}`}>{emailAddress}</a>
        </p>
      )}
    </div>
  );
};

export default ContactDetails;
