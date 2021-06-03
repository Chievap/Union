import ApiBase from "@/api/api-base";
import { AxiosResponse } from "axios";

export type UnionType = {
  name: string;
  description: string;
  members_can_invite: boolean;
  icon?: string;
  banner?: string;
};

export default class UnionApi extends ApiBase {
  public static postUnion = (data: any): Promise<any> => {
    return UnionApi.requestPost("unions", { data }).then(response => response);
  };

  public static getUnion = (
    name: string
  ): Promise<AxiosResponse<UnionType>> => {
    return UnionApi.requestGet<UnionType>("unions", name);
  };

  public static getUnions = (): Promise<AxiosResponse<UnionType>> => {
    return UnionApi.requestGetAll<UnionType>("unions/overview");
  };

  public static postUnionImages = (data: any):Promise<any> => {
    console.log(data)
    return UnionApi.requestPostWithHeaders("unions/images/",  data ).then(response => response);
  }
}
