import React, { useRef, useState } from "react";

import styles from "./UserCard.module.scss";
import { useRouter } from "next/router";
import useUser from "@/hooks/useUser";

const UserCard = () => {
  const router = useRouter();
  const { user, logout } = useUser();

  const [isOpen, setIsOpen] = useState(false);

  const menuRef = useRef<any>();
  const popupState = React.useRef(isOpen);

  React.useEffect(() => {
    popupState.current = isOpen;
  }, [isOpen]);

  React.useEffect(() => {
    const handler = (e: MouseEvent) => {
      if (!menuRef.current.contains(e.target)) {
        setIsOpen(false);
      }
    };
    const keyPressHandler = (event: KeyboardEvent) => {
      if (event.code === "Escape" && popupState.current === true) {
        setIsOpen(false);
      }
    };

    document.addEventListener("mousedown", handler);
    document.addEventListener("keydown", keyPressHandler);

    return () => {
      document.removeEventListener("mousedown", handler);
      document.removeEventListener("keydown", keyPressHandler);
    };
  }, []);
  return (
    <div className={styles.cardCon} ref={menuRef}>
      <button
        onClick={() => setIsOpen(prev => !prev)}
        className={styles.wrapper}
      >
        <p>{user?.email}</p>
        <div className={styles.avaCon} />
        <div className={styles.arrCon}>
          <img
            style={isOpen ? { transform: "scaleY(-1)" } : {}}
            src="/icons/arrDown.svg"
          />
        </div>
      </button>
      {isOpen && (
        <div className={styles.dropDown}>
          <button
            onClick={() => {
              setIsOpen(false);
              router.push(`/profile/${user?.id}`);
            }}
            className={styles.menuItem}
          >
            <div className={styles.iconCon}>
              <img src="/icons/user.svg" />
            </div>
            <p>Profile</p>
          </button>
          <button
            className={styles.menuItem}
            onClick={() => {
              setIsOpen(false);
              router.push("/listings");
            }}
          >
            <div className={styles.iconCon}>
              <img src="/icons/book.svg" />
            </div>
            <p>Listing</p>
          </button>
          <button
            onClick={() => {
              setIsOpen(false);
              logout();
              router.push("/auth");
            }}
            className={styles.menuItem}
          >
            <div className={styles.iconCon}>
              <img src="/icons/exit.svg" />
            </div>
            <p>Exit</p>
          </button>
        </div>
      )}
    </div>
  );
};

export default UserCard;
