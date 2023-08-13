<script setup>
import axios from 'axios';
// import _ from 'lodash';
import { reactive, ref, computed, onMounted, watch } from 'vue';
import { useStore } from "vuex";
import { useRouter, useRoute } from "vue-router";
import api from '@/axios/api.js';
import moment from 'moment'

const store = useStore()
const route = useRoute()
const router = useRouter()

let currOrder = ref()

const urlLang = route.params.lang;
const orderId = ref(localStorage.getItem('order_id'));

const calculateTotal = ( orderList ) => {
  let res = 0;
  JSON.parse(orderList).map((item) => {
    res += item.qty * item.price;
  });
  return res;
};
onMounted(async () => {
  try {
    let orderDetailRes = await api.get(`/${urlLang}/order_detail/${orderId.value}`);
    
    currOrder.value = orderDetailRes.data.data;
  } catch (error) {
    console.error(error);
  }
});

</script>

<template>
  <div class="_orderConfirm">
    <a-typography-title class="_orderConfirm_h1">Order Confirmed</a-typography-title>
    <div class="_orderConfirm_card" v-if="currOrder">
      <div class="_orderConfirm_no">
        <div class="">
          Status
          <p class="_orderConfirm_list__info" :class="currOrder.state">{{ currOrder.state }}</p>
        </div>
        <span class="_orderConfirm_no__num">{{ currOrder.id }}</span>
      </div>
      <div class="_orderConfirm_list">
        shop
        <p class="_orderConfirm_list__info">{{ currOrder.shop_name }}</p>
      </div>
      
      <a-divider class="_orderConfirm_divider"></a-divider>

      <div class="_orderConfirm_list" v-for="item,idx in JSON.parse(currOrder.item_list)" :key="idx">
        <span>{{ item.qty }}</span>
        <span>{{ item.name }}</span>
        <span>{{ item.price }}</span>
      </div>

      <a-divider class="_orderConfirm_divider"></a-divider>

      <div class="_orderConfirm_list">
        Created at
        <p class="_orderConfirm_list__info">{{ moment(currOrder.created_at).format('YYYY/MM/DD HH:mm') }}</p>
      </div>

      <div class="_orderConfirm_list">
        payment
        <p class="_orderConfirm_list__info">{{ currOrder.payment }}</p>
      </div>

      <a-divider class="_orderConfirm_divider"></a-divider>
      <div class="_orderConfirm_total">
        <span>Total</span><span class="_orderConfirm_total__val">{{ calculateTotal(currOrder.item_list) }}</span>
      </div>
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
._orderConfirm_h1{
  font-size: 1.5rem;
  margin-bottom: 2rem;
  text-align: center;
}
._orderConfirm_total{
  display: flex;
  justify-content: space-between;
  font-size: 1.5rem;
}
._orderConfirm_total__val{
  font-weight: bold;
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
  display: flex;
  justify-content: space-between;
}
._orderConfirm_no__num{
  line-height: 1;
  font-size: 1.5rem;
  color: $color-primary;
  background-color: $color-secondary;
  padding: .5rem;
  width: 2.5rem;
  height: 2.5rem;
  font-weight: bold;
  border-radius: $border-radius;
  display: flex;
  justify-content: center;
  align-items: center;
}
._orderConfirm_list{
  margin-bottom: 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
._orderConfirm_list__info{
  font-weight: bold;
  font-size: 1rem;
  margin-top: .5rem;

  &.preparing{
    color: $color-secondary;
  }
}
</style>
