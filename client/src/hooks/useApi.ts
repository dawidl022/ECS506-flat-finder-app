import { Configuration, DefaultApi } from "@/generated";
import { useCookies } from "react-cookie";

const useApi = (givenToken = "") => {
  let cookiesObj;
  try {
    const [cookies] = useCookies(["token"]);
    cookiesObj = cookies;
  } catch (error) {}
  const basePath = "http://127.0.0.1:5000";
  const token = cookiesObj?.token || givenToken;

  const config = new Configuration({ basePath, accessToken: token });

  const apiManager = new DefaultApi(new Configuration(config));

  return { apiManager, token };
};

export default useApi;
