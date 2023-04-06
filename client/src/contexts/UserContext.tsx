import {
  Dispatch,
  ReactNode,
  SetStateAction,
  createContext,
  useState,
} from "react";

interface UserContextProps {
  user: any;
  token: string;
  setUser: Dispatch<SetStateAction<any>>;
  setToken: Dispatch<SetStateAction<string>>;
}

interface UserContextProviderProps {
  children: ReactNode;
}

const UserContext = createContext<UserContextProps>({
  user: {},
  token: "",
  setUser: () => {},
  setToken: () => {},
});

const UserContextProvider = ({ children }: UserContextProviderProps) => {
  const [user, setUser] = useState({});
  const [token, setToken] = useState("");

  return (
    <UserContext.Provider value={{ user, setUser, token, setToken }}>
      {children}
    </UserContext.Provider>
  );
};

export { UserContextProvider, UserContext };
