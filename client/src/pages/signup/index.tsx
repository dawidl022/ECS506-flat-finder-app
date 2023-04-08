import React from "react";

import styles from "./SignUp.module.scss";
import { Configuration, DefaultApi } from "@/generated";

const SignUp = () => {
  // const handleSignUp = () => {
  //   const loginUrl = "http://127.0.0.1:5000/api/v1/login/google";
  //   window.open(loginUrl, "_self", "width=500,height=600");
  // };

  return (
    <div className={styles.wrapper}>
      <h2>Sign up</h2>
      <form action="http://127.0.0.1:5000/api/v1/login/google" method="POST">
        <button className={styles.googleBtn}>
          <img src="/google.svg" />
          <p>Sign in with Google</p>
        </button>
      </form>
    </div>
  );
};

export default SignUp;
