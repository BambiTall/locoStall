<script setup>
import axios from 'axios';
import { reactive, ref, computed, onMounted } from 'vue';
import { useStore } from "vuex";
import { useRouter, useRoute } from "vue-router";
import api from '@/axios/api.js';

const store = useStore();

const lineSignUp = async(data)=> {
    let params = {
      line_id: data.line_id,
      display_name: data.display_name,
      photo: data.photo,
    }
    store.dispatch('signUpLine', params);
}

</script>

<template>
  <div @click="lineSignUp({
      line_id: 'shfaouhtfgdaigfho',
      display_name: 'My Name',
      photo: 'My Photo',
    })">
    line id 註冊
  </div>
</template>

<style scoped lang="scss">
</style>
