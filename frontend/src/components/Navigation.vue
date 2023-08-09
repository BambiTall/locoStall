<script setup>
import { reactive, ref, computed, onMounted, watch } from 'vue';
import { useStore } from 'vuex';
import { useRouter, useRoute } from "vue-router";
import { useI18n } from "vue-i18n";
import { message } from 'ant-design-vue';
import api from '@/axios/api.js';

const store = useStore();
const route = useRoute();
const router = useRouter();

const isShowMenu = ref(false);
const isShowUserMenu = ref(false);

// getters
const langOptions = ref(store.getters.langList)
const currUser = ref(store.getters.currUser);

// local storage
let urlLang = ref(localStorage.getItem('currLang'));
const loggedInId = ref(localStorage.getItem('id'));
let isLoggedIn = computed(()=>{
  return loggedInId.value ? true : false
})

watch(loggedInId, (newVal)=>{
  console.log('LOGIN ID newVal', newVal);
  let res = false
  if(newVal != null){
    isLoggedIn.value = true
  }
})

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

  // set store.currUser empty
  store.dispatch('setCurrUserData', {});

  logoutSuccess();

  if( route.meta.requiresAuth ){
    router.push({ name: 'Login' })
  }
  // reload page
  location.reload();
}
const logoutSuccess = () => {
  message.success(
    'Log out success',
    2,
  );
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
onMounted(async ()=>{
  if( Object.keys(currUser.value).length == 0 && loggedInId.value){
    
    // hasn't get user data yet
    let userDateRes = await store.dispatch('getUserData', loggedInId.value);
  }
})

</script>

<template>
  <div class="_nav">
    <router-link :to="'/' + urlLang" class="_nav_logo">
      <img class="_nav_logo__icon" src="../assets/locostall_logo_icon.svg"/>
      <img class="_nav_logo__text" src="../assets/locostall_logo_text.svg"/>
    </router-link>

    <div class="_nav_hamburger" @click="showMenu">
      <i class="las la-bars"></i>
    </div>
    <div class="_nav_right" :class="isShowMenu ? 'show' : ''">
      <div class="_nav_links" @click="isShowMenu = false">
        <router-link :to="'/' + urlLang + '/admin'" v-if="loggedInId=='6'">
          客戶訂單
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
            <div  @click="login" class="_nav_manage__link" v-if="!isLoggedIn">
              {{ t('login') }}
            </div>

            <template v-else>
              <router-link class="_nav_manage__link" :to="'/' + urlLang+'/user/order'" @click="isShowMenu=false">
                {{ t('orderHistory') }}
              </router-link>
              <router-link class="_nav_manage__link" :to="'/' + urlLang+'/user/profile'" @click="isShowMenu=false">
                {{ t('profile') }}
              </router-link>
              <a-button class="_nav_manage__link" type="text" @click="logout">
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
  margin: 0 $padding-s;
}
._nav_logo{
  max-width: 45px;
  display: flex;
  padding: .5rem 0;
}
._nav_logo__icon{
  margin-right: 1rem;
  width: 100%;
}
._nav_logo__text{
  display: none;
}
._nav_user{
  display: flex;
  align-items: center;
  position: relative;
  // border: 1px 0 1px 0;
  // border-style: solid;
  // border: 1px solid $color-gray-3;
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
._nav_links{
  a{
    font-size: 1rem;
    padding: 1rem;
    // color: white;
    color: $color-primary;

    &:hover{
      background-color: none !important;
    }
  }
}
._nav_manage__link{
  cursor: pointer;
  line-height: 2;
  // color: white;
  color: $color-primary;
  transition: .2s all ease-in;

  &:hover{
    color: $color-primary;
  }
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
    color: $color-primary;
  }
}
._nav_right{
  position: absolute;
  top: 0;
  right: 0;
  z-index: 50;
  opacity: 0;
  width: 90%;
  height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  transition: .2s all ease-in;
  transform: translateX(30px);
  pointer-events: none;
  background-color: $color-secondary;
  // border-top-left-radius: $border-radius;
  // border-bottom-left-radius: $border-radius;

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
  ._nav{
    margin: 0 $padding-m;
  }

  ._nav_logo{
    padding: 1rem 0;
    max-width: 180px;
  }
  ._nav_logo__text{
    display: initial;
    width: 100%;
  }
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

    background: none;
  }
  ._nav_links{
    margin-right: 1rem;

    a{
      color: $color-secondary;
      border-radius: $border-radius;
      transition: .2s all ease-in;

      &:hover{
        color: $color-primary;
        background-color: $color-secondary;
      }
    }
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
    background: white;
    padding: 1rem;

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

  ._nav_manage__link{
    color: $color-secondary;
  }
}
</style>
