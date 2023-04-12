import React, { CSSProperties, FC, useRef } from "react";

import styles from "./Popup.module.scss";

interface PopupProps {
  visible: boolean;
  setVisible?: (v: boolean) => void;
  children?: any;
  containerStyle?: CSSProperties;
}

const Popup: FC<PopupProps> = ({
  visible,
  setVisible,
  children,
  containerStyle,
}) => {
  const popupRef = useRef<any>();

  React.useEffect(() => {
    const handler = (e: MouseEvent) => {
      if (!popupRef.current.contains(e.target) && setVisible && visible) {
        setVisible(false);
      }
    };

    document.addEventListener("mousedown", handler);

    return () => {
      document.removeEventListener("mousedown", handler);
    };
  }, [visible]);

  return (
    <div className={`overlay ${visible ? "show" : "hide"}`}>
      <div
        ref={popupRef}
        className="modal"
        style={{ ...containerStyle }}
        onClick={e => {
          // setVisible(false);
          e.stopPropagation();
        }}
      >
        {children}
      </div>
    </div>
  );
};

export default Popup;
