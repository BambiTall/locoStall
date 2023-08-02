<script setup>
import Navigation from "../src/components/Navigation.vue";
import { useRouter, useRoute } from "vue-router";
import { reactive, ref, computed, onBeforeMount, onMounted, watch } from 'vue';
import { useStore } from "vuex";


const store = useStore();
const router = useRouter();

// local storage
const localstorage_lang = ref(localStorage.getItem('lang'));
const localstorage_login = ref(Boolean(localStorage.getItem('login')));

// getters
const currLang = ref(store.getters.currLang);

// const checkLocalStorage = async () => {
//   try {
//     let useLang = ''

//     if (localstorage_login.value) {
//       // logged in
//       if (localstorage_lang.value) {
//         // lang set

//         useLang = localstorage_lang.value
//       } else {
//         console.log("logged in but lang hasn't been set");
//       }
//     } else {
//       // not logged in
//       // use default lang
//       useLang = currLang.value
//     }
//     store.dispatch('setCurrLang', useLang);
//   } catch (error) {
//     console.error(error);
//   }
// };

router.beforeEach((to, from, next) => {
  if (to.fullPath === '/' || to.fullPath === '/undefined' ) {
    // visit with no lang
    next({ path: `/${currLang.value}` });
  } else {
    // visit with lang
    store.dispatch('setCurrLang', to.params.lang);
    next();
  }
});

onBeforeMount(() => {
});

import liff from "@line/liff";

onMounted(async () => {
  try {
    await liff.init({ liffId: "2000144386-Ax8WZ8k2" });
    // if (!liff.isLoggedIn()){
    //   liff.login();
    // }
    console.log('Liff ready!');
  } catch (err) {
    console.log(`liff.state init error ${err}`);
  }
})

// custom theme
const theme = {
  token: {
    colorPrimary: '#6d9eed',
    // colorBgLayout: '#ffffff',
    borderRadius: 30
  },
};
</script>

<template>
  <a-config-provider :theme="theme">
   <a-layout>
      <a-layout-header class="_header">      
        <Navigation />
      </a-layout-header>
      <a-layout-content class="_body">
        <router-view/>
      </a-layout-content>
      <a-layout-footer class="_footer">
        © locoStall 2023
      </a-layout-footer>
    </a-layout>
  </a-config-provider>
</template>

<style lang="scss">
@import "../src/assets/scss/style.scss";

._header{
  position: fixed;
  display: flex;
  justify-content: space-between;
  z-index: 2;
  width: 100%;
  background-color: white !important;
  padding: 0 $padding-s !important;

}
._body{
  padding: 5rem $padding-s 0 !important;
}

._footer{
  text-align: center;
}

@media(min-width: $breakpoint-s){
  ._header{
    padding: 0 $padding-m !important;
  }

  ._body{
    padding-top: 6rem !important;
  }
}
</style>
