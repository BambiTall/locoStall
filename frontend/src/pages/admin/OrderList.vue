<script setup>
import { reactive, ref, computed, onMounted } from 'vue';
import axios from 'axios';
import { useStore } from "vuex";
import { useRouter, useRoute } from "vue-router";
import api from '@/axios/api.js';

const orderList = ref([])
const route = useRoute()

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
          <div class="_order_prod" v-for="item,key in JSON.parse(order.order_list)" :key="key">
            {{ item }}
            <!-- <div class="_order_prod" v-for="i,key in JSON.parse(item)" :key="key">
              <span class="_order_prod__qty">{{ i.qty }}</span>
              <span class="_order_prod__name">{{ i.name }}</span>
            </div> -->
            <!-- <div class="_order_prod" v-for="i,key in item" :key="key">
              <span class="_order_prod__qty">{{ i[key] }}</span>
              <span class="_order_prod__name">{{ item.name }}</span>
            </div>  -->
            <!-- {{ typeof(item) }}
            {{ item.qty }} -->
          </div>

          <!-- <div>
            <span class="_order_prod__subtotal">{{ item.qty * item.price }}</span>
          </div> -->
          
          <a-divider></a-divider>
          <div class="_order_state">
            {{ t('orderState') }}<span class="_order_state__num">{{ t(order.state) }}</span>
          </div>
          <!-- <div class="_order_payment">
            {{ t('payment') }}<span class="_order_payment__val">{{ order.payment }}</span>
          </div> -->
          <div class="_order_customer">
            {{ t('customer') }}<span class="_order_customer__val">{{ order.user_id }}</span>
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

  <!-- <ul class="_orders">
    <li class="_orders_item" v-for="order,index in orderList" :key="index">
      user_id: {{ order.user_id }} <br>
      shop_id: {{ order.shop_id }} <br>
      payment: {{ order.payment }} <br>
      order_list: {{ order.order_list }} <br>
      created_at: {{ order.created_at }} <br>
      updated_at: {{ order.updated_at }}
    </li>
  </ul> -->

</template>

<style scoped lang="scss">
._order{
  overflow: hidden;
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
    background-color: $color-secondary;
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
  font-weight: bold;
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
