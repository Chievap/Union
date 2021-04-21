import {Module} from "vuex";
// @ts-ignore -> there are no types for this
import { getField, updateField } from 'vuex-map-fields';
import {RootState} from "@/store/store";
import {mutations} from "@/mutations/form"

export enum FORM_ID {
    REGISTER="REGISTER"
}

export interface FormModuleStateInterface {
    formId: FORM_ID | undefined,
    fields: {} | undefined,
    errors: {} | undefined
}

export type FormModuleState = FormModuleStateInterface

export const form: Module<FormModuleState, RootState> = {
    state: () => ({
        formId: undefined,
        fields: {},
        errors: undefined
    }),
    getters: {
        getField
    },
    mutations: {
        updateField,
        ...mutations
    }
}
