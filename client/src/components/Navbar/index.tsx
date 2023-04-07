import React from "react";

import styles from "./Navbar.module.scss";
import UserCard from "./UserCard";
import Link from "next/link";

const Navbar = () => {
  // TODO: create user context (for now just boolean)
  const user = true;

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
            <Link href="/signup">
              <p className={styles.loginBtn}>Sign up</p>
            </Link>
          )}
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
