<script setup>
import { reactive, ref, computed, onMounted, watchEffect } from 'vue';
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
    const res = await api.get(`/orders/shop/${userData.value.shop_id}`);
    orderList.value = res.data;
    console.log('@@@ getOrderList res',res.data);
    
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
onMounted(async () => {
  try {
    await Promise.all([
      getUserData(),
    ]);
  } catch (error) {
    console.error(error);
  }
});
</script>

<template>
  <a-typography-title class="_h1">{{ t('orderList') }}</a-typography-title>
  
  <a-row :gutter="[20, 20]" class="_orders">
    <a-col :xs="24" :sm="6" :md="6" :lg="6" v-for="order,idx in orderList" :key="idx">
      <a-card class="_order">
        <div class="_order_top">
          <div class="_order_id">
            {{ t('orderId') }} <span class="_order_id__num">{{ order.id }}</span>
          </div>
          <a-divider></a-divider>

          <!-- product list -->
          <div class="_order_prod" v-for="item,key in JSON.parse(order.item_list)" :key="key">
            {{ item }}
          </div>

          <!-- <div>
            <span class="_order_prod__subtotal">{{ item.qty * item.price }}</span>
          </div> -->
          
          <a-divider></a-divider>
          <div class="_order_state">
            {{ t('orderState') }}<span class="_order_state__num">{{ t(order.state) }}</span>
          </div>
          <div class="_order_payment">
            {{ t('payment') }}<span class="_order_payment__val">{{ order.payment }}</span>
          </div>
          <div class="_order_customer">
            {{ t('customer') }}<span class="_order_customer__val">{{ order.user_id }}</span>
          </div>

          <a-divider></a-divider>

          <div class="_order_created">
            {{ t('createdAt') }}<div class="_order_created__val">{{ moment(order.created_at).format('YYYY-MM-DD') }}</div>
          </div>
        </div>

        <!-- shop_id: {{ order.shop_id }} <br>
        created_at: {{ order.created_at }} <br>
        updated_at: {{ order.updated_at }} -->
        <a-select
          class="_order_bottom" :class="order.state"
          ref="select"
          v-model:value="order.state"
        >
          <a-select-option value="waiting">{{ t('waiting') }}</a-select-option>
          <a-select-option value="cooking">{{ t('cooking') }}</a-select-option>
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
}
._order_top{
  padding: calc($padding-m/2) $padding-m;
}
._order_bottom{
  width: 100%;
  text-align: center;
  padding: .5rem;

  &.waiting{
    background-color: $color-red;
  }
  &.cooking{
    background-color: $color-green;
  }
  &.cancel{
    background-color: $color-gray-1;
  }
  &.finish{
    background-color: $color-gray-2;
  }
}
._order_id{
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
}
._order_id__num{
  line-height: 1;
  font-size: 2rem;
  color: $color-primary;
  background-color: $color-secondary;
  padding: .5rem;
  width: 3rem;
  height: 3rem;
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
._order_prod{
  display: flex;
  align-items: center;

}
._order_prod__qty{
  color: $color-primary;
  font-size: 2rem;
  flex: 1;
}
._order_prod__name{
  font-size: 1rem;
  flex: 5;
}
</style>
