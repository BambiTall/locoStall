<script setup>
import Navigation from "../src/components/Navigation.vue";
import { useRouter, useRoute } from "vue-router";
import { reactive, ref, computed, onBeforeMount, onMounted, watch } from 'vue';
import { useStore } from "vuex";


const store = useStore();
const router = useRouter();
const lsLang = ref(localStorage.getItem('lang'));
const lsLogin = ref(Boolean(localStorage.getItem('login')));
const currLang = ref(store.getters.currLang);
const isLogin = ref(store.getters.login);

// check local storage
if (lsLang.value && lsLogin.value) {
  store.dispatch('setCurrLang', lsLang.value);
  store.dispatch('login');
} else {
  store.dispatch('setCurrLang', currLang.value);
}

const checkLocalStorage = async () => {
  console.log('checkLocalStorage currLang', currLang.value);
  try {
    if (lsLang.value && lsLogin.value) {
      // Local Storage 有 Login & Lang
      store.dispatch('setCurrLang', lsLang.value);
      store.dispatch('login');
    } else {
      store.dispatch('setCurrLang', currLang.value);
      console.log('設定預設語言 currLang.value:', currLang.value);
    }
  } catch (error) {
    console.error(error);
  }
};

router.beforeEach((to, from) => {
  if (to.fullPath === '/' || to.fullPath === '/undefined' ) {
    // first time visit
    router.push({ path: `/${currLang.value}` });
    console.log('跳轉去 state 的語系', currLang.value);
  }
});

const initApp = async () => {
  try {
    await checkLocalStorage();
  } catch (error) {
    console.error(error);
  }
};

onBeforeMount(() => {
});

onMounted(async () => {
  try {
    await Promise.all([initApp()]);
  } catch (error) {
    console.error(error);
  }
});
</script>

<template>
   <a-layout>
    <a-layout-header :style="{ position: 'fixed', zIndex: 1, width: '100%' }">      
      <Navigation />
    </a-layout-header>
    <a-layout-content :style="{ marginTop: '64px' }" class="_body">
      <router-view/>
    </a-layout-content>
    <a-layout-footer :style="{ textAlign: 'center' }">
      © locoStall 2023
    </a-layout-footer>
  </a-layout>
</template>

<style lang="scss">
@import "../src/assets/scss/style.scss";

._body{
  padding: 50px;
}
</style>
