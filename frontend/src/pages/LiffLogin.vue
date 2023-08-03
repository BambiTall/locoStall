<script setup>
import { reactive, ref, computed, onBeforeMount, onMounted, watch } from 'vue';
import liff from "@line/liff";

const os = ref('')
const lang = ref('')
const idToken = ref('')
const decodedIdToken = ref('')

onMounted(()=>{
  if (!liff.isLoggedIn()){
    liff.login();
  }

  os.value = liff.getOS()
  lang.value = liff.getLanguage()
  idToken.value = liff.getIDToken()
  decodedIdToken.value = liff.getDecodedIDToken()
})
</script>

<template>
  LIFF
  <p>os: {{ os }}</p>
  <p>lang: {{ lang }}</p>
  <p>idToken: {{ idToken }}</p>
  <p>decodedIdToken: {{ decodedIdToken }}</p>
</template>

<style scoped>
</style>
