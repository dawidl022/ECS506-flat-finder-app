import { FC } from "react";
import Link from "next/link";
import { AccommodationSummary } from "@/generated/models/AccommodationSummary";

import styles from "./Tile.module.scss";

interface AccommodationSummaryProps {
  accommodation: AccommodationSummary;
}

const AccommodationSummaryTile: FC<AccommodationSummaryProps> = ({
  accommodation,
}) => {
  return (
    <div className={styles.wrapper}>
      <Link href={`/listings/accommodation/${accommodation.id}`}>
        <img
          src={accommodation.thumbnailUrl}
          alt={`listing ${accommodation.id}`}
        />
        <div className={styles.body}>
          <div className={styles.header}>
            <p className={styles.title}>{accommodation.title}</p>
            <p className={styles.price}>{`£${accommodation.price}`}</p>
          </div>
          {/* <p> {accommodation.shortDescription} </p> */}
          <div className={styles.moreDetails}>
            <p>
              <span>Accommodation type:</span> {accommodation.accommodationType}{" "}
            </p>
            <p>
              <span>rooms number:</span> {accommodation.numberOfRooms}{" "}
            </p>
            <p>
              <span>postcode:</span> {accommodation.postCode}{" "}
            </p>
            <p>
              <span>source:</span> {accommodation.source}{" "}
            </p>
          </div>
        </div>
      </Link>
    </div>
  );
};

export default AccommodationSummaryTile;
