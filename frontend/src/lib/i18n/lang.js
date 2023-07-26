import { createI18n } from 'vue-i18n'

import en from './langPack/en.json'
import tw from './langPack/tw.json'
import jp from './langPack/jp.json'

var defaultLang = "en";




const i18n = createI18n({
    legacy: false,
    allowComposition: true,
    globalInjection: true,
    locale: defaultLang,           // 設定語言
    fallbackLocale: defaultLang,   // 若選擇的語言缺少翻譯則退回的語言
    messages: {
      // "中文": tw,
      // "EN": en,
      tw,en,jp
    }
})


// i18n.global.locale = 'tw';
export default i18n