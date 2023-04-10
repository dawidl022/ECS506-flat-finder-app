import React from "react";

import styles from "./Input.module.scss";

interface InputProps {
  label?: string;
  isRequired?: boolean;
  placeholder?: string;
  value?: string;
  setValue?: (val: string) => void;
}

const Input: React.FC<InputProps> = ({
  label,
  isRequired = false,
  placeholder,
  value,
  setValue,
}) => {
  return (
    <div className={styles.wrapper}>
      <label htmlFor={`input-${label}`} className={styles.label}>
        {label} {isRequired && <span>*</span>}
      </label>
      <input
        id={`input-${label}`}
        placeholder={placeholder}
        value={value}
        required={isRequired}
        onChange={e => setValue && setValue(e.target.value)}
      />
    </div>
  );
};

export default Input;
