import {
  Dispatch,
  ReactNode,
  SetStateAction,
  createContext,
  useContext,
  useEffect,
  useState,
} from "react";
import { Configuration, DefaultApi, UserProfile } from "@/generated";
import { useCookies } from "react-cookie";
import jwtDecode from "jwt-decode";
import useApiConfig from "@/hooks/useApiConfig";
import { useRouter } from "next/router";

type JwtPayload = {
  email: string;
  sub: string;
};

interface UserContextProps {
  user: UserProfile | null;
  setUser: Dispatch<SetStateAction<UserProfile | null>>;
  logout: () => void;
}

interface UserContextProviderProps {
  children: ReactNode;
}

const UserContext = createContext<UserContextProps>({
  user: null,
  setUser: () => null,
  logout: () => null,
});

const UserContextProvider = ({ children }: UserContextProviderProps) => {
  const [user, setUser] = useState<UserProfile | null>(null);
  const [cookies, setCookie, removeCookie] = useCookies(["token"]);
  const [isLoading, setIsLoading] = useState(true);

  const router = useRouter();

  const { config, token } = useApiConfig();

  const logout = () => {
    removeCookie("token");
    setUser(null);
    router.push("/auth");
  };

  useEffect(() => {
    setIsLoading(true);
    if (!token) return setIsLoading(false);
    const payload = jwtDecode(token) as JwtPayload;
    new DefaultApi(new Configuration(config))
      .apiV1UsersUserIdProfileGet({ userId: payload.sub })
      .then(res => {
        setUser(res);
        setIsLoading(false);
        if (res.name === undefined) {
          router.push("/finish-auth");
        }
      });
  }, []);

  // Redirect if user not signed in or didnt finish regestration
  useEffect(() => {
    if (!isLoading) {
      if (!user) {
        router.push("/auth");
      } else {
        if (!user.name) {
          router.push("/finish-auth");
        }
      }
    }
  }, [router.asPath, isLoading]);

  return (
    <UserContext.Provider value={{ user, setUser, logout }}>
      {children}
    </UserContext.Provider>
  );
};

export { UserContextProvider, UserContext };
