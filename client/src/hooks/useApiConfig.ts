import { useCookies } from "react-cookie";

const useApiConfig = () => {
  const [cookies] = useCookies(["token"]);

  const basePath = "http://127.0.0.1:5000";
  const token = cookies.token;
  return { config: { basePath, accessToken: token }, token };
};

export default useApiConfig;
