<script setup>
import axios from 'axios';
import { reactive, ref, computed, onMounted } from 'vue';
// import { useStore } from "vuex";
import { useRouter, useRoute } from "vue-router";
import api from '@/axios/api.js';

const shopList = ref([])
const route = useRoute()
const lang = route.params.lang;

// i18n
import { useI18n } from "vue-i18n";
const { t, locale } = useI18n({ useScope: "global" });

const getShopList = async()=>{
  try {
    const res = await api.get(`${lang}/shops`);
    shopList.value = res.data;
    // console.log('shopList.value',shopList.value);  
  } catch (error) {
    console.error(error);
  }
}


onMounted(async () => {
  try {
    await Promise.all([
      getShopList(),
    ]);
  } catch (error) {
    console.error(error);
  }
});
</script>

<template>
  <a-typography-title class="_h1 _shopList_title">{{ t('nightmarket.raohe') }} <span class="_shopList_title__top">TOP 10</span> </a-typography-title>
  <a-row :gutter="[10, 20]">
    <a-col :xs="12" :sm="6" :md="6" :lg="6" v-for="shop,idx in shopList" :key="idx">
      <router-link :to="`/${lang}/shop/${shop.shop_id}`">
        <a-card hoverable class="_shopList_item">
          <template #cover>
            <div class="_shopList_item__cover">
              <img v-if="shop.cover"
                :alt="shop.name"
                :src="shop.cover"
              />
              <img v-else
                alt="locoStall"
                src="@/assets/default.jpg"
              />
            </div>
          </template>
          <a-card-meta :style="{ height: '6rem' }" :title="shop.name" :description="shop.description">
          </a-card-meta>

          <template #actions>
            <div class="_shopList_rate">
              <a-rate class="_shopList_rate__star" v-model:value="shop.rating" allow-half disabled />
              <span class="_shopList_rate__num">{{ shop.rating }}</span>
            </div>
          </template>
        </a-card>
      </router-link>
    </a-col>
  </a-row>

</template>

<style scoped lang="scss">
._shopList{
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  gap: 2%;

  > a{
    display: flex;
    flex-basis: 18% !important;
  }
}
._shopList_title{
  margin-bottom: 2rem !important;
}
._shopList_title__top{
  font-size: 1.25rem;
  margin-left: .5rem;
  font-weight: bold;
  color: $color-primary;
  background-color: $color-secondary;
  padding: .5rem 1rem;
  border-radius: 2rem;
}
._shopList_item{
  width: 100%;
  box-shadow: 0 0.5rem 1rem #00000026;
}
._shopList_item__cover{
  height: 10rem;
  overflow: hidden;

  img{
    height: 100%;
    width: 100%;
    object-fit: cover;
  }
}
._shopList_rate{
  display: flex;
  padding: 0  1.25rem;
  align-items: center;
  justify-content: space-between;
}
._shopList_rate__star{
  font-size: .75rem;
}
._shopList_rate__num{
  margin-left: .5rem;
  display: inline-flex;
}
</style>
