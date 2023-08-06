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
const isShowUserMenu = ref(false);

// getters
const isLogin = computed(() => store.getters.login);
const langOptions = ref(store.getters.langList)
const userData = ref(store.getters.currUser);

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
  isShowMenu.value = false;
  isShowUserMenu.value = false;
}
const logout = () => {
  store.dispatch('logout');
  isShowMenu.value = false;
  isShowUserMenu.value = false;
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
    <div class="_nav_right" :class="isShowMenu ? 'show' : ''">
      <div class="_nav_links" @click="isShowMenu = false">
        <router-link :to="'/' + urlLang + '/admin'" v-if="userData.type=='magager'">
          訂單列表
        </router-link>
        <router-link v-else :to="'/' + urlLang">
          {{ t('index.shop_list') }}
        </router-link>
      </div>
      <a-space class="_nav_right__setting">
        <div class="_nav_user">
          <a-button class="_nav_user__btn" @click="isShowUserMenu = !isShowUserMenu" type="primary" size="circle">
            <i class="lar la-user"></i>
          </a-button>
          <div class="_nav_manage" :class="isShowUserMenu ? 'show' : ''">
            <a-button type="text" @click="login" class="_nav_manage__link" v-if="!isLogin">
                {{ t('login') }}
            </a-button>

            <template v-else>
              <router-link class="_nav_manage__link" :to="'/' + urlLang+'/user/order'">
                {{ t('orderHistory') }}
              </router-link>
              <router-link class="_nav_manage__link" :to="'/' + urlLang+'/user/profile'">
                {{ t('profile') }}
              </router-link>
              <a-button type="text" @click="logout">
                {{ t('logout') }}
              </a-button>
            </template>
          </div>
        </div>

        <a-select v-model:value="locale" class="_nav_right__lang" @change="handleLangChange(locale)">
          <a-select-option v-for="lang in $i18n.availableLocales" :key="`locale-${lang}`" :value="lang">
            {{ t('locale.'+lang) }}
          </a-select-option>
        </a-select>
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
._nav_user{
  display: flex;
  align-items: center;
  position: relative;
  // border: 1px 0 1px 0;
  // border-style: solid;
  border: 1px solid $color-gray-3;
  border-left: 0;
  border-right: 0;
}
._nav_user__btn{
  display: none;

  i {
    font-size: 1.25rem;
  }
}
._nav_manage{
  width: 8rem;
  background: white;
  text-align: center;
  border-radius: $border-radius;
  display: flex;
  flex-direction: column;
  padding: 1rem 0;
  transition: .2s all ease-in;


  &.show {
    opacity: 1;
    transform: translateX(0);
  }
}
._nav_manage__link{
  padding: .5rem;
  line-height: 1.5;
}
// hamburger
._nav_hamburger{
  position: absolute;
  right: 0;
  padding: 0 1rem;
  z-index: 51;
}
._nav_hamburger{
  i {
    font-size: 1.5rem;
  }
}
._nav_right{
  background: white;
  position: absolute;
  top: 0;
  right: 0;
  z-index: 50;
  opacity: 0;
  width: 80%;
  height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  transition: .2s all ease-in;
  transform: translateX(30px);
  pointer-events: none;

  &.show {
    display: flex;
    justify-content: center;
    pointer-events: initial;
    opacity: 1;
    box-shadow: 0 0.5rem 1rem #00000026;
    transform: translateX(0);
  }
}
._nav_right__setting{
  display: flex;
  flex-direction: column;
}
._nav_right__lang{
  text-align: center;
}

@media(min-width: $breakpoint-m){
  ._nav_hamburger{
    opacity: 0;
  }
  ._nav_right{
    position: relative;
    top: 0;
    opacity: 1;
    width: initial;
    height: initial;
    box-shadow: none !important;
    transform: translateX(0);
    flex-direction: row;
    pointer-events: initial;
  }
  ._nav_links{
    margin-right: 1rem;
  }

  ._nav_right__setting{
    flex-direction: row;
  }
  ._nav_user{
    border: none;
  }
  ._nav_user__btn{
    display: initial;
  }

  ._nav_manage{
    position: absolute;
    right: -2.5rem;
    top: 3rem;
    box-shadow: 0 0.5rem 1rem #00000026;

    opacity: 0;
    transform: translateY(-10px);

    * {
      pointer-events: none;
    }

    &.show{
      *{
        pointer-events: initial;
      }
    }
  }
}
</style>
