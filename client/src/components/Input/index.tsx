import React from "react";

import styles from "./Input.module.scss";

interface InputProps {
  label?: string;
  isRequired?: boolean;
  placeholder?: string;
  value?: string | number;
  setValue?: (val: string) => void;
  isReadOnly?: boolean;
  isDisabled?: boolean;
  isNumber?: boolean;
  limits?: { min: number; max: number };
}

const Input: React.FC<InputProps> = ({
  label,
  isRequired = false,
  placeholder,
  value,
  setValue,
  isReadOnly = false,
  isDisabled = false,
  isNumber = false,
  limits,
}) => {
  return (
    <div className={styles.wrapper}>
      <label htmlFor={`input-${label}`} className={styles.label}>
        {label} {isRequired && <span>*</span>}
      </label>
      <input
        min={limits?.min}
        max={limits?.max}
        type={isNumber ? "number" : "text"}
        // type=
        readOnly={isReadOnly}
        disabled={isDisabled}
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
