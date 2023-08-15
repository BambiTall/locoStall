<script setup>
import axios from 'axios';
import { reactive, ref, computed, onMounted, onBeforeMount, watch } from 'vue';
import { useStore } from "vuex";
import { useRouter, useRoute } from "vue-router";
import api from '@/axios/api.js';

// i18n
import { useI18n } from "vue-i18n";
const { t, locale } = useI18n({ useScope: "global" });

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
    console.log('shopDetail.value',shopDetail.value);
    
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
  localStorage.setItem('order', JSON.stringify(orderData));
  
  router.push({ name: 'Payment', params: { lang: lang } })
}


</script>

<template>
  <div class="_shopDetail" v-if="shopDetail">

  <a-row :gutter="20">
    <a-col :sm="{ span: 24 }" :md="{ span: 6 }">
      <div class="_shopDetail_img">
        <img
          v-if="shopDetail.cover"
          :alt="shopDetail.name"
          :src="shopDetail.cover"
          style="width: 100%; height: 100%; object-fit: cover;"
        />
      </div>
      <h1 class="_shopDetail_name _h1">{{ shopDetail.name }}</h1>
      <a-rate class="_shopDetail_rate" v-model:value="shopDetail.rating" allow-half disabled /> 
      <span class="_shopDetail_rateNum">{{ shopDetail.rating }}</span>
      <p class="_shopDetail_des">{{ shopDetail.description }}</p>
    </a-col>

    <a-col :sm="{ span: 24 }" :md="{ span: 18 }" style="width: 100%;">
      <ul class="_shopDetail_menu">
        <li class="_shopDetail_menu__item" v-for="item,index in shopDetail.menu" :key="index">
          <div class="_shopDetail_menu__left">
            <img class="_shopDetail_menu__img" v-if="item.image" alt="" :src="item.image" />
            <img class="_shopDetail_menu__img" v-else alt="" src="@/assets/default.jpg" />
            
            <!-- product intro card -->
            <a-button type="text" shape="circle" @click="showCard(index)" class="_shopDetail_menu__infoIcon">
              <i class="las la-info-circle"></i>
            </a-button>

            <div class="_shopDetail_prodIntro" :class="currCard == index && isShow ? 'show' : ''"  @click="isShow = false">
              <a-card hoverable class="_shopDetail_prodIntro__card">
                <template #cover>
                  <i class="las la-times _shopDetail_prodIntro__close"></i>
                  <img class="_shopDetail_menu__img" v-if="item.image" alt="" :src="item.image" />
                  <img class="_shopDetail_menu__img" v-else alt="" src="@/assets/default.jpg" />
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
            <div class="_shopDetail_order__price">
              <span class="_shopDetail_order__currency">NTD</span>
              <span class="_shopDetail_order__num">{{ item.price }}</span>
            </div>
            <div class="_shopDetail_count" :class="item.qty > 0 ? 'show' : ''">
              <span class="_shopDetail_count__btn minus" @click="item.qty > 0 ? item.qty-- : '' "></span>
              <input class="_shopDetail_count__num" v-model="item.qty" type="text" disabled/>
              <span class="_shopDetail_count__btn plus" @click="item.qty < 20 ? item.qty++ : '' "></span>
            </div>
          </div>
        </li>
      </ul>
    
      <div class="_shopDetail_btn">
        <a-button class="_shopDetail_btn_wrap"  @click="goPayment" type="primary" block>
          <!-- <div>Total<span class="_shopDetail_btn_total">{{ total }}</span></div> -->
          {{ t('next') }}
        </a-button>
      </div>
    </a-col>
  </a-row>


  </div>
</template>

<style scoped lang="scss">
._shopDetail_btn{
  position: fixed;
  left: 0;
  bottom: 0;
  z-index: 1;
  padding: 1rem;
  width: 100%;
}
._shopDetail_btn_wrap{
  display: flex;
  justify-content: center;
  align-items: center;
  height: 3.5rem;
  border-radius: 30px;
  font-size: 1rem;
  box-shadow: 0 0.5rem 1rem #00000026;
}
._shopDetail_btn_total{
  font-size: 1.5rem;
  margin-left: .25rem;
  font-weight: bold;
}
._shopDetail_img{
  height: 200px;
  overflow: hidden;
  border-radius: $border-radius;
  margin-bottom: 1rem;
}
._shopDetail_name{
  text-align: left;
  font-weight: bold;
  margin: 1rem 0 !important;
}
._shopDetail_menu{
  display: flex;
  flex-wrap: wrap;
  // gap: 1rem;
  gap: 4%;
  flex-direction: column;
}
._shopDetail_menu__item{
  display: flex;
  margin-bottom: 1rem;
  border-radius: $border-radius;
  overflow: hidden;
  box-shadow: 0 0.5rem 1rem #00000026;
  background-color: white;
  // flex-direction: column;
  // flex: 0 0 48%;

  &.buy{
  box-shadow: 0 0.5rem 1rem $color-primary;
  }
}
._shopDetail_menu__left{
  flex: 2;
  position: relative;
}
._shopDetail_menu__right{
  flex: 3;
  padding: 1rem;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}
._shopDetail_menu__img{
  width: 100%;
  height: 100%;
  object-fit: cover;
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
  background-color: rgba($color: $color-secondary, $alpha: .9);
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
  width: 85%;
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
  margin-bottom: .5rem;
  line-height: 1.5;
}
._shopDetail_count{
  display: flex;
  align-items: center;
  // justify-content: flex-end;
  justify-content: space-between;

  &.show{
    ._shopDetail_count__num{
      opacity: 1;
      transform: translateX(0);
    }
    ._shopDetail_count__btn.minus{
      opacity: 1;
      transform: translateX(0);
    }
  }
}
._shopDetail_count__btn{
  cursor: pointer;
  display: flex;
  align-items: center;
  border-radius: 50%;
  justify-content: center;
  color: $color-primary;
  font-size: 1.5rem;
  width: 2.5rem;
  height: 2.5rem;
  // background-color: rgba($color: $color-primary, $alpha: .2);
  background-color: $color-secondary;
  position: relative;
  transition: .3s all ease;

  &.minus{
    opacity: 0;
    transition: .2s all ease;
    transform: translateX(.5rem);

    &::before{
      width: 20px;
      border-bottom: 4px solid $color-primary;
      content: '';
      display: block;
    }
  }
  &.plus{
    &::before{
      width: 20px;
      border-bottom: 3px solid $color-primary;
      content: '';
      display: block;
      position: absolute;
    }
    &::after{
      width: 20px;
      border-bottom: 3px solid $color-primary;
      transform: rotate(90deg);
      content: '';
      display: block;
    }
  }

  &:hover{
    filter: brightness(120%);
  }
}
._shopDetail_count__num{
  color: $color-primary;
  max-width: 4rem;
  font-size: 2rem;
  text-align: center;
  font-weight: bold;
  opacity: 0;
  transform: translateX(.25rem);
  transition: .2s all ease;
}
._shopDetail_order__currency{
  // transform: translateY(-5px);
}
._shopDetail_order__price{
  display: flex;
  align-items: end;
  // flex: auto;
  margin-bottom: 1rem;
}
._shopDetail_order__num{
  font-size: 1.5rem;
  font-weight: bold;
  margin-left: .5rem;
}

._shopDetail_rate{
  margin-bottom: .5rem;
}
._shopDetail_rateNum{
  margin-left: 1rem;
}
._shopDetail_des{
  margin-bottom: 1.5rem;
  line-height: 1.5;
}

@media(min-width: $breakpoint-m){
  ._shopDetail_menu{
    flex-direction: row;
  }
  ._shopDetail_menu__item{
    flex: 0 0 48%;
  }
  ._shopDetail_menu__name{
    font-size: 1.25rem;
  }
}
</style>
