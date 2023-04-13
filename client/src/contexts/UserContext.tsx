import {
  Dispatch,
  ReactNode,
  SetStateAction,
  createContext,
  useContext,
  useEffect,
  useState,
} from "react";
import { UserProfile } from "@/generated";
import { useCookies } from "react-cookie";
import jwtDecode from "jwt-decode";

import { useRouter } from "next/router";
import useApi from "@/hooks/useApi";

type JwtPayload = {
  email: string;
  // user id
  sub: string;
};

interface UserContextProps {
  user: UserProfile | null;
  setUser: Dispatch<SetStateAction<UserProfile | null>>;
  logout: () => void;
  refetchUser: () => void;
  isLoading: boolean;
}

interface UserContextProviderProps {
  children: ReactNode;
}

const UserContext = createContext<UserContextProps>({
  user: null,
  setUser: () => null,
  logout: () => null,
  refetchUser: () => null,
  isLoading: true,
});

const UserContextProvider = ({ children }: UserContextProviderProps) => {
  const [user, setUser] = useState<UserProfile | null>(null);
  const [cookies, setCookie, removeCookie] = useCookies(["token"]);
  const [isLoading, setIsLoading] = useState(true);

  const router = useRouter();

  const { apiManager, token } = useApi();

  const logout = () => {
    removeCookie("token");
    setUser(null);
    router.push("/login");
  };

  useEffect(() => {
    refetchUser();
  }, []);

  const refetchUser = (): void => {
    setIsLoading(true);
    if (!token) return setIsLoading(false);
    const payload = jwtDecode(token) as JwtPayload;
    apiManager.apiV1UsersUserIdProfileGet({ userId: payload.sub }).then(res => {
      setUser(res);
      setIsLoading(false);
      if (res.name === undefined) {
        router.push("/finish-auth");
      }
    });
  };

  // Redirect if user not signed in or didnt finish regestration
  useEffect(() => {
    if (!isLoading) {
      if (!user) {
        router.push("/login");
      } else {
        if (!user.name) {
          router.push("/finish-auth");
        }
      }
    }
  }, [router.asPath, isLoading]);

  return (
    <UserContext.Provider
      value={{ user, setUser, logout, refetchUser, isLoading }}
    >
      {children}
    </UserContext.Provider>
  );
};

export { UserContextProvider, UserContext };
