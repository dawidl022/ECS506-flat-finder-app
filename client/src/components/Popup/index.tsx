"use client";
import React, { CSSProperties, FC, useRef, useState } from "react";

import styles from "./Popup.module.scss";

import ReactDOM from "react-dom";

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
  const [isBrowser, setIsBrowser] = useState(false);

  React.useEffect(() => {
    setIsBrowser(true);
  }, []);

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
  if (isBrowser)
    return ReactDOM.createPortal(
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
      </div>,
      document.getElementById("portal") as HTMLElement
    );
  return <div></div>;

  // return (
  //   <div className={`overlay ${visible ? "show" : "hide"}`}>
  //     <div
  //       ref={popupRef}
  //       className="modal"
  //       style={{ ...containerStyle }}
  //       onClick={e => {
  //         // setVisible(false);
  //         e.stopPropagation();
  //       }}
  //     >
  //       {children}
  //     </div>
  //   </div>
  // );
};

export default Popup;
