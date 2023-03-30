import { FC } from "react";
import { Slide } from "react-slideshow-image";
import "react-slideshow-image/dist/styles.css";

// Default settings for the slider component.
const divSettings = {
  display: "flex",
  alignItems: "center",
  justifyContent: "center",
  backgroundSize: "cover",
};

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
          <div style={divSettings} key={index}>
            <img src={photoUrls} width={"100%"} alt={"Photo: " + index} />
          </div>
        ))}
      </Slide>
    </div>
  );
};

export default PhotoGallery;
