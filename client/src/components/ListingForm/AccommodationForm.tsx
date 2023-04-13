import { FC, useState, FormEvent, ChangeEvent, useEffect } from "react";
import { useRouter } from "next/router";
import { handleFileInput } from "./handleFileInput";
import {
  AccommodationAddressCountryEnum,
  Configuration,
  DefaultApi,
} from "@/generated";
import useApi from "@/hooks/useApi";

import Input from "../Input";
import TextArea from "../TextArea";

import styles from "./Form.module.scss";
import useUser from "@/hooks/useUser";

import { toast } from "react-toastify";

interface FormProps {
  listingId: string;
  editExistingListing: Boolean;
}

const AccommodationForm: FC<FormProps> = ({
  listingId,
  editExistingListing,
}) => {
  const router = useRouter();
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [line1, setLine1] = useState("");
  const [line2, setLine2] = useState("");
  const [town, setTown] = useState("");
  const [postCode, setPostCode] = useState("");
  const [country] = useState("United Kingdom");
  const { user } = useUser();

  const [accommodationType, setAccommodationType] = useState("Flat");
  const [numberOfRooms, setNumberOfRooms] = useState("");
  const [price, setPrice] = useState("");

  const [photos, setPhotos] = useState<Blob[]>();

  const { apiManager: api } = useApi();

  const baseForm = {
    title,
    description,
    address: {
      line1,
      line2,
      town,
      postCode,
      country: AccommodationAddressCountryEnum.Uk,
    },
    accommodationType,
    numberOfRooms: parseInt(numberOfRooms),
    price: parseInt(price),
  };

  useEffect(() => {
    if (editExistingListing) {
      api
        .apiV1ListingsAccommodationListingIdGet({ listingId })
        .then(res => {
          setTitle(res.title);
          setDescription(res.description);
          setLine1(res.address.line1);
          //as line2 is optional, check if there is an input
          setLine2(res.address.line2 ?? "");
          setTown(res.address.town);
          setPostCode(res.address.postCode);
          setAccommodationType(res.accommodationType);
          setNumberOfRooms(res.numberOfRooms.toString());
          setPrice(res.price.toString());
        })
        .catch(err => {
          alert(
            `Could not find listing with ID:  ${listingId} \nError:  ${err}`
          );
        });
    }
  }, []);

  const preview = () => {
    router.push({
      pathname: "/AccommodationPreviewPage",
      query: {
        title,
        description,
        line1,
        line2,
        town,
        postCode,
        country,
        accommodationType,
        numberOfRooms,
        price,
      },
    });
  };

  const checkInputs = () => {
    if (
      title &&
      description &&
      line1 &&
      town &&
      postCode &&
      price &&
      numberOfRooms
    ) {
      return true;
    } else {
      return false;
    }
  };

  const handleSubmit = (e: FormEvent<HTMLElement>) => {
    e.preventDefault();
    if (!editExistingListing) {
      api
        .apiV1ListingsAccommodationPost({
          ...baseForm,
          photos: photos ?? [],
        })
        .then(() => {
          toast.success("Listing is added", {
            position: "top-right",
            autoClose: 5000,
            hideProgressBar: true,
            closeOnClick: true,
            pauseOnHover: true,
            draggable: true,
            progress: undefined,
            theme: "light",
          });
          router.push({ pathname: `/profile/${user?.id}` });
        })

        .catch(err =>
          alert(
            "Accommodation listing failed to be published. \nError: " +
              err.message
          )
        );
    } else {
      api
        .apiV1ListingsAccommodationListingIdPut({
          listingId,
          accommodationFormBase: {
            ...baseForm,
          },
        })
        .then(() => {
          toast.success("Listing is changed", {
            position: "top-right",
            autoClose: 5000,
            hideProgressBar: true,
            closeOnClick: true,
            pauseOnHover: true,
            draggable: true,
            progress: undefined,
            theme: "light",
          });
          router.push({ pathname: `/profile/${user?.id}` });
        })
        .catch(err => {
          alert("Error whilst updating listing. \nError: " + err);
        });
    }
  };

  return (
    <div className={styles.wrapper}>
      <h2 className={styles.title}>Accommodation Form</h2>
      <form className={styles.form} onSubmit={handleSubmit}>
        <section className={styles.inputs}>
          <Input label="Title" isRequired value={title} setValue={setTitle} />

          <TextArea
            label="Description"
            value={description}
            setValue={setDescription}
            isRequired
          />
        </section>
        <section className={styles.inputsAddress}>
          {/* <fieldset> */}
          <Input
            label="Address Line 1"
            isRequired
            value={line1}
            setValue={setLine1}
          />
          <Input label="Address Line 2" value={line2} setValue={setLine2} />
          <Input label="Town" isRequired value={town} setValue={setTown} />
          <Input
            label="Post Code"
            isRequired
            value={postCode}
            setValue={setPostCode}
          />

          <Input
            isReadOnly
            isDisabled
            label="Country"
            // isRequired
            value={country}
          />
          {/* </fieldset> */}
        </section>
        <section className={styles.inputs}>
          <Input
            label="Price"
            isRequired
            value={price}
            setValue={v => setPrice(v)}
            isNumber
          />
          <Input
            label="Number of Rooms"
            isRequired
            value={numberOfRooms}
            setValue={v => setNumberOfRooms(v)}
            isNumber
            limits={{ min: 0, max: 10 }}
          />

          <label className={styles.label} htmlFor="type">
            Type <span>*</span>
          </label>
          <select
            id="type"
            value={accommodationType}
            onChange={e => setAccommodationType(e.target.value)}
          >
            <option value={"Flat"}>Flat</option>
            <option value={"Detached"}>Detached House</option>
            <option value={"Semi-detached"}>Semi-detached House</option>
            <option value={"Terraced"}>Terraced House</option>
            <option value={"Bungalows"}>Bungalows</option>
          </select>

          {!editExistingListing && (
            <div className={styles.fileUploadCon}>
              <label className={styles.label}>
                Picture <span>*</span>{" "}
                <span className={styles.details}>
                  {"(from 1 to 15 photos)"}
                </span>
              </label>
              <label className={styles.labelBtn} htmlFor="photos">
                <img src="/icons/upload.svg" /> Upload photo
              </label>
              <input
                type="file"
                onChange={e => {
                  if (e.target.files != null) {
                    handleFileInput(e);
                    setPhotos(Array.from(e.target.files));
                  }
                }}
                id="photos"
                accept="image/*"
                multiple
                required
              />
              {photos && photos.length > 0 && (
                <p>Uploaded photos: {photos.length}</p>
              )}
            </div>
          )}
        </section>

        <section className={styles.btnCon}>
          <button className={styles.addBtn}>
            {editExistingListing ? "Save" : "Create"}
          </button>
        </section>
      </form>
    </div>
  );
};

export default AccommodationForm;
