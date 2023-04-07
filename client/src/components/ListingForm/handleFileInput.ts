import { ChangeEvent } from "react";
export const handleFileInput = (e: ChangeEvent<HTMLInputElement>) => {
  const files = e.target.files;
  //check if there are more than 15 files selected
  if (files && files.length > 0) {
    if (files.length > 15) {
      alert("You can upload up to 15 files");
      e.target.value = "";
    }

    //check if the file size is greater than 5MB
    for (let i = 0; i < files.length; i++) {
      if (files[i].size > 5242880) {
        alert(`The maximum file size is 5MB`);
        e.target.value = "";
      }
    }
  }
};
