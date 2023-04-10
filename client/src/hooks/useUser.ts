import { UserContext } from "@/contexts/UserContext";
import { useContext } from "react";

const useUser = () => {
  return useContext(UserContext);
};

export default useUser;
