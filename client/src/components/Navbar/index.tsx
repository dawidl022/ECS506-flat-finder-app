import React from "react";

import styles from "./Navbar.module.scss";
import UserCard from "./UserCard";
import Link from "next/link";
import useUser from "@/hooks/useUser";

const Navbar = () => {
  const { user } = useUser();
  return (
    <nav className={styles.wrapper}>
      <div className="container">
        <div className={styles.navbarInner}>
          <Link href="/">
            <h1>Logo</h1>
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
