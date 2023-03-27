import { FC } from 'react';
import Link from 'next/link';
//import from generated/models
import AccomodationSummary  from '../../generated/models/AccomodationSummary';
interface accomodationSummaryProps {
    accomodation: AccomodationSummary;
}

const AccomodationSummaryTile: FC<accomodationSummaryProps> = ({ accomodation }) => {
    return (
        <div>
            <Link href={ `/listings/accommodation/${accomodation.id}` }>                
                <img src={ accomodation.thumbnailUrl } width={150} height={150} alt={`listing ${accomodation.id}`}/>
                <p> { accomodation.title } </p>
                <p> { `£${accomodation.price}` } </p>
                <p> { accomodation.shortDescription } </p>
                <p> { accomodation.accommodationType } </p>
                <p> { accomodation.numberOfRooms } </p>
            </Link>
        </div>
    );
};

export default AccomodationSummaryTile;