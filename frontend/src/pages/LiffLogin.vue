<script setup>
import { reactive, ref, computed, onBeforeMount, onMounted, watch } from 'vue';
import liff from "@line/liff";

const os = ref('')
const lang = ref('')
const isInClient = ref('')
const profile = ref('')
const decodedIdToken = ref('')

onMounted(()=>{
  if (!liff.isLoggedIn()){
    liff.login();
  }

  os.value = liff.getOS()
  lang.value = liff.getLanguage()
  isInClient.value = liff.isInClient()
  profile.value = liff.getProfile()
  decodedIdToken.value = liff.getDecodedIDToken()
})

const sendUsertoAdminMessege = () => {
  // メッセージ送信する
  liff.sendMessages([{
      type: "text",
      text: "ユーザーからメッセージ送信したしん！",
  }])
  .then(() => {
      console.log('Message sent');
  })
  .catch((error) => {
      console.log('Error sending message: ' + error);
  });
};

const sendAdmintoUserMessege = () => {
  console.log('sendAdmintoUserMessege');
  window.alert('sendAdmintoUserMessege');
};
</script>

<template>
  LIFF
  <a-button shape="round" block size="large" @click="sendUsertoAdminMessege">ユーザーから管理者へ</a-button>
  <a-button shape="round" block size="large" @click="sendAdmintoUserMessege">管理者からユーザーへ</a-button>
  <p>os: {{ os }}</p>
  <p>lang: {{ lang }}</p>
  <p>isInClient: {{ isInClient }}</p>
  <p>profile: {{ profile }}</p>
  <p>decodedIdToken: {{ decodedIdToken }}</p>
</template>

<style scoped>
</style>
