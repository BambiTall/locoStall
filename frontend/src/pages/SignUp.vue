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

// const lang = route.params.lang;
const formState = reactive({
  mail: '',
  password: ''
});

const langOptions = computed(() => store.getters.langList)

const onFinish = values => {
  store.dispatch('signUp', values);
  router.push({ name: 'Login' })
};
const onFinishFailed = errorInfo => {
  console.log('Failed:', errorInfo);
};

const goLogin = () => {
  router.push({ name: 'Login' })
};
</script>

<template>
  <a-typography-title class="_h1">{{ t('signup') }}</a-typography-title>
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
      <a-button type="primary" shape="round" block size="large" html-type="submit">{{ t('submit') }}</a-button>
    </a-form-item>

    <a-form-item>
      <a-button class="_signup_back" type="link" block @click="goLogin"><i class="las la-arrow-left"></i>{{ t('prev') }}</a-button>
    </a-form-item>
  </a-form>
</template>

<style scoped lang="scss">
._signup_form{
  width: 90%;
  max-width: $form-max-width;
  margin: auto;
}
._signup_back{
  i {
    margin-right: 1rem;
  }
}
._signup_btn{
  bottom {
    flex: 1 !important;
  }
}
</style>
