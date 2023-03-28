import { FC } from "react";
import Link from "next/link";
import { AccommodationSummary } from "@/generated/models/AccommodationSummary";

interface AccommodationSummaryProps {
  accommodation: AccommodationSummary;
}

const AccommodationSummaryTile: FC<AccommodationSummaryProps> = ({
  accommodation,
}) => {
  return (
    <div>
      <Link href={`/listings/accommodation/${accommodation.id}`}>
        <img
          src={accommodation.thumbnailUrl}
          width={150}
          height={150}
          alt={`listing ${accommodation.id}`}
        />
        <p> {accommodation.title} </p>
        <p> {`£${accommodation.price}`} </p>
        <p> {accommodation.shortDescription} </p>
        <p> {accommodation.accommodationType} </p>
        <p> {accommodation.numberOfRooms} </p>
        <p> {accommodation.postCode} </p>
        <p> {accommodation.source} </p>
      </Link>
    </div>
  );
};

export default AccommodationSummaryTile;
