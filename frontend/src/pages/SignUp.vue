<script setup>
import axios from 'axios';
import { reactive, ref, computed, onMounted } from 'vue';
import { useStore } from "vuex";
import { useRouter, useRoute } from "vue-router";
import api from '@/axios/api.js';

// i18n
import { useI18n } from "vue-i18n";
const { t, locale } = useI18n({ useScope: "global" });

const router = useRouter()
const store = useStore();
const isLogin = computed(() => store.getters.login);

// const lang = route.params.lang;
const formState = reactive({
  display_name: '',
  mail: '',
  native_lang: '',
  line_id: '',
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
  <a-typography-title style="text-align: center;">{{ t('signup') }}</a-typography-title>
  <a-form
    :model="formState"
    layout="vertical"
    name="basic"
    class="_signup_form"
    autocomplete="off"
    @finish="onFinish"
    @finishFailed="onFinishFailed"
  >
    <!-- <a-form-item
      v-if="isLogin"
      label="Display name"
      name="display_name"
    >
      <a-input v-model:value="formState.display_name" />
    </a-form-item> -->

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
      <a-row :gutter="20">
        <a-col :span="12"><a-button type="link" block @click="goLogin"><i class="las la-arrow-left"></i>Back to log in</a-button></a-col>
        <a-col :span="12"><a-button type="primary" shape="round" block size="large" html-type="submit">{{ t('submit') }}</a-button></a-col>
      </a-row>
    </a-form-item>
  </a-form>
</template>

<style scoped lang="scss">
._signup_form{
  width: 90%;
  max-width: $form-max-width;
  margin: auto;
}
._signup_btn{
  bottom {
    flex: 1 !important;
  }
}
</style>
