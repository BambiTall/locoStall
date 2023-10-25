<script setup>
import axios from 'axios';
import { reactive, ref, computed, onMounted, watch } from 'vue';
import { useStore } from "vuex";
import { useRouter, useRoute } from "vue-router";
import api from '@/axios/api.js';
import moment from 'moment'
import liff from "@line/liff";

// i18n
import { useI18n } from "vue-i18n";
const { t, locale } = useI18n({ useScope: "global" });

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

// const generateOrderFlexMsg = (orderRes) => {

//   const itemArr = JSON.parse(orderRes.item_list)
//   let itemListCode = ``

//   for(var i = 0; i < itemArr.length; i++){
//     itemListCode += `{
//           "type": "box",
//           "layout": "baseline",
//           "spacing": "sm",
//           "contents": [
//             {
//               "type": "text",
//               "text": "${itemArr[i].qty}",
//               "weight": "bold",
//               "size": "lg",
//               "color": "#ffc648"
//             },
//             {
//               "type": "text",
//               "text": "${itemArr[i].name}",
//               "wrap": true,
//               "size": "md",
//               "color": "#666666",
//               "flex": 6,
//               "weight": "bold"
//             },
//             {
//               "type": "text",
//               "text": "${itemArr[i].price}",
//               "align": "end",
//               "weight": "bold",
//               "size": "md"
//             }
//           ]
//         },`
//   }

//   let res = `
//   {
//     "type": "flex",
//     "altText": "Flex Message",
//     "contents": {
//       "type": "bubble",
//       "header": {
//         "type": "box",
//         "layout": "horizontal",
//         "contents": [
//           {
//             "type": "text",
//             "text": "${ t('orderId') }",
//             "weight": "bold",
//             "color": "#3f3b34"
//           },
//           {
//             "type": "text",
//             "text": "${orderRes.id}",
//             "size": "xxl",
//             "align": "end",
//             "weight": "bold",
//             "color": "#ffc648",
//             "action": {
//               "type": "uri",
//               "label": "action",
//               "uri": "https://liff.line.me/2000144386-Ax8WZ8k2/jp/user/order"
//             }
//           }
//         ],
//         "alignItems": "center"
//       },
//       "hero": {
//         "type": "image",
//         "url": "https://raw.githubusercontent.com/BambiTall/locoStall/main/frontend/src/assets/img/tofu.jpg",
//         "size": "full",
//         "aspectRatio": "20:13",
//         "aspectMode": "cover",
//         "align": "center"
//       },
//       "body": {
//         "type": "box",
//         "layout": "vertical",
//         "spacing": "md",
//         "contents": [
//           {
//             "type": "text",
//             "text": "${orderRes.shop_name}",
//             "wrap": true,
//             "weight": "bold",
//             "gravity": "center",
//             "size": "xl"
//           },
//           {
//             "type": "box",
//             "layout": "vertical",
//             "margin": "lg",
//             "spacing": "sm",
//             "contents": [
//               ${itemListCode}
//               {
//                 "type": "separator",
//                 "margin": "xl"
//               },
//               {
//                 "type": "box",
//                 "layout": "baseline",
//                 "spacing": "sm",
//                 "contents": [
//                   {
//                     "type": "text",
//                     "text": "${ t('total') }",
//                     "wrap": true,
//                     "size": "lg",
//                     "color": "#666666"
//                   },
//                   {
//                     "type": "text",
//                     "text": "${calculateTotal(currOrder.value.item_list)}",
//                     "align": "end",
//                     "size": "xl",
//                     "weight": "bold"
//                   }
//                 ],
//                 "margin": "xl"
//               },
//               {
//                 "type": "separator",
//                 "margin": "xl"
//               },
//               {
//                 "type": "box",
//                 "layout": "baseline",
//                 "spacing": "sm",
//                 "contents": [
//                   {
//                     "type": "text",
//                     "text": "${ t('payment') }",
//                     "color": "#aaaaaa",
//                     "size": "sm"
//                   },
//                   {
//                     "type": "text",
//                     "text": "${ t(orderRes.payment) }",
//                     "wrap": true,
//                     "color": "#666666",
//                     "size": "sm",
//                     "align": "end",
//                     "flex": 3
//                   },
//                   {
//                     "type": "text",
//                     "wrap": true,
//                     "color": "#93c878",
//                     "size": "sm",
//                     "text": "支払済",
//                     "align": "end",
//                     "weight": "bold"
//                   }
//                 ],
//                 "margin": "xl"
//               },
//               {
//                 "type": "box",
//                 "layout": "baseline",
//                 "spacing": "sm",
//                 "contents": [
//                   {
//                     "type": "text",
//                     "text": "${ t('createdAt') }",
//                     "color": "#aaaaaa",
//                     "size": "sm"
//                   },
//                   {
//                     "type": "text",
//                     "text": "${moment(currOrder.value.created_at).format('YYYY/MM/DD HH:mm')}",
//                     "wrap": true,
//                     "color": "#666666",
//                     "size": "sm",
//                     "align": "end"
//                   }
//                 ],
//                 "margin": "sm"
//               }
//             ]
//           }
//         ]
//       }
//     }
//   }`

//   // order_detail results
//   /*
//     "created_at": "2023-08-07 23:53:43.167981",
// 		"id": 5,
// 		"item_list": "[{\"prod_id\": 2, \"qty\": 2, \"name\": \"Thick Meat Soup\", \"price\": 70}, {\"prod_id\": 3, \"qty\": 1, \"name\": \"Oil Rice\", \"price\": 40}]",
// 		"payment": "cash",
// 		"shop_id": 8,
// 		"shop_name": "\u6771\u767c\u865f",
// 		"state": "cancel",
// 		"updated_at": "2023-08-09 16:16:35.364413",
// 		"user_id": 1
//   */
//   return res;
// };


onMounted(async () => {
  try {
    let orderDetailRes = await api.get(`/${urlLang}/order_detail/${orderId.value}`);
    
    currOrder.value = orderDetailRes.data.data;

    // Ganerate Flex message
    // const orderFlexMsgRes = generateOrderFlexMsg(currOrder.value);
    let sendMessageArr = [];
    
    // state reminder
    let stateTextMsg = {
      'type': 'text',
      'text': `[ ${t('order')} ${currOrder.value.id} ] ${t('orderConfirmed')}`
    }
    sendMessageArr.push( stateTextMsg );
    // sendMessageArr.push( JSON.parse(orderFlexMsgRes) );

    liff.sendMessages(
      sendMessageArr
    ).then(() => {
    }).catch((err) => {
        console.error(err);
    });

    // console.log('sendMessageArr',sendMessageArr);
    
  } catch (error) {
    console.error(error);
  }
});

</script>

<template>
  <div class="_orderConfirm">
    <a-typography-title class="_orderConfirm_h1">{{ t('orderConfirmed') }}</a-typography-title>
    <div class="_orderConfirm_card" v-if="currOrder">
      <div class="_orderConfirm_no">
        <div class="_orderConfirm_state">
          {{ t('state') }}
          <p class="_orderConfirm_state__val" :class="currOrder.state">{{ t(currOrder.state) }}</p>
        </div>
        <span class="_orderConfirm_no__num">{{ currOrder.id }}</span>
      </div>
      <div class="_orderConfirm_list">
        {{ t('shopName') }}
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
        {{ t('createdAt') }}
        <p class="_orderConfirm_list__info">{{ moment(currOrder.created_at).format('YYYY/MM/DD HH:mm') }}</p>
      </div>

      <div class="_orderConfirm_list">
        {{ t('payment') }}
        <p class="_orderConfirm_list__info">{{ t(currOrder.payment) }}</p>
      </div>

      <a-divider class="_orderConfirm_divider"></a-divider>
      <div class="_orderConfirm_total">
        <span>{{ t('total') }}</span><span class="_orderConfirm_total__val">{{ calculateTotal(currOrder.item_list) }}</span>
      </div>

      <router-link :to="'/' + urlLang + '/user/order'">
        <a-button class="_orderConfirm_btn" type="primary" shape="round" block size="large">{{ t('orderList') }}</a-button>
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
    color: $color-gray-1;
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
