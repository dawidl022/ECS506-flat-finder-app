import {
  Dispatch,
  ReactNode,
  SetStateAction,
  createContext,
  useContext,
  useState,
} from "react";
import { UserProfile } from "@/generated";

interface UserContextProps {
  user: UserProfile | null;
  setUser: Dispatch<SetStateAction<UserProfile | null>>;
}

interface UserContextProviderProps {
  children: ReactNode;
}

const UserContext = createContext<UserContextProps>({
  user: null,
  setUser: () => null,
});

const useUser = () => {
  return useContext(UserContext);
};

const UserContextProvider = ({ children }: UserContextProviderProps) => {
  const [user, setUser] = useState<UserProfile | null>(null);

  return (
    <UserContext.Provider value={{ user, setUser }}>
      {children}
    </UserContext.Provider>
  );
};

export { UserContextProvider, useUser };
