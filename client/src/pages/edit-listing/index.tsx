import { useRouter } from 'next/router';
import { GetServerSideProps, NextPage } from 'next';
import EditListing from '@/components/EditListing/EditListing';
import { UserListingsInner, UserListingsInnerTypeEnum } from '@/generated/models/UserListingsInner';

interface EditListingProps {
    id: string;
    type: UserListingsInnerTypeEnum;
  }
  
  const EditPage: NextPage<EditListingProps> = ({ id, type }) => {
    return (
      <div className="container">
        <h1>Edit Listing</h1>
        <EditListing listingType={type} listingId={id} />
      </div>
    );
  };
  
  export const getServerSideProps: GetServerSideProps<EditListingProps> = async (
    context
  ) => {
    const { id, type } = context.query;
  
    if (!id || !type) {
      return {
        redirect: {
          destination: '/',
          permanent: false,
        },
      };
    }
  
    return {
      props: {
        id: id as string,
        type: type as UserListingsInnerTypeEnum,
      },
    };
  };
  
export default EditPage;
