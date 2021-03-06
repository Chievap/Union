import { CommitOptions, createStore, DispatchOptions, Store } from "vuex";
import { user, UserModuleStateInterface } from "@/store/modules/user";
import { ActionsInterface as userActions } from "@/actions/user";
import { ActionsInterface as unionActions } from "@/actions/union";
import { ActionsInterface as unionsActions } from "@/actions/unions";
import { ActionsInterface as postActions } from "@/actions/post";
import { ActionsInterface as inviteActions } from "@/actions/invite";
import { MutationsInterface as userMutations } from "@/mutations/user";
import { MutationsInterface as formMutations } from "@/mutations/form";
import { MutationsInterface as unionMutations } from "@/mutations/union";
import { MutationsInterface as unionsMutations } from "@/mutations/unions";
import { MutationsInterface as postMutations } from "@/mutations/post";
import { MutationsInterface as inviteMutations } from "@/mutations/invite";
import { form, FormModuleStateInterface } from "@/store/modules/form";
import { UnionModuleStateInterface, union } from "./modules/union";
import { posts, PostModuleStateInterface } from "@/store/modules/post";
import { invite, InviteModuleStateInterface } from "@/store/modules/invite";
import { UnionsModuleStateInterface, unions } from "@/store/modules/unions";

// More info: https://betterprogramming.pub/the-state-of-typed-vuex-the-cleanest-approach-2358ee05d230

export interface RootState {
  user: UserModuleStateInterface;
  form: FormModuleStateInterface;
  union: UnionModuleStateInterface;
  unions: UnionsModuleStateInterface;
  post: PostModuleStateInterface;
  invite: InviteModuleStateInterface;
}
export type MutationTypes = userMutations &
  formMutations &
  unionMutations &
  unionsMutations &
  postMutations &
  inviteMutations;
export type ActionTypes = userActions &
  unionActions &
  unionsActions &
  postActions &
  inviteActions;

// Override commit and dispatch to only accept our own typings
export interface StoreInterface
  extends Omit<Store<RootState>, "commit" | "getters" | "dispatch"> {
  commit<K extends keyof MutationTypes>(
    key: K,
    payload?: Parameters<MutationTypes[K]>[1],
    options?: CommitOptions
  ): ReturnType<MutationTypes[K]>;

  dispatch<K extends keyof ActionTypes>(
    key: K,
    payload?: Parameters<ActionTypes[K]>[1],
    options?: DispatchOptions
  ): ReturnType<ActionTypes[K]>;
}

export const store: StoreInterface = createStore<RootState>({
  modules: {
    user,
    form,
    union,
    posts,
    invite,
    unions,
  },
});
