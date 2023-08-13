<script setup>
import axios from 'axios';
import { reactive, ref, computed, onMounted, onBeforeMount, watch, toRaw } from 'vue';
import { useStore } from "vuex";
import { useRouter, useRoute } from "vue-router";
import api from '@/axios/api.js';

// i18n
import { useI18n } from "vue-i18n";
const { t, locale } = useI18n({ useScope: "global" });

const router = useRouter()
const store = useStore();

const currUserId = ref(localStorage.getItem('id'));
const currUser = computed(() => store.getters.currUser);

const formState = reactive({
  display_name: '',
  mail: '',
  native_lang: '',
  password: '',
  line_id: '',
  type: '',
  shop_id: ''
});

const langOptions  = computed(() => store.getters.langList)


const updateUserData = async () => {
  const plainObject = toRaw(formState);
  try {
    let updateUserDataRes = await api.post(`/user/${currUserId.value}`, plainObject);
    // console.log('Update user data successful:', updateUserDataRes);
  } catch (error) {
    console.error('Error updating user data:', error);
  }
};


onMounted(async()=>{
  try{
    if( Object.keys(currUser.value).length == 0 ){
      // console.log('@User store 沒有 currUser 資料');
      // hasn't get user data yet
      let res = await api.get(`/user/${currUserId.value}`);
      Object.assign(formState, res.data);

      store.dispatch('setCurrUserData', res.data);
    } else {
      // console.log('@User 已有 currUser 資料，直接放進 form');
      // got user data
      Object.assign(formState, currUser.value);
    }
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
      autocomplete="off"
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
        label="Line Id"
        name="line_id"
      >
        <a-input v-model:value="formState.line_id" disabled/>
      </a-form-item>

      <a-form-item
        :label="t('password')"
        name="password"
        :rules="[{ required: true, message: 'Please input your password!' }]"
      >
        <a-input-password v-model:value="formState.password" />
      </a-form-item>

      <a-form-item
        label="Type"
        name="type"
      >
        <a-input v-model:value="formState.type" disabled />
      </a-form-item>

      <a-form-item
        label="Shop ID"
        name="shop_id"
        v-if="formState.type==='manager'"
      >
        <a-input v-model:value="formState.shop_id" />
      </a-form-item>

      <a-form-item>
        <a-button @click="updateUserData" class="_form_submit" type="primary" block shape="round" size="large" html-type="submit">{{ t('update') }}</a-button>
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
