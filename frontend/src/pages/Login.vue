<script setup>
import axios from 'axios';
import { reactive, ref, computed, onMounted, watch ,onBeforeMount } from 'vue';
import { useStore } from "vuex";
import { useRouter, useRoute } from "vue-router";
import api from '@/axios/api.js';

// i18n
import { useI18n } from "vue-i18n";
const { t, locale } = useI18n({ useScope: "global" });

const route = useRoute()
const router = useRouter()
const store = useStore();
const isLogin = computed(() => store.getters.login);
const prevRoute = ref(store.getters.prevRoute);

// const lang = route.params.lang;
let userInfo = ref({})

const formState = reactive({
  mail: '',
  password: '',
});

const onLogin = values => {
  logIn( values );
};
const onLoginFailed = errorInfo => {
  console.log('Login Failed:', errorInfo);
};

const logIn = async( state )=>{
  try {
    const res = await api.post('/user/login', state);

    // set user id
    localStorage.setItem('id', res.data.id);
    store.dispatch('login');

    let userRes = await api.get(`/user/${res.data.id}`);

    store.dispatch('setCurrUser', userRes.data);
    store.dispatch('setCurrLang', userRes.data.native_lang);
    
    prevRoute.value.params.lang = userRes.data.native_lang
    
    router.push( prevRoute.value )

  } catch (error) {
    console.error(error);
  }
}

const lineLogin = () => {
  router.push({ name: 'LiffLogin' })
};

const goSignUp = () => {
  router.push({ name: 'SignUp' })
};
</script>

<template>
  <a-typography-title style="text-align: center;">{{ t('login') }}</a-typography-title>
  <a-form
    layout="vertical"
    :model="formState"
    name="basic"
    class="_login_form"
    autocomplete="off"
    @finish="onLogin"
    @finishFailed="onLoginFailed"
  >
    <a-form-item
      :label="t('email')"
      name="mail"
      :rules="[{ required: true, message: 'Please input your e-mail!' }]"
    >
      <a-input v-model:value="formState.mail" />
    </a-form-item>

    <a-form-item
      :label="t('password')"
      name="password"
      :rules="[{ required: true, message: 'Please input your password!' }]"
    >
      <a-input-password v-model:value="formState.password" />
    </a-form-item>

    <a-form-item>
      <a-button type="primary" shape="round" block size="large" html-type="submit">{{ t('login') }}</a-button>
    </a-form-item>
  </a-form>

  <a-divider class="_login_divider">還沒有帳號？</a-divider>

  <div class="_login_signin">
    <a-row :gutter="20">
      <a-col :span="12"><a-button shape="round" block size="large" @click="goSignUp">{{ t('signup') }}</a-button></a-col>
      <a-col :span="12"><a-button shape="round" block size="large" @click="lineLogin" style="background-color: #00b900; color: white;">Line Log in</a-button></a-col>
    </a-row>
  </div>

</template>

<style scoped lang="scss">
._login_form{
  width: 90%;
  max-width: $form-max-width;
  margin: auto;
}
._login_signin{
  width: 90%;
  max-width: $form-max-width;
  margin: auto;

  button{
    margin-bottom: 1rem;
  }
}
._login_divider{
  margin: 5rem 0 !important;
}
.ant-divider-horizontal.ant-divider-with-text{
  color: $color-gray-1 !important;
}
</style>
