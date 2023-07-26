import { createStore } from 'vuex'
import { ref,reactive } from "vue";

export const store = createStore({
    state () {
        return {
            currLang: 'zh',
            login: ref(false),
            order: [],
            langList:[
                {
                    value: 'disabled',
                    label: 'Please Select your native Language',
                },
                {
                    value: 'en',
                    label: 'English',
                },{
                    value: 'jp',
                    label: '日本語',
                },{
                    value: 'zh',
                    label: '中文',
                },
            ],
            currUser: {}
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
            console.log('@store setCurrUser data',data);
            
            state.currUser = data;
        },
    }
})