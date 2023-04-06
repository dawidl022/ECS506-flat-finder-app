import { FC } from "react";
import { useRouter } from "next/router";
import AccommodationDetails from "@/components/Listing/AccommodationDetails";
import { Accommodation, AccommodationAddressCountryEnum } from "@/generated";

const AccommodationPreviewPage: FC = ({}) => {
  const router = useRouter();

  const title = router.query.title as string;
  const description = router.query.description as string;
  const line1 = router.query.line1 as string;
  const line2 = router.query.line2 as string;
  const town = router.query.town as string;
  const postCode = router.query.postCode as string;
  const accommodationType = router.query.accommodationType as string;
  const numberOfRooms = Number(router.query.numberOfRooms);
  const price = Number(router.query.price);

  const accomodation: Accommodation = {
    id: "0",
    title,
    description,
    accommodationType,
    numberOfRooms,
    photoUrls: [],
    source: "preview",
    author: {
      name: "Preview User",
      userProfile: {
        id: "0",
        email: "Dummy Email",
        name: "Preview User",
        contactDetails: {
          phoneNumber: "Dummy Phone Number",
        },
      },
    },
    contactInfo: {
      phoneNumber: "Dummy Phone Number",
      email: "Dummy Email",
    },
    price,
    address: {
      line1,
      line2,
      town,
      postCode,
      country: AccommodationAddressCountryEnum.Uk,
    },
  };
  return (
    <div>
      <AccommodationDetails accommodation={accomodation} />
    </div>
  );
};

export default AccommodationPreviewPage;
