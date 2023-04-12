import { FC } from "react";
import Link from "next/link";
import { SeekingSummary } from "@/generated/models/SeekingSummary";

interface seekingSummaryProps {
  seekingAccomodation: SeekingSummary;
}

// const SeekingSummaryTile: FC<seekingSummaryProps> = ({
const SeekingSummaryTile: FC<any> = ({ seekingAccomodation }) => {
  console.log(seekingAccomodation);
  return (
    <div>
      {/* <Link href={`/listings/seeking/${seekingAccomodation.id}`}>
        <h3> {seekingAccomodation.title} </h3>
        <p> {seekingAccomodation.shortDescription} </p>
      </Link> */}
    </div>
  );
};

export default SeekingSummaryTile;
