import React, { useRef, useState } from "react";

import styles from "./UserCard.module.scss";
import { useRouter } from "next/router";

const UserCard = () => {
  const router = useRouter();

  const [isOpen, setIsOpen] = useState(false);
  let menuRef = useRef<any>();

  React.useEffect(() => {
    let handler = (e: MouseEvent) => {
      if (!menuRef.current.contains(e.target)) {
        setIsOpen(false);
      }
    };

    document.addEventListener("mousedown", handler);

    return () => {
      document.removeEventListener("mousedown", handler);
    };
  }, []);
  return (
    <div ref={menuRef}>
      <div onClick={() => setIsOpen(prev => !prev)} className={styles.wrapper}>
        <p>username</p>
        <div className={styles.avaCon} />
        <div className={styles.arrCon}>
          <img
            style={isOpen ? { transform: "scaleY(-1)" } : {}}
            src="/icons/arrDown.svg"
          />
        </div>
      </div>
      {isOpen && (
        <div className={styles.dropDown}>
          <div
            onClick={() => {
              setIsOpen(false);
              router.push("/profile/seagull");
            }}
            className={styles.menuItem}
          >
            <div className={styles.iconCon}>
              <img src="/icons/user.svg" />
            </div>
            <p>Profile</p>
          </div>
          <div
            className={styles.menuItem}
            onClick={() => {
              setIsOpen(false);
              // TODO:
              router.push("/listings");
            }}
          >
            <div className={styles.iconCon}>
              <img src="/icons/book.svg" />
            </div>
            <p>Listing</p>
          </div>
          <div
            onClick={() => {
              setIsOpen(false);
              // TODO: exit logic (delete cookie)
            }}
            className={styles.menuItem}
          >
            <div className={styles.iconCon}>
              <img src="/icons/exit.svg" />
            </div>
            <p>Exit</p>
          </div>
        </div>
      )}
    </div>
  );
};

export default UserCard;
