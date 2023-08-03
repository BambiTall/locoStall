<script setup>
import { reactive, ref, computed, onBeforeMount, onMounted, watch } from 'vue';
import liff from "@line/liff";

const os = ref('')
const lang = ref('')
const profile = ref('')
const decodedIdToken = ref('')

onMounted(()=>{
  if (!liff.isLoggedIn()){
    liff.login();
  }

  os.value = liff.getOS()
  lang.value = liff.getLanguage()
  profile.value = liff.getProfile()
  decodedIdToken.value = liff.getDecodedIDToken()
})
</script>

<template>
  LIFF
  <p>os: {{ os }}</p>
  <p>lang: {{ lang }}</p>
  <p>profile: {{ profile }}</p>
  <p>decodedIdToken: {{ decodedIdToken }}</p>
</template>

<style scoped>
</style>
