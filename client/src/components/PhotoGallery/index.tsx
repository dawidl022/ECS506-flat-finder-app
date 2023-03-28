import { FC } from 'react';
import { Slide } from 'react-slideshow-image';
import 'react-slideshow-image/dist/styles.css';
import { Accommodation } from '../../generated/models/Accommodation';


// Default settings for the slider component.
const divSettings = {
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    backgroundSize: "cover",
    height: "350px",    
}

interface accomodationProps {
    accomodation: Accommodation;
}

const PhotoGallery: FC<accomodationProps> = ({ accomodation }) => {
    const images = accomodation.photoUrls;
    return (
        <div style={{width:"350px", height: "350px"}}>
            <Slide>
            {images.map((images) => (
                <div style={divSettings}>
                    <img src={images} width={350} height={350}/>
                </div>
                ))}
            </Slide>    
        </div>         
    );
};


export default PhotoGallery;
