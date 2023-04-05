import React from "react";
import Navbar from "../Navbar";

const Layout = ({ children }: any) => {
  return (
    <div>
      <Navbar />
      <div style={{ paddingTop: 100 }}>{children}</div>
    </div>
  );
};

export default Layout;
