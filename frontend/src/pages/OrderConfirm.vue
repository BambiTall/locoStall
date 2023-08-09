<script setup>
import axios from 'axios';
// import _ from 'lodash';
import { reactive, ref, computed, onMounted, watch } from 'vue';
import { useStore } from "vuex";
import { useRouter, useRoute } from "vue-router";
import api from '@/axios/api.js';

const store = useStore()
const route = useRoute()
const router = useRouter()

// let currOrder = ref()
// let shopMenu = ref()

// const currUser = computed(() => store.getters.currUser);
const currOrder = computed(() => store.getters.currOrder);

const urlLang = route.params.lang;

const orderData = localStorage.getItem('order');
// const getOrderDetail = async( order_id )=>{
//   try {
//     const res = await api.get(`/order/${order_id}`);
//     console.log('getOrderDetail res',res);
    
//     // currOrder.value = res.data.data;
//     // item_list = currOrder.value.item_list
//     // getMenus( currOrder.value.shop_id )
//   } catch (error) {
//     console.log('@getOrderDetail ERROR', error);
//   }
// }
// const getMenus = async( id )=>{
//   try {
//     const res = await api.get(`${lang}/menu/${id}`);
//     shopMenu.value = res.data.data;
//   } catch (error) {
//     console.log('@getMenus ERROR', error);
//   }
// }

// onMounted(async () => {
//   try {
//     await Promise.all([
//       // getOrderDetail(10)
//     ]);
//   } catch (error) {
//     console.error(error);
//   }
// });


</script>

<template>
  <div class="_orderConfirm">
    currOrder: {{ currOrder }}
    orderData: {{ orderData }}
    <div class="_orderConfirm_card" v-if="currOrder">
      <a-typography-title class="_h1">Order Confirmed</a-typography-title>
      <div class="_orderConfirm_no">
        No.<span class="_orderConfirm_no__num">{{ currOrder.id }}</span>
      </div>

      <div class="_orderConfirm_list">
        Status
        <p class="_orderConfirm_list__info preparing">{{ currOrder.state }}</p>
      </div>
      <div class="_orderConfirm_list">
        Created at
        <p class="_orderConfirm_list__info">{{ currOrder.created_at }}</p>
      </div>

      <div class="_orderConfirm_list">
        payment
        <p class="_orderConfirm_list__info">{{ currOrder.payment }}</p>
      </div>
      <div class="_orderConfirm_list">
        shop
        <p class="_orderConfirm_list__info">{{ currOrder.shop_id }}</p>
      </div>

      <div  v-for="item,key in JSON.parse(currOrder.item_list)" :key="key">
        {{ item }}
      </div>

      <!-- <a-divider class="_orderConfirm_divider"></a-divider>
      <div class="_orderConfirm_total">
        <span>Total</span><span>{{ total }}</span>
      </div> -->
    </div>


    <router-link :to="'/' + urlLang + '/user/order'">
      <a-button type="primary" shape="round" block size="large">訂單列表</a-button>
    </router-link>
  </div>
</template>

<style scoped lang="scss">
._orderConfirm{
  * {
    // font-weight: bold;
  }
}
._orderConfirm_total{
  display: flex;
  justify-content: space-between;
  font-size: 1.5rem;
}
._orderConfirm_card{
  padding: 2rem;
  border-radius: 2rem;
  box-shadow: 0 0.5rem 1rem #00000026;
  margin-bottom: 2rem;
  width: $card-width;
  max-width: $form-max-width;
  margin: auto;
  margin-bottom: 3rem;
}
._orderConfirm_no{
  margin-bottom: 1rem;
}
._orderConfirm_no__num{
  font-size: 2rem;
  color: $color-primary;
  font-weight: bold;
}
._orderConfirm_list{
  margin-bottom: 1rem;
}
._orderConfirm_list__info{
  font-weight: bold;
  font-size: 1.25rem;

  &.preparing{
    color: $color-secondary;
  }
}
</style>
