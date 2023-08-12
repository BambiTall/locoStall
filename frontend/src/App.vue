<script setup>
import Navigation from "../src/components/Navigation.vue";
import { useRouter, useRoute } from "vue-router";
import { reactive, ref, computed, onBeforeMount, onMounted, watch } from 'vue';
import { useStore } from "vuex";
import i18n from '@/lib/i18n/lang'
import api from '@/axios/api.js';

const store = useStore();
const router = useRouter();

// local storage
const loggedInId = ref(localStorage.getItem('id'));
let isLoggedIn = loggedInId.value != null ? true : false;

const lang = ref(localStorage.getItem('currLang'));
console.log('@App lang', lang.value);


let accessToken = ref()
let isBrowserCheck = ref()
let message = ref()
let adminSendMsgRes = ref()
let profile = ref()

// getters
const currUser = ref(store.getters.currUser);

router.beforeEach((to, from, next) => {
  // save prevRoute
  // if( to.name == 'Login' ){
  //   let routeObj = {}
  //   routeObj.name = from.name
  //   routeObj.params = from.params
  //   store.dispatch('setPrevRoute', routeObj);
  // }

  // handle 跳轉
  if (!to.params.lang || to.params.lang !== i18n.global.locale.value) {
    // visit with no lang
    next({ 
      path: `/${i18n.global.locale.value}`,
      query: to.query
    });
  }
   else if (to.meta.requiresAuth) {
    // console.log('需要 AUTH');
    if( !isLoggedIn ){
      // console.log('還沒登入');
      next({
        path: lang.value + '/login',
        query: { redirect: to.fullPath },
      });
    } else {
      // console.log('已登入');
      next();
    }
  } 
  else {
    // console.log('不需 AUTH');
    // visit with lang
    store.dispatch('setCurrLang', to.params.lang);
    next();
  }
});

onBeforeMount(async () => {
  try{    
    if( loggedInId.value != null && Object.keys(currUser.value).length == 0){
      const getUserDataRes = await store.dispatch('getUserData', Number(loggedInId.value));
    }
  } catch {

  }
});

import liff from "@line/liff";

const sendAdmintoUserMessege = async()=> {
  adminSendMsgRes.value = await api.post('/backend/token', {
    accessToken: accessToken.value,
  });
  // alert('adminSendMsgRes', adminSendMsgRes);
}

onMounted(async () => {
  try {
    await liff.init({ liffId: "2000144386-Ax8WZ8k2" });

    accessToken.value = liff.getAccessToken();
    if (accessToken.value == null) {
      isBrowserCheck.value = false;
      message.value = "LINEアプリから実行してください";
      return false;
    }
    isBrowserCheck.value = true;
    message.value = "ログイン成功";
    
    // 註冊
    const liffProfile = liff.getProfile()
    profile.value = liffProfile
    let params = {
      line_id: liffProfile.userId,
    }
    store.dispatch('signUpLine', params);

  } catch (err) {
    console.log(`liff.state init error ${err}`);
  }
})

// custom theme
const theme = {
  token: {
    colorPrimary: '#ffc648',
    colorBgLayout: '#ffffff',
    borderRadius: 30
  },
};
</script>

<template>
  <a-config-provider :theme="theme">
   <a-layout class="_layout">
      <a-layout-header class="_header">      
        <Navigation />
        <a-button @click="sendAdmintoUserMessege" type="primary" size="circle">
          Admin Send
        </a-button>
        <p>message: {{ message }}</p>
        <p>accessToken: {{ accessToken }}</p>
        <p>adminSendMsgRes: {{ adminSendMsgRes }}</p>
        <p>profile: {{ profile }}</p>
        
      </a-layout-header>
      <a-layout-content class="_body">
        <router-view/>

        <a-layout-footer class="_footer">
          © locoStall 2023
        </a-layout-footer>
      </a-layout-content>
    </a-layout>
  </a-config-provider>
</template>

<style lang="scss">
@import "../src/assets/scss/style.scss";
// ._layout{
//   height: 100%;
// }
._header{
  position: fixed;
  display: flex;
  justify-content: space-between;
  z-index: 2;
  width: 100%;
  // background-color: $color-secondary !important;
  background-color: white !important;
  padding: 0 !important;

}
._body{
  padding: 6rem $padding-s 0 !important;
  min-height: 100vh !important;
}

._footer{
  text-align: center;
}

@media(min-width: $breakpoint-s){
  // ._header{
  //   padding: 0 $padding-m !important;
  // }

  ._body{
    padding-top: 6rem !important;
  }
}
</style>
