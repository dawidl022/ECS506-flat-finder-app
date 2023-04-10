import React from "react";

import styles from "./EditingButtonComponent.module.scss";

interface EditingButtonProps {
  setIsEditing: (v: boolean) => void;
}

const EditingButton: React.FC<EditingButtonProps> = ({ setIsEditing }) => {
  return (
    <button onClick={() => setIsEditing(true)} className={styles.wrapper}>
      Edit profile
    </button>
  );
};

export default EditingButton;
