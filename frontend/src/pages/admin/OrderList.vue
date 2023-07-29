<script setup>
import { reactive, ref, computed, onMounted } from 'vue';
import axios from 'axios';
import { useStore } from "vuex";
import { useRouter, useRoute } from "vue-router";
import api from '@/axios/api.js';

const orderList = ref([])
const route = useRoute()
const lang = route.params.lang;

// i18n
import { useI18n } from "vue-i18n";
const { t, locale } = useI18n({ useScope: "global" });

const getOrderList = async()=>{
  try {
    const res = await api.get(`/orders`);
    orderList.value = res.data;
    // console.log('getOrderList res',res.data);
    
  } catch (error) {
    console.error(error);
  }
}

onMounted(async () => {
  try {
    await Promise.all([
      getOrderList(),
    ]);
  } catch (error) {
    console.error(error);
  }
});
</script>

<template>
  <a-typography-title style="text-align: center;">Order List</a-typography-title>
  <ul class="_orders">
    <li class="_orders_item" v-for="order,index in orderList" :key="index">
      user_id: {{ order.user_id }} <br>
      shop_id: {{ order.shop_id }} <br>
      payment: {{ order.payment }} <br>
      order_list: {{ order.order_list }} <br>
      created_at: {{ order.created_at }} <br>
      updated_at: {{ order.updated_at }}
    </li>
  </ul>

</template>

<style scoped lang="scss">
._orders_item {
  border-bottom: 1px solid $color-gray-3;
  padding: 2rem;
}
</style>
