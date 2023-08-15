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
        <div class="_orderConfirm_state">
          Status
          <p class="_orderConfirm_state__val" :class="currOrder.state">{{ currOrder.state }}</p>
        </div>
        <span class="_orderConfirm_no__num">{{ currOrder.id }}</span>
      </div>
      <div class="_orderConfirm_list">
        shop
        <p class="_orderConfirm_list__info _orderConfirm_list__shopName">{{ currOrder.shop_name }}</p>
      </div>
      
      <a-divider class="_orderConfirm_divider"></a-divider>

      <div class="_orderConfirm_list" v-for="item,idx in JSON.parse(currOrder.item_list)" :key="idx">
        <div class="_orderConfirm_item">
          <span class="_orderConfirm_item__qty">{{ item.qty }}</span>
          <span class="_orderConfirm_item__name">{{ item.name }}</span>
          <span class="_orderConfirm_item__orice">{{ item.price }}</span>
        </div>
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

      <router-link :to="'/' + urlLang + '/user/order'">
        <a-button class="_orderConfirm_btn" type="primary" shape="round" block size="large">訂單列表</a-button>
      </router-link>

    </div>

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
  margin-bottom: .5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
._orderConfirm_list__shopName{
  font-size: 1.1rem;
}
._orderConfirm_state{

}
._orderConfirm_state__val{
  font-weight: bold;
  font-size: 1.25rem;
  margin-top: .25rem;

  &.waiting{
    color: $color-red;
  }
  &.cooking{
    color: $color-blue;
  }
  &.foodReady{
    color: $color-green;
  }
  &.cancel{
    color: $color-gray-2;
  }
  &.finish{
    background-color: $color-gray-1;
  }
}
._orderConfirm_list__info{
  font-weight: bold;
  // font-size: 1rem;

  &.preparing{
    color: $color-secondary;
  }
}
._orderConfirm_item{
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  font-size: 1.25rem;
  *{
    font-weight: bold;
  }
}
._orderConfirm_item__qty{
  color: $color-primary;
  flex: 1;
}
._orderConfirm_item__name{
  flex: 5;
}
._orderConfirm_item__price{
  flex: 1;
}
._orderConfirm_btn{
  max-width: $form-max-width;
  margin: auto;
  margin-top: 2rem;
}
</style>
