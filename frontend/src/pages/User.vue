<script setup>
import axios from 'axios';
import { reactive, ref, computed, onMounted, onBeforeMount, watch } from 'vue';
import { useStore } from "vuex";
import { useRouter, useRoute } from "vue-router";
import api from '@/axios/api.js';

const router = useRouter()
const store = useStore();

const isLogin = computed(() => store.getters.login);
const currUser = computed(() => store.getters.currUser);
const userData = ref();

const formState = reactive({
  mail: '',
  native_lang: '',
  password: '',
  display_name: ''
});

const langOptions = ref(store.getters.langList)

const onFinish = values => {
  signIn( values );
  store.dispatch('login');
};
const onFinishFailed = errorInfo => {
  console.log('Failed:', errorInfo);
};

onBeforeMount(async()=>{
  try{
    if(currUser != {}){
      let res = await api.get(`/user/${currUser.value.id}`);

      console.log('onBeforeMount CHECK CURRUSER');
      
      userData.value = res.data;
      // formState.value = userData.value;
      Object.assign(formState, res.data);
    } else {
      console.log('onBeforeMount currUser === {}');
      // router.push({ name: 'Login' })
    }
    
  } catch {

  }
  // console.log('@Page/User currUser', currUser.value);
  // userData.value = res.data
})
</script>

<template>
  <!-- currUser: {{ currUser }}
  isLogin: {{ isLogin }} -->
  <p>currUser: <span v-if="currUser">{{currUser}}</span></p>
  userData：{{ userData }}
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
      name="display_name"
    >
      <a-input v-model:value="formState.display_name" />
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
      name="native_lang"
      :rules="[{ required: true, message: 'Please input your native Language!' }]"
    >
    <a-select v-model:value="formState.native_lang" :options="langOptions"></a-select>

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
