import React from "react";

import styles from "./Auth.module.scss";
import { Configuration, DefaultApi } from "@/generated";

const Auth = () => {
  return (
    <div className={styles.wrapper}>
      <h2>Welcome</h2>
      <form action="http://127.0.0.1:5000/api/v1/login/google" method="POST">
        <button className={styles.googleBtn}>
          <img src="/google.svg" />
          <p>Sign in with Google</p>
        </button>
      </form>
    </div>
  );
};

export default Auth;
