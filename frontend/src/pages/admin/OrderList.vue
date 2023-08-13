<script setup>
import { reactive, ref, computed, onMounted, watchEffect, onUnmounted } from 'vue';
import axios from 'axios';
import { useStore } from "vuex";
import { useRouter, useRoute } from "vue-router";
import api from '@/axios/api.js';
import moment from 'moment'

const orderList = ref([])
const userData = ref({})
const route = useRoute()
const store = useStore()

// i18n
import { useI18n } from "vue-i18n";
const { t, locale } = useI18n({ useScope: "global" });

const currUser = computed(() => store.getters.currUser);
const loggedInId = ref(Number(localStorage.getItem('id')));

const getOrderList = async()=>{
  try {
    const res = await api.get(`/orders/manager/${userData.value.id}`);
    orderList.value = res.data;
    // console.log('@getOrderList orderList.value',orderList.value);
  } catch (error) {
    console.error(error);
  }
}

const getUserData = async()=>{
  try {
    const res = await api.get(`/user/${loggedInId.value}`);
    userData.value = res.data;
    await getOrderList();

  } catch (error) {
    console.error(error);
  }
}

const orderStateHandler = async( id, newState )=>{
  try {
    let params = {
      order_id: id,
      state: newState
    }
    const orderStateRes = await api.post(`/update_order`, params);
  } catch (error) {
    console.error(error);
  }
}

// setInterval
let interval = null;
const runInterval = () => {
  interval = setInterval(
    function () {
      getOrderList()
    }.bind(this),
    3000
  );
}

const calculateTotal = ( orderList ) => {
  let res = 0;
  JSON.parse(orderList).map((item) => {
    res += item.qty * item.price;
  });
  return res;
};

onMounted(async () => {
  try {
    await Promise.all([
      getUserData(),
    ]);

    runInterval();

  } catch (error) {
    console.error(error);
  }
});

onUnmounted(() => {
  clearInterval(interval);
});
</script>

<template>
  <!-- <a-typography-title class="_h1">{{ t('orderList') }}</a-typography-title> -->

  <div v-if="orderList.length==0" class="_orders_nodata">
    {{ t('noData') }}
  </div>
  <a-row :gutter="[20, 20]" class="_orders">
    <a-col :xs="24" :sm="8" :md="8" :lg="6" v-for="order,idx in orderList" :key="idx">
      <a-card class="_order" :class="order.state">
        <div class="_order_top">
          <div class="_order_id">
            <!-- {{ t('orderId') }}  -->
            <div class="_order_created">
              {{ t('createdAt') }} <div class="_order_created__val">{{ moment(order.created_at).format('YYYY/MM/DD HH:mm') }}</div>
            </div>
            <span class="_order_id__num">{{ order.id }}</span>
          </div>

          <a-divider class="_order_hr"></a-divider>

          <!-- product list -->
          <div class="_order_items" v-for="item,idx in JSON.parse(order.item_list)" :key="idx">
            <div class="_order_item">
              <span class="_order_item__qty">{{ item.qty }}</span>
              <span class="_order_item__name">{{ item.name }}</span>
              <span class="_order_item__subtotal">{{ item.qty * item.price }}</span>
            </div>
          </div>
          
          <a-divider class="_order_hr"></a-divider>
          <div class="_order_total">
            <span>{{ t('total') }}</span><span class="_order_total__val">{{ calculateTotal(order.item_list) }}</span>
          </div>

          <a-divider class="_order_hr"></a-divider>

          <!-- <div class="_order_state">
            {{ t('orderState') }}<span class="_order_state__num">{{ t(order.state) }}</span>
          </div> -->
          <div class="_order_payment">
            {{ t('payment') }}<span class="_order_payment__val">{{ t(order.payment) }}</span>
          </div>
          <div class="_order_customer">
            {{ t('customer') }}<span class="_order_customer__val">{{ order.user_id }}{{ order.user_name }}</span>
          </div>

          <!-- <a-divider class="_order_hr"></a-divider> -->

          <!-- <div class="_order_created">
            {{ t('createdAt') }}<div class="_order_created__val">{{ moment(order.created_at).format('YYYY/MM/DD HH:mm') }}</div>
          </div> -->
        </div>

        <a-select
          class="_order_bottom" :class="order.state"
          ref="select"
          v-model:value="order.state"
          @change="orderStateHandler(order.id, order.state)"
        >
          <a-select-option value="waiting">{{ t('waiting') }}</a-select-option>
          <a-select-option value="cooking">{{ t('cooking') }}</a-select-option>
          <a-select-option value="foodReady">{{ t('foodReady') }}</a-select-option>
          <a-select-option value="finish">{{ t('finish') }}</a-select-option>
          <a-select-option value="cancel">{{ t('cancel') }}</a-select-option>
        </a-select>

      </a-card>
    </a-col>
  </a-row>
</template>

<style scoped lang="scss">
._order{
  overflow: hidden;
  box-shadow: 0 0.5rem 1rem #00000026;
  transition: .2s all ease-in;

  &.finish, &.cancel{
    opacity: .45;

    &:hover{
      opacity: 1;
    }
    // background-color: $color-gray-4;

    // *{
    //   color: $color-gray-1;
    // }
  }
}
._orders_nodata{
  text-align: center;
}
._order_top{
  padding: calc($padding-m/2);
}
._order_hr{
  margin: .75rem 0;
}
._order_item{
  display: flex;
  align-items: center;
  margin-bottom: .5rem;
  * {
    font-weight: bold;
  }
}
._order_item__qty{
  color: $color-primary;
  font-size: 1.25rem;
  flex: 1;
  line-height: 1;
  // margin-right: 1rem;
}
._order_item__name{
  font-size: 1.25rem;
  flex: 5;
  line-height: 1;
}
._order_item__subtotal{
  font-size: 1rem;
  flex: 1;
  text-align: right;
}
._order_total{
  display: flex;
  justify-content: space-between;
  align-items: center;
}
._order_total__val{
  font-weight: bold;
  font-size: 1.25rem;
}
._order_bottom{
  width: 100%;
  text-align: center;
  padding: .5rem;

  &.waiting{
    background-color: $color-red;
  }
  &.cooking{
    background-color: $color-blue;
  }
  &.foodReady{
    background-color: $color-green;
  }
  &.cancel{
    background-color: $color-gray-2;
  }
  &.finish{
    background-color: $color-gray-1;
  }
}
._order_id{
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
}
._order_id__num{
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
._order_state{
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
}
._order_state__num{
  font-weight: bold;
}
._order_payment{
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
}
._order_payment__val{
  font-weight: bold;
}
._order_created{
  // display: flex;
  // justify-content: space-between;
  // align-items: flex-end;
}
._order_created__val{
  font-weight: bold;
}
._order_customer{
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
}
._order_customer__val{
  font-weight: bold;
}
</style>
