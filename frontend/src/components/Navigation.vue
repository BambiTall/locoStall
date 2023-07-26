<script setup>
import { reactive, ref, computed, onMounted, watch } from 'vue';
import { useStore } from 'vuex';
import { useRouter, useRoute } from "vue-router";
import Logo from "../assets/locoStall_logo.vue";

// i18n
import { useI18n } from "vue-i18n";
const i18n = useI18n();
const { t, locale, availableLocales } = useI18n({ useScope: "global" });
const localeTrans={
  "locale": {
    "en": "English",
    "jp": "日本語",
    "tw": "中文",
  }
}
for(var k in availableLocales){
  i18n.mergeLocaleMessage(availableLocales[k], localeTrans);  
}
// const switchLang = () => {
//   router.push({ name: 'Login' })
// }

// vuex
const store = useStore();
const router = useRouter()

const isLogin = computed(() => store.getters.login);
const currLang = computed(() => store.getters.currLang);
// const currLang = ref(store.getters.currLang);
// const isLogin = ref(store.getters.login);
// console.log('currLang',currLang.value);

// let lsLang = localStorage.getItem('currLang');


const login = () => {
  router.push({ name: 'Login' })
}
const logout = () => {
  store.dispatch('logout');
}
// watch(currLang, (oldValue,newValue) => {
//   console.log('watch(currLang',oldValue,newValue);
  
//   localStorage.setItem('lang', newValue);
// });

</script>

<template>
  <ul class="_nav">
    <router-link to="/" class="_nav_logo"><Logo class="_nav_logo__svg"/></router-link>
    <li>
      <a-space>
        <a-select v-model:value="locale">
          <a-select-option v-for="lang in $i18n.availableLocales" :key="`locale-${lang}`" :value="lang">
            {{ t('locale.'+lang) }}
          </a-select-option>
        </a-select>
        <a-button v-if="!isLogin" class="_login__submit" type="primary" shape="round" size="large" @click="login">{{ t('login') }}</a-button>
        <a-button v-else class="_login__submit" type="primary" shape="round" size="large" @click="logout">{{ t('logout') }}</a-button>
      </a-space>
    </li>
  </ul>
</template>

<style scoped lang="scss">
._nav{
  // padding: 1rem;
  display: flex;
  justify-content: space-between;
}
._nav_logo{
  max-width: 180px;
  display: flex;
}
._nav_logo__svg{
  width: 100%;
}
</style>
