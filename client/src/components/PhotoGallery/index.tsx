import { FC } from "react";
import { Slide } from "react-slideshow-image";
import "react-slideshow-image/dist/styles.css";

import styles from "./PhotoGallery.module.scss";

interface PhotoGalleryProps {
  photoUrls: string[];
  width?: string;
}

const PhotoGallery: FC<PhotoGalleryProps> = ({
  photoUrls,
  width = "350px",
}) => {
  return (
    <div style={{ width: width }}>
      <Slide transitionDuration={200}>
        {photoUrls.map((photoUrls, index) => (
          <div className={styles.wrapper} key={index}>
            <img src={photoUrls} width={"100%"} alt={"Photo: " + index} />
          </div>
        ))}
      </Slide>
    </div>
  );
};

export default PhotoGallery;
