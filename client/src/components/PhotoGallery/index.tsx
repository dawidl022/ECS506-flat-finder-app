import { FC } from 'react';
import { Slide } from 'react-slideshow-image';
import 'react-slideshow-image/dist/styles.css';


// Default settings for the slider component.
const divSettings = {
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    backgroundSize: "cover"       
}

interface PhotoGalleryProps {
    photoUrls: Array<String>;
}

const PhotoGallery: FC<PhotoGalleryProps> = ({ photoUrls }) => {    
    return (        
        <Slide transitionDuration={200}>
        {photoUrls.map((photoUrls) => (
            <div style={divSettings}>
                <img src={photoUrls.toString()} width={"100%"}/>
            </div>
            ))}
        </Slide>             
    );
};


export default PhotoGallery;
