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
      <p className={styles.label}>
        {label} {isRequired && <span>*</span>}
      </p>
      <input
        placeholder={placeholder}
        value={value}
        onChange={e => setValue && setValue(e.target.value)}
      />
    </div>
  );
};

export default Input;
