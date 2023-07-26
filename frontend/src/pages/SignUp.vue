<script setup>
import axios from 'axios';
import { reactive, ref, computed, onMounted } from 'vue';
import { useStore } from "vuex";
import { useRouter, useRoute } from "vue-router";
import api from '@/axios/api.js';

const router = useRouter()

const store = useStore();
const isLogin = computed(() => store.getters.login);

// const lang = route.params.lang;
const formState = reactive({
  mail: '',
  nLang: '',
  password: '',
  displayName: '',
  password: ''
});

const langOptions = ref(store.getters.langList)

const onFinish = values => {
  signIn( values );
  store.dispatch('login');
  router.push({ name: 'User' })
};
const onFinishFailed = errorInfo => {
  console.log('Failed:', errorInfo);
};

const signIn = async( state )=>{
  try {
    const res = await api.post('/user', state);
    console.log('signIn res.data.native_lang',res.data.native_lang);
    store.dispatch('setCurrLang', res.data.native_lang);
  } catch (error) {
    console.error(error);
  }
}

const goLogin = () => {
  router.push({ name: 'Login' })
};
</script>

<template>
  <a-typography-title style="text-align: center;">Sign up</a-typography-title>
  <a-form
    :model="formState"
    layout="vertical"
    name="basic"
    class="_signup_form"
    autocomplete="off"
    @finish="onFinish"
    @finishFailed="onFinishFailed"
  >
    <a-form-item
      v-if="isLogin"
      label="Display name"
      name="displayName"
    >
      <a-input v-model:value="formState.displayName" />
    </a-form-item>

    <a-form-item
      label="E-mail"
      name="mail"
      :rules="[{ required: true, message: 'Please input your e-mail!' }]"
    >
      <a-input v-model:value="formState.mail" />
    </a-form-item>


    <a-form-item
      label="Native Language"
      name="nLang"
      :rules="[{ required: true, message: 'Please input your native Language!' }]"
    >
      <a-select v-model:value="formState.nLang" placeholder="please select your native Language">
        <a-select-option value="en">English</a-select-option>
        <a-select-option value="jp">日本語</a-select-option>
        <a-select-option value="zh">中文</a-select-option>
      </a-select>
    </a-form-item>

    <a-form-item
      label="Password"
      name="password"
      :rules="[{ required: true, message: 'Please input your password!' }]"
    >
      <a-input-password v-model:value="formState.password" />
    </a-form-item>
    
    <a-form-item>
      <a-row :gutter="20">
        <a-col :span="12"><a-button type="link" block @click="goLogin"><i class="las la-arrow-left"></i>Back to log in</a-button></a-col>
        <a-col :span="12"><a-button type="primary" shape="round" block size="large" html-type="submit">Sign up</a-button></a-col>
      </a-row>
    </a-form-item>
  </a-form>
</template>

<style scoped lang="scss">
._signup_form{
  width: 90%;
  max-width: $form-max-widh;
  margin: auto;
}
._signup_btn{
  bottom {
    flex: 1 !important;
  }
}
</style>
