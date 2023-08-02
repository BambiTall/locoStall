<script setup>
import { reactive, ref, computed, onMounted, watch } from 'vue';
import { useStore } from 'vuex';
import { useRouter, useRoute } from "vue-router";
import { useI18n } from "vue-i18n";
import Logo from "../assets/locoStall_logo.vue";

const store = useStore();
const route = useRoute();
const router = useRouter();

const isShowMenu = ref(false);

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

const showMenu = () => {
  isShowMenu.value = !isShowMenu.value;
}

const handleLangChange = (locale) => {
  urlLang.value = locale;
  router.push({ name: route.params.name, params: { lang: locale } }).then(() => {
    location.reload();
  });
}

</script>

<template>
  <div class="_nav">
    <router-link :to="'/' + urlLang" class="_nav_logo"><Logo class="_nav_logo__svg"/></router-link>
    
    <div class="_nav_hamburger" @click="showMenu">
      <i class="las la-bars"></i>
    </div>
    <!-- <div class="_nav_center" >
      <router-link :to="'/' + urlLang + '/admin'" class="_nav_logo">
      order list
      </router-link>
    </div> -->
    <div class="_nav_right" :class="isShowMenu ? 'show' : ''">
      <a-space class="_nav_right__setting">
        <a-select v-model:value="locale" class="_nav_right__lang" @change="handleLangChange(locale)">
          <a-select-option v-for="lang in $i18n.availableLocales" :key="`locale-${lang}`" :value="lang">
            {{ t('locale.'+lang) }}
          </a-select-option>
        </a-select>
        <a-button v-if="!isLogin" class="" type="primary" shape="round" size="large" @click="login">{{ t('login') }}</a-button>
        <a-button v-else class="" type="primary" shape="round" size="large" @click="logout">{{ t('logout') }}</a-button>
      </a-space>
    </div>
  </div>
</template>

<style scoped lang="scss">
._nav{
  // padding: 1rem;
  width: 100%;
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

// hamburger
._nav_hamburger{
  position: absolute;
  right: 0;
  padding: 0 1rem;
  // background-color: red;
  // position: fixed;
  // width: 50%;
  // right: 0;
  // height: 100%;
  // z-index: 101;
}
._nav_hamburger{
  i {
    font-size: 1.5rem;
  }
}
._nav_right{
  background: white;
  position: absolute;
  top: 64px;
  right: 0;
  opacity: 0;
  width: 100%;
  pointer-events: none;
  &.show {
    display: flex;
    justify-content: center;
    pointer-events: initial;
    opacity: 1;
    box-shadow: 0 0.5rem 1rem #00000026;
  }
}
._nav_right__lang{
  text-align: center;
}

@media(min-width: $breakpoint-m){
  ._nav_hamburger{
    opacity: 0;
  }
  ._nav_right{
    top: 0;
    position: relative;
    opacity: 1;
    width: initial;
    pointer-events: initial;
    box-shadow: none !important;
  }
}
</style>
