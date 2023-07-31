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
  <a-typography-title>{{ t('index.shop_list') }} </a-typography-title>
  <a-row :gutter="[20, 20]">
    <a-col :xs="24" :sm="6" :md="6" :lg="6" v-for="shop,idx in shopList" :key="idx">
      <router-link :to="`/${lang}/shop/${shop.shop_id}`">
        <a-card hoverable class="_shopList_item">
            <template #cover>
              <img
                alt="example"
                src="@/assets/default.jpg"
              />
            </template>
            <template class="ant-card-actions" #actions>
              Know more
            </template>
              <a-card-meta :title="shop.name" :description="shop.description">
              </a-card-meta>
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
._shopList_item{
  width: 100%;
}
</style>
