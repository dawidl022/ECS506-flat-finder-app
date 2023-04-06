import { FC } from "react";
import { useRouter } from "next/router";
import SeekingDetails from "@/components/Listing/SeekingDetails";
import { Seeking } from "@/generated";
const SeekingPreviewPage: FC = ({}) => {
  const router = useRouter();
  const title = router.query.title as string;
  const description = router.query.description as string;
  const name = router.query.location as string;
  const lat = Number(router.query.lat);
  const _long = Number(router.query._long);

  const Seeking: Seeking =  { 
    id: "0",
    author: {
      name: "Preview User",
      userProfile: {
        id: "0",
        email : "Dummy Email",
        name: "Preview User",
        contactDetails: {
          phoneNumber: "Dummy Phone Number",
        }
      }
    },
    contactInfo: {
      phoneNumber: "Dummy Phone Number",
      email: "Dummy Email",
    }, 
    title, 
    description, 
    preferredLocation: {
      name,
      coordinates: {
        lat,
        _long,
      },
    },
  
  };
  return (
    <div> 
      <SeekingDetails seeking={Seeking} />
    </div>
  );
};

export default SeekingPreviewPage;
