import { createRouter, createWebHistory } from 'vue-router'

import Login from '../pages/Login.vue';
import SignUp from '../pages/SignUp.vue';
import LiffLogin from '../pages/LiffLogin.vue';
import User from '../pages/user/User.vue';
import UserOrderHistory from '../pages/user/OrderHistory.vue';
import ShopDetail from '../pages/ShopDetail.vue';
import Index from '../pages/Index.vue';
import Payment from '../pages/Payment.vue';
import OrderConfirm from '../pages/OrderConfirm.vue';
import Sandy from '../pages/Sandy.vue';

// Admin
import OrderList from '../pages/admin/OrderList.vue';

// Not Found
import NotFound from '../pages/NotFound.vue';

// let route_base = 'en'
// let history = createWebHistory(route_base);

import i18n from '@/lib/i18n/lang'

let history = createWebHistory();

let routes = [
  // {
  //   path: '/',
  //   name: 'Home',
  //   redirect: '/'+ i18n.global.locale.value
  // },
  {
    path: '/:lang',
    name: 'Index',
    component: Index
  },
  {
    // /zh/shop/1
    path: '/:lang/shop/:id',
    name: 'ShopDetail',
    component: ShopDetail
  },
  {
    path: '/:lang/payment',
    name: 'Payment',
    component: Payment
  },
  {
    path: "/:lang/login",
    name: 'Login',
    component: Login,
  },
  {
    path: "/:lang/signup",
    name: 'SignUp',
    component: SignUp,
  },
  {
    path: "/:lang/user/profile",
    name: 'User',
    component: User,
    meta: { requiresAuth: true }
  },
  {
    path: "/:lang/user/order",
    name: 'UserOrderHistory',
    component: UserOrderHistory,
    meta: { requiresAuth: true }
  },
  {
    path: "/:lang/login/liff",
    name: 'LiffLogin',
    component: LiffLogin,
  },
  {
    path: '/:lang/payment',
    name: 'Payment',
    component: Payment
  },
  {
    path: '/:lang/orderConfirm',
    name: 'OrderConfirm',
    component: OrderConfirm
  },
  // Admin
  {
    path: '/:lang/admin/',
    name: 'OrderList',
    component: OrderList,
    meta: { requiresAuth: true }
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: NotFound
  },
  {
    path: '/sandy',
    name: 'Sandy',
    component: Sandy
  }
  
]

const router = createRouter({ history, routes });

export default router