import { createStore } from 'vuex'
import { ref,reactive } from "vue";
import i18n from '@/lib/i18n/lang'
import api from '@/axios/api.js';
console.log('@store i18n.global.locale.value', i18n.global.locale.value);

const setLocalStorage = ( name, val) => {
    localStorage.setItem(name, val);
}

const store = createStore({
    state () {
        return {
            currLang: i18n.global.locale,
            // login: ref(false),
            order: [],
            langList:[
                {
                    value: 'en',
                    label: 'English',
                },{
                    value: 'jp',
                    label: '日本語',
                },{
                    value: 'zh',
                    label: '中文',
                }
            ],
            currUser: {},
            currOrder: {},
            lineProfile: {},
            prevRoute: {}
        }
    },
    getters:{
        currLang:state => {
            return state.currLang
        },
        langList:state => {
            return state.langList
        },
        order:state => {
            return state.order
        },
        // login:state=>{
        //     return state.login
        // },
        currOrder:state => {
            return state.currOrder
        },
        currUser:state => {
            return state.currUser
        },
        lineProfile:state => {
            return state.lineProfile
        },
        prevRoute:state => {
            return state.prevRoute
        },
    },
    actions:{
        order: ({commit}, order) => {
            commit("order", order)
        },
        // login:({commit})=>{
        //     commit("login")
        // },
        logout:({commit})=>{
            commit("logout")
        },
        setCurrLang:({commit}, lang)=>{
            commit("setCurrLang", lang)
        },
        setCurrUserData:({commit}, data)=>{
            commit("setCurrUserData", data)
        },
        signUp:({commit}, data)=>{
            commit("signUp", data)
        },
        getUserData:({commit}, id)=>{
            commit("getUserData", id)
        },
        setCurrOrder:({commit}, data)=>{
            commit("setCurrOrder", data)
        },
        setLineProfile:({commit}, data)=>{
            commit("setLineProfile", data)
        },
        setPrevRoute:({commit}, data)=>{
            commit("setPrevRoute", data)
        },
        signUpLine:async({commit}, data)=>{
            try {
                let signUpLineRes = await api.post(`/line_user`, data);
                console.log('@actions signUpLineRes.data',signUpLineRes.data);
                commit("signUpLine", signUpLineRes.data)
                return signUpLineRes.data;
            } catch (error) {
                console.log('error in signUpLine', error);
            }
        },
    },
    mutations:{
        order:(state, val)=>{
            state.order = val;
        },
        logout:(state)=>{
            state.login = false;
            localStorage.removeItem('login');
            localStorage.removeItem('id');
        },
        setCurrLang:(state, lang)=>{
            state.currLang = lang;
            setLocalStorage('currLang', lang)
        },
        getUserData: async (state, id)=>{
            let userRes = await api.get(`/user/${id}`);
            state.currUser = userRes.data;
            state.currLang = userRes.data.native_lang;

            setLocalStorage('id', id)
            setLocalStorage('currLang', state.currLang)
        },
        setCurrUserData:(state, data)=>{
            console.log('@store setCurrUserData', data);
            state.currUser = data;
        },
        signUp: async (state, data)=>{
            let signUpRes = await api.post(`/user`, data);
            console.log('@store signUpRes',signUpRes);
        },
        signUpLine: async (state, data)=>{
            state.currUser = data;
            console.log('@mutations signUpLine data',data);
        },
        setCurrOrder:(state, data)=>{
            state.currOrder = data;
        },
        setLineProfile:(state, data)=>{
            state.lineProfile = data;
        },
        setPrevRoute:(state, data)=>{
            state.prevRoute = data;
            // console.log('setPrevRoute state.prevRoute',state.prevRoute);
        },
        
    }
})

export default store;