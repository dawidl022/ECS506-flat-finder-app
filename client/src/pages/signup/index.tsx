import React from "react";

import styles from "./SignUp.module.scss";

const SignUp = () => {
  const handleSignUp = () => {
    // TODO:
    alert("Handle sign up");
  };

  return (
    <div className={styles.wrapper}>
      <h2>Sign up</h2>
      <button onClick={() => handleSignUp()} className={styles.googleBtn}>
        <img src="/google.svg" />
        <p>Sign in with Google</p>
      </button>
    </div>
  );
};

export default SignUp;
