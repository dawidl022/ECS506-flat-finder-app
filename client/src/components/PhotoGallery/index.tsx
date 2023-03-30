import { FC } from 'react';
import { Slide } from 'react-slideshow-image';
import 'react-slideshow-image/dist/styles.css';


// Default settings for the slider component.
const divSettings = {
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    backgroundSize: "cover",
    height: "350px"           
}

interface PhotoGalleryProps {
    photoUrls: Array<String>;
    width: String;
}

const PhotoGallery: FC<PhotoGalleryProps> = ({ photoUrls, width }) => {    
    return (
        <div style={{width:width.toString()}}>              
            <Slide transitionDuration={200}>
            {photoUrls.map((photoUrls) => (        
                <div style={divSettings}>
                    <img src={photoUrls.toString()} width={"100%"}/>
                </div>            
                ))}
            </Slide>                 
        </div>
    );
};


export default PhotoGallery;
