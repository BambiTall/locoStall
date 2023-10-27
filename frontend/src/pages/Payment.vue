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
const isWaiting = ref(false);

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


const getOrderUpdate = async(order_id)=>{
  try {
    const getOrderUpdateRes = await api.get(`${lang}/order_detail/${order_id}`);
    
    if(getOrderUpdateRes.data.data.state === 'cooking' || getOrderUpdateRes.data.data.state === 'foodReady'){
      isWaiting.value = false;
      // 沒清成功？？
      clearInterval(interval);

      router.push({ name: 'OrderConfirm' })
    }  
  } catch (error) {
    console.error(error);
  }
}

// setInterval
let interval = null;
const runInterval = (order_id) => {
  interval = setInterval(
    function () {
      getOrderUpdate(order_id)
    }.bind(this),
    3000
  );
}

const sendOrderToDB = async( params )=>{
  try {
    
    const res = await api.post('/send_order', params);

    localStorage.setItem('order_id', res.data.data.id);
    store.dispatch('setCurrOrder', res.data.data);
    runInterval(res.data.data.id)
    if(res.data.data.payment=='linepay'){
      linepayAuth(res.data.data)
    } else {
      // Automatically change state for demo
      setTimeout(async() => {
        let params = {
          'order_id': res.data.data.id,
          'state': 'cooking',
        }
        const updateRes = await api.post('/update_order', params);
        setTimeout(async() => {
          isWaiting.value = false;
        }, 3000);
      }, 3000);
    }

  } catch (error) {
    console.log('@sendOrderToDB ERROR');
  }
}

const linepayAuth = async( params )=>{
  try {
    // str to json
    params.item_list = JSON.parse(params.item_list);
    // console.log(' params', params);
    const res = await api.post('/linepay', params);
    console.log('linepayAuth res.data',res.data);
    // alert(res.data);
    window.location.href = res.data.paymentUrl;
  } catch (error) {
    console.log('@linepayAuth ERROR');
  }
}

const sendOrder = () => {
  if(localStorage.getItem('id') === null){
    // 登入
    alert('請先登入');
    router.push({ name: 'Login' })
  } else {
    // 送出訂單
    orderData.value.orderList.map((i)=>{
      delete i.name
      delete i.price
    })

    const params = {
      item_list: orderData.value.orderList,
      // user_id: currUser.value.id,
      user_id: localStorage.getItem('id'),
      shop_id: orderData.value.shop_id,
      payment: payment.value,
    }

    isWaiting.value = true;
    sendOrderToDB(params)
    // if (params.payment=='cash') {
    //   isWaiting.value = true;
    //   sendOrderToDB(params)
    // } else if(params.payment=='linepay') {
    //   isWaiting.value = true;
    //   // linepayAuth(params)
    //   sendOrderToDB(params)
    // }
  }
}
const goShopDetail = () => {
  router.push({ name: 'ShopDetail', params: { lang: lang, id: orderData.value.shop_id } })
}

onBeforeMount(() => {
  if(!orderData.value.orderList){
  }
});
onMounted(async() => {
  // console.log('@ Payment Page');
  total.value = calculateTotal();
  // if(isWaiting.value) {
  //   // for linepay after redirection
  //   isWaiting.value = false;
  //   alert("line pay finished!")
  // }
});

</script>

<template>
  <a-typography-title class="_h2">{{ t('orderList') }}</a-typography-title>
  <div class="_payment">
    <div class="_payment_waiting" v-if="isWaiting">
      <div class="_payment_waiting__card">
        <div class="_payment_waiting__img">
          <img src="@/assets/locostall_ani.gif"/>
        </div>
        <div class="_payment_waiting__text">Waiting for confirmation ...</div>
      </div>
      
    </div>
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
        <a-radio value="linepay" class="_payment_card__linepay"><img class="" src="../assets/LINE_pay.png"/></a-radio>
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
._payment_waiting{
  position: fixed;
  top: 0;
  left: 0;
  z-index: 100;
  width: 100vw;
  height: 100vh;
  background-color: rgba($color: $color-secondary, $alpha: .9);
}
._payment_waiting__card{
  text-align: center;
  z-index: 101;
  position: relative;
  left: auto;
  top: 25%;
  background-color: white;
  width: 90%;
  height: 50%;
  padding: $padding-m;
  border-radius: $border-radius;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  margin: auto;
}
._payment_waiting__img{
  font-size: 5rem;
  
  img{
    width: 50%;
  }
}
._payment_waiting__text{
  font-size: 1.5rem;
  width: 80%;
  line-height: 1.5;
  color: $color-primary;
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
  border-radius: $border-radius;
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
._payment_card__linepay{
  span{
    display: inline-flex;
    align-items: center;
  }
  img{
    // display:block;
    // height: 100%;
    // width: 100%;
    // max-height: 1.25rem;
    // max-width: 100%;
  }
}

@media(min-width: $breakpoint-m){
  ._payment_waiting__card{
    width: 50%;
  }
}
</style>
