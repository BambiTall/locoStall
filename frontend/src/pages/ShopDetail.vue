<script setup>
import axios from 'axios';
import { reactive, ref, computed, onMounted, onBeforeMount } from 'vue';
import { useStore } from "vuex";
import { useRouter, useRoute } from "vue-router";
import api from '@/axios/api.js';

const shopDetail = ref()
const isShow = ref(false)
const currCard = ref(0)

const route = useRoute()
const router = useRouter()
const store = useStore()

const lang = route.params.lang;
const id = route.params.id;

const getShopDetail = async(id)=>{
  try {
    const res = await api.get(`${lang}/shop/${id}`);
    shopDetail.value = res.data;
    shopDetail.value.menu.map((item) => {
      item.qty = 0
    })
  } catch (error) {
    console.error(error);
  }
}


onBeforeMount(async () => {
  try {
    await Promise.all([
      getShopDetail(id)
    ]);
  } catch (error) {
    console.error(error);
  }
});


const total = ref(0)
const valChange = () => {
  total.value = 0
  for(let i=0; i<shopDetail.value.menu.length; i++){
    total.value += Number(shopDetail.value.menu[i].qty) * shopDetail.value.menu[i].price;
  }
}

const showCard = (id) => {
  currCard.value = id;
  isShow.value = true;
}
const goPayment = () => {
  // 把訂單內容存進 store
  let orderData = {}
  let orderList = []

  shopDetail.value.menu.map((i)=>{
    if(i.qty > 0){
      orderList.push({
        name: i.name,
        prod_id: i.prod_id,
        qty: i.qty,
        price: i.price
      })
    }
  })
  
  orderData.shop_id = id;
  orderData.orderList = orderList;

  store.dispatch("order", orderData);

  router.push({ name: 'Payment', params: { lang: lang } })
}


</script>

<template>
  <div class="_shopDetail" v-if="shopDetail">

  <a-row :gutter="20">
    <a-col :sm="{ span: 24 }" :md="{ span: 6 }">
      <h1 class="_shopDetail_name">{{ shopDetail.name }}</h1>
      <a-rate class="_shopDetail_rate" v-model:value="shopDetail.rating" allow-half disabled />
      <p class="_shopDetail_des">{{ shopDetail.description }}</p>
    </a-col>

    <a-col :sm="{ span: 24 }" :md="{ span: 18 }">
      <ul class="_shopDetail_menu">
        <li class="_shopDetail_menu__item" v-for="item,index in shopDetail.menu" :key="index">
          <div class="_shopDetail_menu__left">
            <img class="_shopDetail_menu__img" v-if="!shopDetail.img" alt="" src="@/assets/default.jpg" />
            
            <!-- product intro card -->
            <a-button type="text" shape="circle" @click="showCard(index)" class="_shopDetail_menu__infoIcon">
              <i class="las la-info-circle"></i>
            </a-button>

            <div class="_shopDetail_prodIntro" :class="currCard == index && isShow ? 'show' : ''"  @click="isShow = false">
              <a-card hoverable class="_shopDetail_prodIntro__card">
                <template #cover>
                  <i class="las la-times _shopDetail_prodIntro__close"></i>
                  <img alt="example" src="@/assets/default.jpg" />
                </template>
                <a-card-meta :title="item.name">
                  <template #description>
                    <p>{{ item.description }}</p>
                  </template>
                </a-card-meta>
              </a-card>
            </div>

          </div>
          <div class="_shopDetail_menu__right">
            <p class="_shopDetail_menu__name">{{ item.name }}</p>
            <div class="_shopDetail_order">
              <div class="_shopDetail_order__price">
                <span class="_shopDetail_order__currency">NTD</span>
                <span class="_shopDetail_order__num">{{ item.price }}</span>
              </div>
              
              <div class="_shopDetail_count">
                <a-input-group compact>
                  <a-select class="_shopDetail_count__num" v-model:value="item.qty" @change="valChange()">
                    <a-select-option value="0">0</a-select-option>
                    <a-select-option v-for="n in 20" :value="n">{{ n }}</a-select-option>
                  </a-select>
                </a-input-group>
              </div>
            </div>
          </div>
        </li>
      </ul>
    
      <a-button class="_bigBtn" @click="goPayment" type="primary" block>
        <div class="_bigBtn_wrap">
          <div>Total<span class="_bigBtn_total">{{ total }}</span></div>
          Continue
        </div>
      </a-button>
    </a-col>
  </a-row>


  </div>
</template>

<style scoped lang="scss">
._bigBtn{
  position: fixed;
  left: 0;
  bottom: 0;
  height: 3.5rem;
  z-index: 5;
}
._bigBtn_wrap{
  display: flex;
  justify-content: space-between;
  align-items: center;
}
._bigBtn_total{
  font-size: 1.5rem;
  margin-left: .25rem;
  font-weight: bold;
}
._shopDetail_name{
  font-size: 2rem;
  font-weight: bold;
  margin-bottom: 1rem;
}
._shopDetail_menu{
  display: flex;
  flex-wrap: wrap;
  // gap: 1rem;
}
._shopDetail_menu__item{
  display: flex;
  border-bottom: 1px solid $color-gray-2;
  padding: .75rem 0;
  flex: 1;
  flex: 0 0 100%;
}
._shopDetail_menu__left{
  flex: 1;
  position: relative;
}
._shopDetail_menu__right{
  flex: 3;
  padding-left: 1rem;
  box-sizing: border-box;
}
._shopDetail_menu__img{
  width: 100%;
}
._shopDetail_menu__infoIcon{
  position: absolute;
  right: 0;
  bottom: 0;
  color: white;

  i {
    font-size: 1.5rem;
  }
}

._shopDetail_prodIntro{
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba($color: #000000, $alpha: .5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100;
  opacity: 0;
  pointer-events: none;
  transition: .2s all ease-in;

  &.show{
    opacity: 1;
    pointer-events: initial;
  }
}
._shopDetail_prodIntro__card{
  overflow: hidden;
  border-radius: 2rem;
  border: none;
  width: 90%;
  max-width: 350px;
}
._shopDetail_prodIntro__close{
  position: absolute;
  right: 1rem;
  top: 1rem;
  font-size: 2rem;
  display: inline;
  width: 2rem;
  color: white;
}
._shopDetail_menu__name{
  font-size: 1rem;
  font-weight: bold;
}
._shopDetail_order{
  display: flex;
  align-items: center;
}
._shopDetail_count{
  display: flex;
  margin-right: 1rem;

  input{
    color: $color-primary;
    font-weight: bold;
    max-width: 3rem;
    text-align: center;
    border: none;
    font-size: 1.5rem;
  }
}
._shopDetail_count__num{
    font-size: 1.2rem;
}
._shopDetail_order__currency{
  transform: translateY(-5px);
}
._shopDetail_order__price{
  display: flex;
  align-items: end;
  flex: auto;
}
._shopDetail_order__num{
  font-size: 1.5rem;
  font-weight: bold;
  margin-left: .5rem;
}

._shopDetail_rate{
  margin-bottom: 1.25rem;
}
._shopDetail_des{
  margin-bottom: 1.5rem;
  line-height: 1.5;
}

@media(min-width: $breakpoint-m){
  ._shopDetail_menu__item{
    flex: 0 0 50%;
  }
}
</style>
