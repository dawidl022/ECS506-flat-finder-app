import React from "react";

import styles from "./AvatarPlaceholder.module.scss";

interface AvatarPlaceholderProps {
  name: string;
  addStyles?: React.CSSProperties;
  size: number;
}

const AvatarPlaceholder: React.FC<AvatarPlaceholderProps> = ({
  name,
  addStyles = {},
  size,
}) => {
  return (
    <div
      style={{ ...addStyles, width: size, height: size }}
      className={styles.wrapper}
    >
      <p style={{ fontSize: size / 2 - 5 }}>{name && name[0]}</p>
    </div>
  );
};

export default AvatarPlaceholder;
