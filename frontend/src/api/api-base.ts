import axios, { AxiosRequestConfig, AxiosResponse } from "axios";

export default class ApiBase {
  private static BASE_URL = "http://127.0.0.1:8000"; // TODO: Replace with env var

  protected static async executeRequest<T = any>(
    method: "get" | "delete" | "post" | "put",
    url: string,
    config?: AxiosRequestConfig,
    data?: T
  ): Promise<AxiosResponse<T>> {
    const response = await axios.request({
      method,
      url: `${this.BASE_URL}${url}`,
      withCredentials: true,
      data: data,
      ...config,
    });
    return response;
  }

  public static async requestGet<T = any>(
    resource: string,
    id: string,
    config?: AxiosRequestConfig
  ) {
    return this.executeRequest<T>("get", `/${resource}/${id}`, {
      ...config,
    });
  }

  public static async requestGetAll<T = any>(
    resource: string,
    config?: AxiosRequestConfig
  ) {
    return this.executeRequest<T>("get", `/${resource}`, {
      ...config,
    });
  }

  public static async requestPost<T = any>(
    resource: string,
    config?: AxiosRequestConfig,
    data?: T
  ) {
    return this.executeRequest<T>(
      "post",
      `/${resource}`,
      {
        ...config,
      },
      data
    );
  }
  public static async requestDelete<T = any>(
    resource: string,
    id: string,
    config?: AxiosRequestConfig
  ) {
    return this.executeRequest<T>("delete", `/${resource}/${id}`, {
      ...config,
    });
  }
}
