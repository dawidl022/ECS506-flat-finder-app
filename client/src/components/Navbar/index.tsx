import React from "react";

import styles from "./Navbar.module.scss";
import UserCard from "./UserCard";
import Link from "next/link";
import { useUser } from "@/contexts/UserContext";
import { Configuration, DefaultApi } from "@/generated";
import { useCookies } from "react-cookie";
import jwtDecode from "jwt-decode";

type JwtPayload = {
  email: string;
  sub: string;
};

const Navbar = () => {
  const [cookies] = useCookies(["token"]);
  const { user, setUser } = useUser();

  React.useEffect(() => {
    if (!cookies.token) return;
    const payload = jwtDecode(cookies.token) as JwtPayload;
    new DefaultApi(
      new Configuration({
        basePath: "http://127.0.0.1:5000",
        accessToken: cookies.token,
      })
    )
      .apiV1UsersUserIdProfileGet({ userId: payload.sub })
      .then(res => {
        // console.log(res);
        setUser(res);
      });
  }, []);

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
