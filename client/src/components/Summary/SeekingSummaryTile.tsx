import { FC } from 'react';
import Link from 'next/link';
import { AccommodationSummary } from '@/generated/models/AccommodationSummary';

interface seekingSummaryProps {
    accomodation: AccommodationSummary;
}

const SeekingSummaryTile: FC<seekingSummaryProps> = ({ accomodation }) => {
    return (
        <div>
            <Link href={ `/listings/accommodation/${accomodation.id}` }>                
                <p> { accomodation.title } </p>
                <p> { `£${accomodation.price}` } </p>
                <p> { accomodation.shortDescription } </p>
                <p> { accomodation.accommodationType } </p>
                <p> { accomodation.numberOfRooms } </p>
                <p> { accomodation.postCode }  </p>
                <p> { accomodation.source } </p>
            </Link>
        </div>
    );
};

export default SeekingSummaryTile;