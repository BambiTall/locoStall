<script setup>
import axios from 'axios';
import { reactive, ref, computed, onMounted } from 'vue';
import { useStore } from "vuex";
import { useRouter, useRoute } from "vue-router";
import api from '@/axios/api.js';

const router = useRouter()
const store = useStore();

const isLogin = computed(() => store.getters.login);
const currUser = computed(() => store.getters.currUser);

const formState = reactive({
  mail: '',
  nLang: 'disabled',
  password: '',
  displayName: '',
  password: ''
});

const langOptions = ref(store.getters.langList)

const onFinish = values => {
  signIn( values );
  store.dispatch('login');
};
const onFinishFailed = errorInfo => {
  console.log('Failed:', errorInfo);
};

onMounted(()=>{
  // console.log('@Page/User currUser', currUser.value);
})
</script>

<template>
  <!-- currUser: {{ currUser }}
  isLogin: {{ isLogin }} -->
  <a-typography-title>User page</a-typography-title>
  <a-form
    :model="formState"
    name="basic"
    :label-col="{ span: 8 }"
    :wrapper-col="{ span: 16 }"
    autocomplete="off"
    @finish="onFinish"
    @finishFailed="onFinishFailed"
  >
    <a-form-item
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
    <a-select v-model:value="formState.nLang" :options="langOptions"></a-select>

    </a-form-item>

    <a-form-item
      label="Password"
      name="password"
      :rules="[{ required: true, message: 'Please input your password!' }]"
    >
      <a-input-password v-model:value="formState.password" />
    </a-form-item>

    <a-form-item :wrapper-col="{ offset: 8, span: 16 }">
      <a-button type="primary" html-type="submit">Edit</a-button>
    </a-form-item>
  </a-form>

</template>

<style scoped lang="scss">
</style>
