import { FC, useState, FormEvent, ChangeEvent, useEffect } from "react";
import { useRouter } from "next/router";
import { Configuration, DefaultApi } from "@/generated";
import { handleFileInput } from "./handleFileInput";
import useApi from "@/hooks/useApi";
import useUser from "@/hooks/useUser";

import styles from "./Form.module.scss";
import Input from "../Input";
import TextArea from "../TextArea";

import { toast } from "react-toastify";

interface FormProps {
  listingId: string;
  editExistingListing: Boolean;
}

// {"author":
// {"name":"Ivan Seagull",
// "userProfile":{"contactDetails":{"phoneNumber":"13131313"},
// "email":"ivan.seagull.k@gmail.com","id":"e7cf519d-9011-45a0-9505-0861aef17444","name":"Ivan Seagull"}},
// "contactInfo":{"email":"ivan.seagull.k@gmail.com","phoneNumber":"13131313"},
// "description":"313131313","id":"internal_457498e6-0647-44da-a412-38de407626a4",
// "photoUrls":[],"preferredLocation":"london","title":"1313131"}

const SeekingForm: FC<FormProps> = ({ listingId, editExistingListing }) => {
  const router = useRouter();
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [location, setLocation] = useState("");
  const { apiManager: api } = useApi();
  const { user } = useUser();
  const [photos, setPhotos] = useState<Blob[]>();

  useEffect(() => {
    if (editExistingListing) {
      api
        .apiV1ListingsSeekingListingIdGet({ listingId })
        .then(res => {
          setTitle(res.title);
          setDescription(res.description);
          setLocation(res.preferredLocation);
          setPhotos(res.photoUrls?.map(url => new Blob([url])) ?? []);
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
      pathname: "/SeekingPreviewPage",
      query: {
        title,
        description,
        location,
      },
    });
  };

  const checkInputs = () => {
    if (title && description && location) {
      return true;
    } else {
      return false;
    }
  };

  const handleSubmit = (e: FormEvent<HTMLElement>) => {
    e.preventDefault();
    const baseForm = {
      title,
      description,
      preferredLocation: location,
    };

    if (!editExistingListing) {
      api
        .apiV1ListingsSeekingPost({
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
            "Seeking listing failed to be published. \nError: " + err.message
          )
        );
    } else {
      api
        .apiV1ListingsSeekingListingIdPut({
          listingId,
          seekingFormBase: {
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
      <h2 className={styles.title}>Seeking Form</h2>
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
        <section className={styles.inputs}>
          <Input
            label="Location"
            isRequired
            value={location}
            setValue={setLocation}
          />

          {!editExistingListing && (
            <div className={styles.fileUploadCon}>
              <label className={styles.label}>
                Picture <span></span>{" "}
                <span className={styles.details}>
                  {"(from 0 to 15 photos)"}
                </span>
              </label>
              <label className={styles.labelBtn} htmlFor="photos">
                <img src="/icons/upload.svg" /> Upload photo
              </label>
              <input
                type="file"
                id="photos"
                onChange={e => {
                  if (e.target.files != null) {
                    handleFileInput(e);
                    setPhotos(Array.from(e.target.files));
                  }
                }}
                accept="image/*"
                multiple
              />
            </div>
          )}
        </section>
        <section className={styles.btnCon}>
          <button
            className={styles.previewBtn}
            type="button"
            onClick={preview}
            disabled={!checkInputs()}
          >
            Preview
          </button>
          <button className={styles.addBtn}>
            {editExistingListing ? "Save" : "Create"}
          </button>
        </section>
      </form>
    </div>
  );
};

export default SeekingForm;
