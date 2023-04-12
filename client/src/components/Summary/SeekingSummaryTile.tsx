import { FC } from "react";
import Link from "next/link";
import { SeekingSummary } from "@/generated/models/SeekingSummary";

import styles from "./Tile.module.scss";

interface seekingSummaryProps {
  seekingAccomodation: SeekingSummary;
}

const SeekingSummaryTile: FC<seekingSummaryProps> = ({
  seekingAccomodation,
}) => {
  return (
    <div className={styles.wrapper}>
      <Link href={`/listings/seeking/${seekingAccomodation.id}`}>
        <div className={styles.imgCon}>
          {/* <PhotoGallery/> */}
          {seekingAccomodation.thumbnailUrl ? (
            <img
              className={styles.accImg}
              src={`http://127.0.0.1:5000${seekingAccomodation.thumbnailUrl}`}
              alt={`listing ${seekingAccomodation.id}`}
            />
          ) : (
            <img className={styles.imgPlc} src={"./plchld.svg"} />
          )}
        </div>
        <div className={styles.body}>
          <h3 className={styles.title}> {seekingAccomodation.title} </h3>
          <div className={styles.moreDetails}>
            <p>
              <span>description:</span> {seekingAccomodation.shortDescription}
            </p>
          </div>
        </div>
      </Link>
    </div>
  );
};

export default SeekingSummaryTile;
