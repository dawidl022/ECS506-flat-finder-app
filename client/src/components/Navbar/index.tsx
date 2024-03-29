import React from "react";
import styles from "./Navbar.module.scss";
import UserCard from "./UserCard";
import Link from "next/link";
import useUser from "@/hooks/useUser";

const Navbar = () => {
  const { user } = useUser();
  const [isActive, setIsActive] = React.useState(false);

  const changeBackground = () => {
    if (window.scrollY >= 30) setIsActive(true);
    else setIsActive(false);
  };

  React.useEffect(() => {
    document.addEventListener("scroll", changeBackground);

    return () => {
      document.removeEventListener("scroll", changeBackground);
    };
  }, []);

  return (
    <nav className={isActive ? styles.wrapperActive : styles.wrapper}>
      <div className="container">
        <div className={styles.navbarInner}>
          <Link href="/">
            <img src="/FDM.png" alt="logo" className={styles.logo} />
          </Link>
          {user ? (
            <UserCard />
          ) : (
            <Link href="/login">
              <p className={styles.loginBtn}>Log in</p>
            </Link>
          )}
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
