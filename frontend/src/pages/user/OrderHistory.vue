<script setup>
import axios from 'axios';
import { reactive, ref, computed, onMounted, onBeforeMount, watch } from 'vue';
import { useStore } from "vuex";
import { useRouter, useRoute } from "vue-router";
import api from '@/axios/api.js';
import moment from 'moment'

// i18n
import { useI18n } from "vue-i18n";
const { t, locale } = useI18n({ useScope: "global" });

const router = useRouter()
const store = useStore();

const loggedInId = ref(localStorage.getItem('id'));
const currUser = computed(() => store.getters.currUser);
const orderHistory = ref([]) 

const calculateTotal = ( orderList ) => {
  let res = 0;
  JSON.parse(orderList).map((item) => {
    res += item.qty * item.price;
  });
  return res;
};

onMounted(async()=>{
  try{
    if(orderHistory.value.length === 0){
      let res = await api.get(`orders/user/${loggedInId.value}`);
      orderHistory.value = res.data;
      // console.log('orderHistory.value',orderHistory.value);
    }
  } catch {
  }
})
</script>

<template>
  <a-typography-title class="_h1">{{ t('orderHistory') }}</a-typography-title>
  <!-- {{ currUser }} -->
  <div class="_history_wrap">
    <div v-if="orderHistory.length==0">
      {{ t('noData') }}
    </div>
    <div v-else class="_history_items" v-for="order,idx in orderHistory" :key="idx">
      <!-- {{ order }} -->

      <div class="_history_row">
        <div class="_history_id">
          <span class="_history_id__num">{{ order.id }}</span>
        </div>
        <div class="_history_state">
          {{ t('orderState') }}<span class="_history_state__val" :class="order.state">{{ t(order.state) }}</span>
        </div>
        <div class="_history_payment">
          {{ t('payment') }}<span class="_history_payment__val">{{ t(order.payment) }}</span>
        </div>
        <div class="_history_total">
          {{ t('total') }}<span class="_history_total__val">{{ calculateTotal(order.item_list) }}</span>
        </div>
      </div>

      <div class="_history_row">
        <div class="_history_created">
          {{ t('createdAt') }}<span class="_history_created__val">{{ moment(order.created_at).format('YYYY/MM/DD HH:mm') }}</span>
        </div>
      </div>

      <a-collapse>
        <a-collapse-panel key="1" :header="t('orderDetail')">
          <div class="_history_details">
            <div class="_history_detail" v-for="item,idx in JSON.parse(order.item_list)" :key="idx">
              <span class="_history_detail__qty">{{ item.qty }}</span>
              <span class="_history_detail__name">{{ item.name }}</span>
              <span class="_history_detail__subtotal">{{ item.qty * item.price }}</span>
            </div>
          </div>
        </a-collapse-panel>
      </a-collapse>
    </div>
  </div>
</template>

<style scoped lang="scss">
._history_wrap{
  max-width: $form-max-width;
  margin: auto;
}
._history_items{
  padding: 1rem;
  border-radius: 2rem;
  box-shadow: 0 0.5rem 1rem #00000026;
  margin-bottom: 2rem;
  background-color: white;
}
._history_row{
  display: flex;
  justify-content: space-between;
}
._history_id{
}
._history_id__num{
  line-height: 1;
  font-size: 1.25rem;
  color: $color-primary;
  background-color: $color-secondary;
  width: 2rem;
  height: 2rem;
  font-weight: bold;
  border-radius: $border-radius;
  display: flex;
  justify-content: center;
  align-items: center;
}
._history_state{
  display: flex;
  flex-direction: column;
  margin-bottom: .75rem;
}
._history_state__val{
  font-weight: bold;
  margin-top: .5rem;

  &.waiting{
    color: $color-red;
  }
  &.cooking{
    color: $color-green;
  }
  &.cancel{
    color: $color-gray-2;
  }
  &.finish{
    color: $color-gray-1;
  }
}

._history_payment{
  display: flex;
  flex-direction: column;
  margin-bottom: .75rem;
}
._history_payment__val{
  font-weight: bold;
  margin-top: .5rem;
}
._history_total{
  display: flex;
  flex-direction: column;
  margin-bottom: .75rem;
}
._history_total__val{
  font-weight: bold;
  margin-top: .5rem;
  text-align: right;
  font-size: 1rem;
}

._history_created{
  width: 100%;
  display: flex;
  justify-content: space-between;
  margin-bottom: .75rem;
}
._history_created__val{
  font-weight: bold;
  margin-left: .5rem;
}

._history_detail{
  display: flex;
}
._history_detail__qty{
  flex: 1;
}
._history_detail__name{
  flex: 4;
}
._history_detail__subtotal{
  flex: 1;
  text-align: right;
}
</style>
