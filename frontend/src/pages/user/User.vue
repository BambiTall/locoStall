<script setup>
import axios from 'axios';
import { reactive, ref, computed, onMounted, onBeforeMount, watch } from 'vue';
import { useStore } from "vuex";
import { useRouter, useRoute } from "vue-router";
import api from '@/axios/api.js';

// i18n
import { useI18n } from "vue-i18n";
const { t, locale } = useI18n({ useScope: "global" });

const router = useRouter()
const store = useStore();

const isLogin = computed(() => store.getters.login);
const currUserId = ref(localStorage.getItem('id'));
const userData = ref(store.getters.currUser);

const formState = reactive({
  mail: '',
  native_lang: '',
  password: '',
  display_name: ''
});

const langOptions = ref(store.getters.langList)

onBeforeMount(async()=>{
  try{
    let res = await api.get(`/user/${currUserId.value}`);
    Object.assign(formState, res.data);

    store.dispatch('setCurrUserData', res.data);
    store.dispatch('setCurrLang', res.data.native_lang);

  } catch {

  }
})
</script>

<template>
  <a-typography-title class="_h1">User page</a-typography-title>
  <div class="_form">
    <a-form
      :model="formState"
      name="basic"
      class="_user_form"
      :label-col="{ span: 8 }"
      :wrapper-col="{ span: 16 }"
      autocomplete="off"
      @finish="onFinish"
      @finishFailed="onFinishFailed"
    >
      <a-form-item
        :label="t('displayName')"
        name="display_name"
      >
        <a-input v-model:value="formState.display_name" />
      </a-form-item>

      <a-form-item
        :label="t('email')"
        name="mail"
        :rules="[{ required: true, message: 'Please input your e-mail!' }]"
      >
        <a-input v-model:value="formState.mail" />
      </a-form-item>

      <a-form-item
        :label="t('nativeLang')"
        name="native_lang"
        :rules="[{ required: true, message: 'Please input your native Language!' }]"
      >
      <a-select v-model:value="formState.native_lang" :options="langOptions"></a-select>

      </a-form-item>

      <a-form-item
        :label="t('password')"
        name="password"
        :rules="[{ required: true, message: 'Please input your password!' }]"
      >
        <a-input-password v-model:value="formState.password" />
      </a-form-item>

      <a-form-item>
        <a-button class="_form_submit" type="primary" block shape="round" size="large" html-type="submit">{{ t('update') }}</a-button>
      </a-form-item>
    </a-form>

  </div>
</template>

<style scoped lang="scss">
._form{
  width: 90%;
  max-width: $form-max-width;
  margin: auto;
}
._form_submit{

}
</style>
