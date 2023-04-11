import React, { useRef, useState } from "react";

import styles from "./UserCard.module.scss";
import { useRouter } from "next/router";
import useUser from "@/hooks/useUser";
import AvatarPlaceholder from "@/components/AvatarPlaceholder";
import useApi from "@/hooks/useApi";

const UserCard = () => {
  const router = useRouter();
  const { user, logout } = useUser();
  const { apiManager } = useApi();
  const [isAdmin, setIsAdmin] = useState(false);

  const [isOpen, setIsOpen] = useState(false);

  const menuRef = useRef<any>();
  const popupState = React.useRef(isOpen);

  React.useEffect(() => {
    popupState.current = isOpen;
  }, [isOpen]);

  const checkIsAdmin = () => {
    apiManager
      .apiV1AdminsUserIdGet({ userId: user?.id as string })
      .then(() => setIsAdmin(true));
  };

  React.useEffect(() => {
    if (user?.id) checkIsAdmin();
  }, [user]);

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
        <p>
          {user?.name?.split(" ")[0] + " " + user?.name?.split(" ")[1][0] + "."}
        </p>
        <AvatarPlaceholder
          size={42}
          addStyles={{ margin: "0 6px 0 12px" }}
          name={user?.name as string}
        />
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
          {isAdmin && (
            <button
              className={styles.menuItem}
              onClick={() => {
                setIsOpen(false);
                router.push("/admin");
              }}
            >
              <div className={styles.iconCon}>
                <img src="/icons/admin.svg" />
              </div>
              <p>Admin</p>
            </button>
          )}
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
