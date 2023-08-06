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

</script>

<template>
  <a-typography-title>Order History</a-typography-title>
</template>

<style scoped lang="scss">
</style>
