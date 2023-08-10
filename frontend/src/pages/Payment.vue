<script setup>
import axios from 'axios';
import { reactive, ref, computed, onMounted, onBeforeMount, watch } from 'vue';
import { useStore } from "vuex";
import { useRouter, useRoute } from "vue-router";
import api from '@/axios/api.js';

// i18n
import { useI18n } from "vue-i18n";
const { t, locale } = useI18n({ useScope: "global" });

const store = useStore()
const route = useRoute()
const router = useRouter()

const total = ref(0);

const orderData = computed(() => store.getters.order);
const currUser = computed(() => store.getters.currUser);

const lang = route.params.lang;

const payment = ref('cash')
const calculateTotal = () => {
  let res = 0;
  orderData.value.orderList.map((item) => {
    res += item.qty * item.price;
  });
  return res;
};


const submitOrder = async( params )=>{
  try {
    const res = await api.post('/send_order', params);
    store.dispatch('setCurrOrder', res.data.data);
    router.push({ name: 'OrderConfirm' })
  } catch (error) {
    console.log('@submitOrder ERROR');
  }
}

const sendOrder = () => {
  // 送出訂單
  orderData.value.orderList.map((i)=>{
    delete i.name
    delete i.price
  })

  const params = {
    item_list: orderData.value.orderList,
    user_id: currUser.value.id,
    shop_id: orderData.value.shop_id,
    payment: payment.value,
  }

  submitOrder(params)
}

const goShopDetail = () => {
  router.push({ name: 'ShopDetail', params: { lang: lang, id: orderData.value.shop_id } })
}

onBeforeMount(() => {
  if(!orderData.value.orderList){
  }
});
onMounted(() => {
  total.value = calculateTotal();
});

</script>

<template>
  <a-typography-title class="_h2">{{ t('orderList') }}</a-typography-title>
  <div class="_payment">
    <div class="_payment_card">
      <div class="_payment_items" v-for="item,idx in orderData.orderList" :key="idx">
        <div class="_payment_item">
          <span class="_payment_item__qty">{{ item.qty }}</span>
          <span class="_payment_item__name">{{ item.name }}</span>
          <span class="_payment_item__subtotal">{{ item.qty * item.price }}</span>
        </div>
      </div>

      <a-divider class="_payment_divider"></a-divider>
      <div class="_payment_total">
        <span>{{ t('total') }}</span><span>{{ total }}</span>
      </div>
    </div>

    <div class="_payment_card">
      <div class="_payment_card__subtitle">
        {{ t('payment') }}
      </div>

      <a-radio-group class="_payment_card__radio" name="radioGroup" style="display: flex; justify-content: space-between;" v-model:value="payment">
        <a-radio value="linepay">{{ t('linePay') }}</a-radio>
        <a-radio value="cash">{{ t('cash') }}</a-radio>
      </a-radio-group>
    </div>

    <a-row :gutter="20">
      <a-col :span="12"><a-button @click="goShopDetail" shape="round" block size="large">{{ t('prev') }}</a-button></a-col>
      <a-col :span="12"><a-button @click="sendOrder" type="primary" shape="round" block size="large">{{ t('ok') }}</a-button></a-col>
    </a-row>
    
  </div>
</template>

<style scoped lang="scss">
._payment{
  max-width: $form-max-width;
  margin: auto;

  * {
    font-weight: bold;
  }
}
._payment_item{
  display: flex;
  align-items: center;
  margin-bottom: .5rem;
}
._payment_item__qty{
  color: $color-primary;
  font-size: 2rem;
  flex: 1;
  margin-right: 1rem;
}
._payment_item__name{
  font-size: 1.25rem;
  flex: 5;
  line-height: 1.3;
}
._payment_item__subtotal{
  font-size: 1.5rem;
  flex: 1;
  text-align: right;
}
._payment_total{
  display: flex;
  justify-content: space-between;
  font-size: 1.5rem;
}
._payment_card{
  padding: 2rem;
  border-radius: 2rem;
  box-shadow: 0 0.5rem 1rem #00000026;
  margin-bottom: 2rem;
  background-color: white;
}
._payment_card__subtitle{
  font-size: 1.25rem;
  margin-bottom: 1rem;
}
._payment_card__radio{
  label{
    font-size: 1.25rem;
  }
}
</style>
