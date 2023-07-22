<script setup>
import { onMounted } from 'vue';
import liff from "@line/liff";

onMounted(async () => {
  try {
    await liff.init({ liffId: "2000144386-Ax8WZ8k2" });
    console.log('LIFF OK');
  } catch (err) {
    console.log(`liff.state init error ${err}`);
  }
  // try {
  //   await liff.init({ liffId: "2000144386-Ax8WZ8k2" });
  //   if (!liff.isLoggedIn())
  //     liff.login({ redirectUri: window.location.href });
  // } catch (err) {
  //   console.log(`liff.state init error ${err}`);
  // }
})
</script>

<template>
  LIFF
</template>

<style scoped>
</style>
