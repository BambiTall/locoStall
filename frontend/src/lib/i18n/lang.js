import { createI18n } from 'vue-i18n'

import en from './langPack/en.json'
import zh from './langPack/zh.json'
import jp from './langPack/jp.json'

// lang 初始值
let defaultLang = localStorage.getItem("currLang");

if( defaultLang == null){
  defaultLang = 'en';
} else if( defaultLang == 'ja'){
  defaultLang = 'jp';
  localStorage.setItem("currLang", 'jp');
}
console.log('@i18n lang', defaultLang);

const i18n = createI18n({
    legacy: false,
    allowComposition: true,
    globalInjection: true,
    locale: defaultLang,           // 設定語言
    fallbackLocale: defaultLang,   // 若選擇的語言缺少翻譯則退回的語言
    messages: {
      zh,en,jp
    }
})


// i18n.global.locale = 'tw';
export default i18n