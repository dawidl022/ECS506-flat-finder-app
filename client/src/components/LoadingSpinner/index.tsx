import React, { CSSProperties, FC } from "react";
import { Circles } from "react-loader-spinner";

import styles from "./LoadingSpinner.module.scss";

interface LoadingSpinnerProps {
  conStyles?: CSSProperties;
}

const LoadingSpinner: FC<LoadingSpinnerProps> = ({ conStyles }) => {
  return (
    <div className={styles.wrapper} style={conStyles}>
      <Circles
        height="80"
        width="80"
        color="#4285f4"
        ariaLabel="circles-loading"
        wrapperStyle={{}}
        wrapperClass=""
        visible={true}
      />
    </div>
  );
};

export default LoadingSpinner;
