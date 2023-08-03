import { createStore } from 'vuex'
import { ref,reactive } from "vue";
import i18n from '@/lib/i18n/lang'

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
            lineProfile: {}
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
        setCurrUser:({commit}, data)=>{
            commit("setCurrUser", data)
        },
        setCurrOrder:({commit}, data)=>{
            commit("setCurrOrder", data)
        },
        setLineProfile:({commit}, data)=>{
            commit("setLineProfile", data)
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
            localStorage.removeItem('currLang');
        },
        setCurrLang:(state, lang)=>{
            state.currLang = lang;
            localStorage.setItem('currLang', lang);
        },
        setCurrUser:(state, data)=>{
            // console.log('store setCurrUser', data);
            state.currUser = data;
        },
        setCurrOrder:(state, data)=>{
            state.currOrder = data;
        },
        setLineProfile:(state, data)=>{
            state.lineProfile = data;
        },
    }
})

export default store;