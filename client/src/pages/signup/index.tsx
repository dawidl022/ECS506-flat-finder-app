import React from "react";

import styles from "./SignUp.module.scss";
import { Configuration, DefaultApi } from "@/generated";

const SignUp = () => {
  // const handleSignUp = () => {
  //   // TODO:
  //   new DefaultApi(new Configuration({ basePath: "http://localhost:5000", accessToken: string }))
  //     .apiV1ListingsAccommodationGet({
  //       location: "London",
  //       radius: 20,
  //     })
  //     .then(res => console.log(res))
  //     .catch(er => console.log(er));
  //   // fetch("http://127.0.0.1:5000/api/v1/listings/accommodation");
  //   console.log("123");
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
