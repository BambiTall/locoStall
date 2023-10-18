<script setup>
import Navigation from "../src/components/Navigation.vue";
import { useRouter, useRoute } from "vue-router";
import { reactive, ref, computed, onBeforeMount, onMounted, watch } from 'vue';
import { useStore } from "vuex";
import i18n from '@/lib/i18n/lang'
import api from '@/axios/api.js';

const store = useStore();
const router = useRouter();

// local storage
const loggedInId = ref(localStorage.getItem('id'));
let isLoggedIn = ref(localStorage.getItem('login'));

const lang = ref(localStorage.getItem('currLang'));
console.log('@App lang', lang.value);


let accessToken = ref()
let isBrowserCheck = ref()
let isInClient = ref(false)
let message = ref()
let adminSendMsgRes = ref()
let profile = ref()

// getters
const currUser = computed(() => store.getters.currUser);

router.beforeEach((to, from, next) => {
  // handle 跳轉
  if (to.fullPath === '/') {
    next({ 
      path: `/${lang.value}`,
      query: to.query
    });
  }
  //  else if (to.meta.requiresAuth) {
  //   // console.log('需要 AUTH');
  //   if( !isLoggedIn ){
  //     // console.log('還沒登入');
  //     next({
  //       path: lang.value + '/login',
  //       query: { redirect: to.fullPath },
  //     });
  //   } else {
  //     // console.log('已登入');
  //     next();
  //   }
  // } 
  else {
    // console.log('不需 AUTH');
    // visit with lang
    store.dispatch('setCurrLang', to.params.lang);
    next();
  }
});

const lineProgress = async (params) => {
  try {
    let signUpLineRes = await api.post(`/line_user`, params);
    let getLineUserRes = await api.get(`/line_user/${signUpLineRes.data.line_id}`);

    localStorage.setItem('id', getLineUserRes.data.id);
    store.dispatch('setCurrUser', getLineUserRes.data);
  } catch (error) {
    // console.error(error);
  }
};

onBeforeMount(async () => {
  try{    
    if( loggedInId.value != null && Object.keys(currUser.value).length == 0){
      const getUserDataRes = await store.dispatch('getUserData', Number(loggedInId.value));
      store.dispatch('login',true)
    }
  } catch {

  }
});

import liff from "@line/liff";

const sendAdmintoUserMessege = async()=> {
  adminSendMsgRes.value = await api.post('/backend/token', {
    accessToken: accessToken.value,
  });
  alert('adminSendMsgRes', adminSendMsgRes);
}

onMounted(async () => {
  try {
    await liff.init({ liffId: "2000144386-Ax8WZ8k2" });

    isInClient.value =liff.isInClient();

    if(Boolean(isInClient.value)){
      accessToken.value = liff.getAccessToken();
      if (accessToken.value == null) {
        isBrowserCheck.value = false;
        message.value = "LINEアプリから実行してください";
        return false;
      }
      isBrowserCheck.value = true;
      message.value = "ログイン成功";
      
      let nativeLang = ''
      const liffLang = liff.getLanguage();
      
      if (liffLang.includes('ja')) {
        nativeLang = 'jp';
      } else if (liffLang.includes('zh')) {
        nativeLang = 'zh';
      } else {
        nativeLang = 'en';
      }

      const liffProfile = await liff.getProfile()
      profile.value = liffProfile
      let params = {
        line_id: liffProfile.userId,
        display_name: liffProfile.displayName,
        photo: liffProfile.pictureUrl,
        native_lang: nativeLang
      }

      lineProgress(params)

      setTimeout(async() => {
    liff.sendMessages([
        {
          'type': 'text',
          'text': 'This is a Text Message'
        },
        {
            'type': 'flex',
            'altText': 'Flex Message',
            'contents': {
              "type": "bubble",
              "header": {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "text",
                    "text": "注文番号",
                    "weight": "bold",
                    "color": "#3f3b34"
                  },
                  {
                    "type": "text",
                    "text": "70",
                    "size": "xxl",
                    "align": "end",
                    "weight": "bold",
                    "color": "#ffc648",
                    "action": {
                      "type": "uri",
                      "label": "action",
                      "uri": "https://liff.line.me/2000144386-Ax8WZ8k2/jp/user/order"
                    }
                  }
                ],
                "alignItems": "center"
              },
              "hero": {
                "type": "image",
                "url": "https://raw.githubusercontent.com/BambiTall/locoStall/main/frontend/src/assets/img/tofu.jpg",
                "size": "full",
                "aspectRatio": "20:13",
                "aspectMode": "cover",
                "align": "center"
              },
              "body": {
                "type": "box",
                "layout": "vertical",
                "spacing": "md",
                "contents": [
                  {
                    "type": "text",
                    "text": "名彭下港臭豆腐",
                    "wrap": true,
                    "weight": "bold",
                    "gravity": "center",
                    "size": "xl"
                  },
                  {
                    "type": "box",
                    "layout": "vertical",
                    "margin": "lg",
                    "spacing": "sm",
                    "contents": [
                      {
                        "type": "box",
                        "layout": "baseline",
                        "spacing": "sm",
                        "contents": [
                          {
                            "type": "text",
                            "text": "1",
                            "weight": "bold",
                            "size": "lg",
                            "color": "#ffc648"
                          },
                          {
                            "type": "text",
                            "text": "揚げ臭豆腐",
                            "wrap": true,
                            "size": "md",
                            "color": "#666666",
                            "flex": 6,
                            "weight": "bold"
                          },
                          {
                            "type": "text",
                            "text": "60",
                            "align": "end",
                            "weight": "bold",
                            "size": "md"
                          }
                        ]
                      },
                      {
                        "type": "separator",
                        "margin": "xl"
                      },
                      {
                        "type": "box",
                        "layout": "baseline",
                        "spacing": "sm",
                        "contents": [
                          {
                            "type": "text",
                            "text": "総額",
                            "wrap": true,
                            "size": "lg",
                            "color": "#666666"
                          },
                          {
                            "type": "text",
                            "text": "60",
                            "align": "end",
                            "size": "xl",
                            "weight": "bold"
                          }
                        ],
                        "margin": "xl"
                      },
                      {
                        "type": "separator",
                        "margin": "xl"
                      },
                      {
                        "type": "box",
                        "layout": "baseline",
                        "spacing": "sm",
                        "contents": [
                          {
                            "type": "text",
                            "text": "支払い",
                            "color": "#aaaaaa",
                            "size": "sm"
                          },
                          {
                            "type": "text",
                            "text": "LINE PAY",
                            "wrap": true,
                            "color": "#666666",
                            "size": "sm",
                            "align": "end",
                            "flex": 3
                          },
                          {
                            "type": "text",
                            "wrap": true,
                            "color": "#93c878",
                            "size": "sm",
                            "text": "支払済",
                            "align": "end",
                            "weight": "bold"
                          }
                        ],
                        "margin": "xl"
                      },
                      {
                        "type": "box",
                        "layout": "baseline",
                        "spacing": "sm",
                        "contents": [
                          {
                            "type": "text",
                            "text": "注文時間",
                            "color": "#aaaaaa",
                            "size": "sm"
                          },
                          {
                            "type": "text",
                            "text": "2023/08/19 13:52",
                            "wrap": true,
                            "color": "#666666",
                            "size": "sm",
                            "align": "end"
                          }
                        ],
                        "margin": "sm"
                      }
                    ]
                  }
                ]
              }
            }

            }
    ]).then(() => {
      
    }).catch((err) => {
        console.error(err);
    });
}, 3000);

    }
  } catch (err) {
    console.log(`liff.state init error ${err}`);
  }
})

// custom theme
const theme = {
  token: {
    colorPrimary: '#ffc648',
    colorBgLayout: '#ffffff',
    borderRadius: 30
  },
};
</script>

<template>
  <a-config-provider :theme="theme">
   <a-layout class="_layout">
      <a-layout-header class="_header">      
        <Navigation />
      </a-layout-header>
      <a-layout-content class="_body">

        <!-- <div class="_body_liffwrap">
          <a-button @click="sendAdmintoUserMessege" type="primary" size="circle">
            Admin Send
          </a-button>
          <p><h4>message: </h4> {{ message }}</p>
          <p><h4>accessToken: </h4> {{ accessToken }}</p>
          <p><h4>adminSendMsgRes: </h4> {{ adminSendMsgRes }}</p>
          <p><h4>profile: </h4>{{ profile }}</p>
        </div> -->

        <router-view/>

        <a-layout-footer class="_footer">
          © locoStall 2023
        </a-layout-footer>
      </a-layout-content>
    </a-layout>
  </a-config-provider>
</template>

<style lang="scss">
@import "../src/assets/scss/style.scss";
// ._layout{
//   height: 100%;
// }
._header{
  position: fixed;
  display: flex;
  justify-content: space-between;
  z-index: 2;
  width: 100%;
  // background-color: $color-secondary !important;
  background-color: white !important;
  padding: 0 !important;

}
._body{
  width: 100%;
  max-width: $page-max-width;
  margin: auto;
  padding: 5rem $padding-s 0 !important;
  min-height: 100vh !important;
}
._body_liffwrap{
  * {
    word-wrap: break-word
  }
}
._footer{
  text-align: center;
}

@media(min-width: $breakpoint-s){
  // ._header{
  //   padding: 0 $padding-m !important;
  // }

  ._body{
    padding-top: 6rem !important;
  }
}
</style>
