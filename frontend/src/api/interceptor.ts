import axios, { AxiosRequestConfig } from "axios";
import Cookie from "js-cookie";

axios.interceptors.request.use(
  function(config: AxiosRequestConfig) {
    if (
      !config.url ||
      config.url?.indexOf("register") > -1 ||
      config.url?.indexOf("login") > -1 ||
      config.url?.indexOf("validate") > -1
    )
      return config;

    config.withCredentials = false;
    config.headers.Authorization = Cookie.get("Authorization");

    return config;
  },
  function(error) {
    return Promise.reject(error);
  }
);
