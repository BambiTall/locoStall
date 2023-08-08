import { createStore } from 'vuex'
import { ref,reactive } from "vue";
import i18n from '@/lib/i18n/lang'
import api from '@/axios/api.js';

const store = createStore({
    state () {
        return {
            currLang: i18n.global.locale,
            login: ref(false),
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
        login:state=>{
            return state.login
        },
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
        checkLogin:({commit})=>{
            commit("checkLogin")
        },
        login:({commit})=>{
            commit("login")
        },
        logout:({commit})=>{
            commit("logout")
        },
        setCurrLang:({commit}, lang)=>{
            commit("setCurrLang", lang)
        },
        setCurrUserData:({commit}, data)=>{
            commit("setCurrUserData", data)
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
    },
    mutations:{
        order:(state, val)=>{
            state.order = val;
        },
        checkLogin:(state)=>{
            if(localStorage.getItem('login')){
                state.login = localStorage.getItem('login');
            }
        },
        login:(state)=>{
            state.login = true;
            localStorage.setItem('login', true);
        },
        logout:(state)=>{
            state.login = false;
            localStorage.removeItem('login');
            localStorage.removeItem('id');
        },
        setCurrLang:(state, lang)=>{
            state.currLang = lang;
            localStorage.setItem('currLang', lang);
        },
        getUserData: async (state, id)=>{
            let userRes = await api.get(`/user/${id}`);
            state.currUser = userRes.data;
            state.currLang = userRes.data.native_lang;

            localStorage.setItem('id', id);
            localStorage.setItem('currLang', state.currLang);
        },
        setCurrUserData:(state, data)=>{
            // console.log('store setCurrUserData', data);
            state.currUser = data;
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