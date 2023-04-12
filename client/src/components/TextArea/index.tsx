import React from "react";

import styles from "./TextArea.module.scss";

interface TextAreaProps {
  label?: string;
  isRequired?: boolean;
  placeholder?: string;
  value?: string;
  setValue?: (val: string) => void;
}

const TextArea: React.FC<TextAreaProps> = ({
  label,
  isRequired,
  placeholder,
  value,
  setValue,
}) => {
  return (
    <div className={styles.wrapper}>
      <label htmlFor={`input-${label}`} className={styles.label}>
        {label} {isRequired && <span>*</span>}
      </label>
      <textarea
        id={`input-${label}`}
        placeholder={placeholder}
        value={value}
        required={isRequired}
        onChange={e => setValue && setValue(e.target.value)}
      />
    </div>
  );
};

export default TextArea;
