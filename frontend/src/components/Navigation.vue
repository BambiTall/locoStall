<script setup>
import { reactive, ref, computed, onMounted, watch } from 'vue';
import { useStore } from 'vuex';
import { useRouter, useRoute } from "vue-router";
import { useI18n } from "vue-i18n";
import Logo from "../assets/locoStall_logo.vue";

const store = useStore();
const route = useRoute();
const router = useRouter();

// getters
const isLogin = computed(() => store.getters.login);
const langOptions = ref(store.getters.langList)

// local storage
let urlLang = ref(localStorage.getItem('currLang'));

// i18n
const i18n = useI18n();
const { t, locale, availableLocales } = useI18n({ useScope: "global" });

let localeOptions = {}

langOptions.value.map((item)=>{
  localeOptions[item.value] = item.label
})

const localeTrans={
  "locale": localeOptions
}

for(var k in availableLocales){
  i18n.mergeLocaleMessage(availableLocales[k], localeTrans);
}

const login = () => {
  router.push({ name: 'Login' })
}
const logout = () => {
  store.dispatch('logout');
}
const handleLangChange = (locale) => {
  urlLang.value = locale;
  router.push({ name: route.params.name, params: { lang: locale } }).then(() => {
    location.reload();
  });
}

</script>

<template>
  <ul class="_nav">
    <router-link :to="'/' + urlLang" class="_nav_logo"><Logo class="_nav_logo__svg"/></router-link>
    <li>
      <a-space>
        <a-select v-model:value="locale" @change="handleLangChange(locale)">
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
