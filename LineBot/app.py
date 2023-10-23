from flask import Flask, request, abort, jsonify

from linebot import (
    LineBotApi, WebhookHandler
)

from linebot.exceptions import (
    InvalidSignatureError
)

import requests
import os
import json

import logging
import google.cloud.logging
from google.cloud.logging.handlers import CloudLoggingHandler

client = google.cloud.logging.Client()


# 建立line event log，用來記錄line event
bot_event_handler = CloudLoggingHandler(client,name="bot_event")
bot_event_logger=logging.getLogger('bot_event')
bot_event_logger.setLevel(logging.INFO)
bot_event_logger.addHandler(bot_event_handler)

app = Flask(__name__)
line_bot_api = LineBotApi("sA/voEKSLrbVFPU/Y0kDRVQ12QS83+0uosFPY3yuFbiIaJHqW04g+I7GhaO8n3+9//wKym0tN0FTHW8z2WvZopw4Mvf29mxwLLviZI8AeFIqJbJTolky3Ls4uVcnMLr6/MSey67rF3oBmvqOANzOUAdB04t89/1O/w1cDnyilFU=")

handler = WebhookHandler("5d5144941f2eefa3806df63d8826d6b2")

@app.route("/", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    print(body)
    bot_event_logger.info(body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

menuDataEn ="""
{
  "size": {
    "width": 2500,
    "height": 1686
  },
  "selected": true,
  "name": "Menu",
  "chatBarText": "More Info",
  "areas": [
    {
      "bounds": {
        "x": 63,
        "y": 61,
        "width": 2369,
        "height": 756
      },
      "action": {
        "type": "postback",
        "text": "Get Started",
        "data": "data1"
      }
    },
    {
      "bounds": {
        "x": 62,
        "y": 888,
        "width": 742,
        "height": 741
      },
      "action": {
        "type": "postback",
        "text": "Language Setting",
        "data": "data2"
      }
    },
    {
      "bounds": {
        "x": 889,
        "y": 887,
        "width": 737,
        "height": 737
      },
      "action": {
        "type": "postback",
        "text": "Explore",
        "data": "data3"
      }
    },
    {
      "bounds": {
        "x": 1706,
        "y": 874,
        "width": 734,
        "height": 756
      },
      "action": {
        "type": "uri",
        "uri": "https://line.me/R/nv/camera/"
      }
    }
  ]
}
"""
menuDataZh ="""
{
  "size": {
    "width": 2500,
    "height": 1686
  },
  "selected": true,
  "name": "選單",
  "chatBarText": "展開選單",
  "areas": [
    {
      "bounds": {
        "x": 63,
        "y": 61,
        "width": 2369,
        "height": 756
      },
      "action": {
        "type": "postback",
        "text": "使用說明",
        "data": "data1"
      }
    },
    {
      "bounds": {
        "x": 62,
        "y": 888,
        "width": 742,
        "height": 741
      },
      "action": {
        "type": "postback",
        "text": "語言設定",
        "data": "data2"
      }
    },
    {
      "bounds": {
        "x": 889,
        "y": 887,
        "width": 737,
        "height": 737
      },
      "action": {
        "type": "postback",
        "text": "探索更多",
        "data": "data3"
      }
    },
    {
      "bounds": {
        "x": 1706,
        "y": 874,
        "width": 734,
        "height": 756
      },
      "action": {
        "type": "uri",
        "uri": "https://line.me/R/nv/camera/"
      }
    }
  ]
}
"""
menuDataJa = """
{
  "size": {
    "width": 2500,
    "height": 1686
  },
  "selected": true,
  "name": "メニュー",
  "chatBarText": "詳細情報",
  "areas": [
    {
      "bounds": {
        "x": 63,
        "y": 61,
        "width": 2369,
        "height": 756
      },
      "action": {
        "type": "postback",
        "text": "使用説明",
        "data": "data1"
      }
    },
    {
      "bounds": {
        "x": 62,
        "y": 888,
        "width": 742,
        "height": 741
      },
      "action": {
        "type": "postback",
        "text": "言語設定",
        "data": "data2"
      }
    },
    {
      "bounds": {
        "x": 889,
        "y": 887,
        "width": 737,
        "height": 737
      },
      "action": {
        "type": "postback",
        "text": "探す",
        "data": "data3"
      }
    },
    {
      "bounds": {
        "x": 1706,
        "y": 874,
        "width": 734,
        "height": 756
      },
      "action": {
        "type": "uri",
        "uri": "https://line.me/R/nv/camera/"
      }
    }
  ]
}
"""

from linebot.models.events import FollowEvent

def link_rich_menu_to_user(user_id, rich_menu_id):
    line_bot_api.link_rich_menu_to_user(user_id, rich_menu_id)

# Save user IDs to a file when they interact with the rich menu
@handler.add(FollowEvent)
def reply_text_and_get_user_profile(event):
    # Get user profile
    menuJson = json.loads(menuDataEn)
    lineRichMenuId = line_bot_api.create_rich_menu(rich_menu=RichMenu.new_from_json_dict(menuJson))
    uploadImageFile = open(r"richmenu_en.jpg", 'rb')
    open("tmp"+ event.source.user_id + ".txt","a").close()
    line_bot_api.set_rich_menu_image(lineRichMenuId,'image/jpeg',uploadImageFile)
    line_bot_api.link_rich_menu_to_user(event.source.user_id, lineRichMenuId)
    user_profile = line_bot_api.get_profile(event.source.user_id)
    link_rich_menu_to_user(user_profile.user_id, lineRichMenuId)

from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageSendMessage, PostbackEvent, TemplateSendMessage,
    CarouselTemplate, CarouselColumn, QuickReplyButton, PostbackAction, QuickReply, RichMenu, ImageMessage, 
    FlexSendMessage, BubbleContainer, ImageComponent, BoxComponent, TextComponent, IconComponent, ButtonComponent, URIAction
)
import requests

language = "en"  # 預設語言為英文

@handler.add(PostbackEvent)
def handle_postback(event):
    global language

    if event.postback.data == 'data1':
        with open("tmp/"+ event.source.user_id + ".txt","r") as f:
            language = f.read()
        reply_text = get_instruction_text(language)  # Get Started 功能
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_text)
        )
        return

    elif event.postback.data == 'data2':  #選擇語言功能
        quick_reply = QuickReply(
            items=[
                QuickReplyButton(action=PostbackAction(label="中文", data="zh")),
                QuickReplyButton(action=PostbackAction(label="English", data="en")),
                QuickReplyButton(action=PostbackAction(label="日本語", data="ja"))
            ]
        )
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='Language Setting', quick_reply=quick_reply)
        )
        return

    elif event.postback.data == 'data3':
        with open("tmp/"+ event.source.user_id + ".txt","r") as f:
            language = f.read()
        carousel_template = create_carousel_template(language)  # explore 清單
        template_message = TemplateSendMessage(
            alt_text='Carousel Template',
            template=carousel_template
        )
        line_bot_api.reply_message(event.reply_token, template_message)
        return

    elif event.postback.data == 'zh':
        language = "zh"
        with open("tmp/"+ event.source.user_id + ".txt","w") as f:
            f.write(language)
        menuJson=json.loads(menuDataZh)
        lineRichMenuId = line_bot_api.create_rich_menu(rich_menu=RichMenu.new_from_json_dict(menuJson))
        print(lineRichMenuId)
        uploadImageFile = open(r"richmenu_zh.jpg", 'rb')
        line_bot_api.set_rich_menu_image(lineRichMenuId,'image/jpeg',uploadImageFile)
        line_bot_api.link_rich_menu_to_user(event.source.user_id, lineRichMenuId)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='設定完成')
        )
        return

    elif event.postback.data == 'ja':
        language = "ja"  # 更新語言設定為日文
        with open("tmp/"+ event.source.user_id + ".txt","w") as f:
            f.write(language)
        menuJson=json.loads(menuDataJa)
        lineRichMenuId = line_bot_api.create_rich_menu(rich_menu=RichMenu.new_from_json_dict(menuJson))
        print(lineRichMenuId)
        uploadImageFile = open(r"richmenu_ja.jpg", 'rb')
        line_bot_api.set_rich_menu_image(lineRichMenuId,'image/jpeg',uploadImageFile)
        line_bot_api.link_rich_menu_to_user(event.source.user_id, lineRichMenuId)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='セットアップが完了しました')
        )
        return

    elif event.postback.data == 'en':
        language = "en"  # 更新語言設定為英文
        with open("tmp/"+ event.source.user_id + ".txt","w") as f:
            f.write(language)
        menuJson = json.loads(menuDataEn)
        lineRichMenuId = line_bot_api.create_rich_menu(rich_menu=RichMenu.new_from_json_dict(menuJson))
        print(lineRichMenuId)
        uploadImageFile = open(r"richmenu_en.jpg", 'rb')
        line_bot_api.set_rich_menu_image(lineRichMenuId,'image/jpeg',uploadImageFile)
        line_bot_api.link_rich_menu_to_user(event.source.user_id, lineRichMenuId)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='Setup complete')
        )
        return

def get_instruction_text(language):
    # with open("tmp/"+ event.source.user_id + ".txt","w") as f:
    #         f.read(language)
    # 根據語言回傳引導指示文案
    if language == "zh":
        return "【使用說明】\n\n• 拍照點單\n點擊按鈕，開起相機，拍攝招牌以獲得點餐連結\n\n• 語言設定\n選擇中文、日文或英文\n\n• 探索\n尋找更多夜市美食 "
    elif language == "ja":
        return "【使用説明】\n\n• 画像検索\nボタンをタップしてカメラを起動し、看板を撮影して注文リンクをゲットしよう\n\n• 言語\n中国語、日本語、英語から選択\n\n• 探す\nもっと夜市の美味しいものを見つけよう！"
    else:
        return "Instructions:\n\n• Snap-to-Order\nJust tap the button, open your camera, snap a photo of the sign, and get the ordering link.\n\n• Language\nChoose from Chinese, Japanese, or English.\n\n• Explore\nDiscover more night market delights!"

def create_carousel_template(language):
    carousel_columns = []

    if language == "zh":
        carousel_column1 = CarouselColumn(
            thumbnail_image_url='https://leafyeh.com/wp-content/uploads/flickr/47417246271_9679a79ba4_b.jpg',
            title='福州世祖胡椒餅',
            text='外皮酥酥脆脆，內餡則是濃郁的肉香與胡椒粉微微的嗆辣，兩者融合而成的香氣，滿滿的鮮甜，一吃就覺得好幸福',
            actions=[
                URIAction(label='點餐', uri='https://liff.line.me/2000144386-Ax8WZ8k2/zh/shop/0')
            ]
        )
        carousel_columns.append(carousel_column1)

        carousel_column2 = CarouselColumn(
            thumbnail_image_url='https://cdn2.ettoday.net/images/6280/d6280464.jpg',
            title='老芋仔芋頭酥',
            text='流芯酥曾獲得2021比利時美食評鑑推薦，堅持古法手工製作，嚴選用料，創新之餘仍保留古早味的精髓，讓人「芋」罷不能',
            actions=[
                URIAction(label='點餐', uri='https://liff.line.me/2000144386-Ax8WZ8k2/zh/shop/1')
            ]
        )
        carousel_columns.append(carousel_column2)

        carousel_column3 = CarouselColumn(
            thumbnail_image_url='https://ak-d.tripcdn.com/images/100s0z000000n2at66F03.jpg',
            title='施老闆麻辣臭豆腐',
            text='榮獲2018年台北米其林指南，麻辣湯底有股中藥味，喝起來十分舒服',
            actions=[
                URIAction(label='點餐', uri='https://liff.line.me/2000144386-Ax8WZ8k2/zh/shop/2')
            ]
        )
        carousel_columns.append(carousel_column3)

        carousel_column4 = CarouselColumn(
            thumbnail_image_url='https://lordcat.tw/wp-content/uploads/2022/04/1651325631-1622d5c737a238168a234103228b3e2d.jpg',
            title='下港名彭臭豆腐',
            text='有著最傳統的台灣小吃，其中讓人又愛又恨的脆皮臭豆腐為招牌，天天熱賣上千份又香又臭的臭豆腐絕不能錯過',
            actions=[
                URIAction(label='點餐', uri='https://liff.line.me/2000144386-Ax8WZ8k2/zh/shop/3')
            ]
        )
        carousel_columns.append(carousel_column4)

        carousel_column5 = CarouselColumn(
            thumbnail_image_url='https://lordcat.tw/wp-content/uploads/2019/04/1652191927-fecf413191371cf259cfb131a00c24b6.jpg',
            title='阿國滷味',
            text='連續在2019及2020登上米其林指南，琳琅滿目食材令人口水直流，同時標價清楚',
            actions=[
                URIAction(label='點餐', uri='https://liff.line.me/2000144386-Ax8WZ8k2/zh/shop/4')
            ]
        )
        carousel_columns.append(carousel_column5)

        carousel_column6 = CarouselColumn(
            thumbnail_image_url='https://lordcat.tw/wp-content/uploads/2016/08/1652285181-0d3e4265b5fcf5f82d5add629469f506.jpg',
            title='連家清燉豬腳',
            text='跳脫傳統醬油滷豬腳的手法，原汁原味的湯頭十分鮮甜，豬腳Q彈，而且豬腳處理得乾乾淨淨，完全沒有腥味',
            actions=[
                URIAction(label='點餐', uri='https://liff.line.me/2000144386-Ax8WZ8k2/zh/shop/5')
            ]
        )
        carousel_columns.append(carousel_column6)

        carousel_column7 = CarouselColumn(
            thumbnail_image_url='https://lh3.googleusercontent.com/xnzWNm7IiHeveS1grP5p_YZs9N_jfaJTiT0cakJSQqLwMgJlU-DD31ZzGHOYXTwZ_IWllGQ_N9QusU15oUiILW7dtOsrxp3Gj-jcM8styxDS8Q=s600',
            title='古早味寶寶麻糬',
            text='於2018~2021年連續4年獲得米其林的青睞，簡單中的不簡單、平凡中的不平凡，麻糬都是現包，只有賣麻糬以及菜燕',
            actions=[
                URIAction(label='點餐', uri='https://liff.line.me/2000144386-Ax8WZ8k2/zh/shop/6')
            ]
        )
        carousel_columns.append(carousel_column7)

        carousel_column8 = CarouselColumn(
            thumbnail_image_url='https://lordcat.tw/wp-content/uploads/2019/07/1652286920-242e52376d32d3137a236f1236f57adf.jpg',
            title='紅燒麵牛雜湯',
            text='2021年台北米其林必比登推薦，以牛肉麵、陽春麵、乾拌麵、牛雜湯為主，其中米其林推薦的是牛雜湯和乾拌麵',
            actions=[
                URIAction(label='點餐', uri='https://liff.line.me/2000144386-Ax8WZ8k2/zh/shop/7')
            ]
        )
        carousel_columns.append(carousel_column8)

        carousel_column9 = CarouselColumn(
            thumbnail_image_url='https://margaret.tw/wp-content/uploads/2020/09/nEO_IMG_DSC09917.jpg',
            title='東發號麵線油飯肉羹',
            text='曾榮獲2018米其林餐盤推薦，只賣三樣東西麵線、肉羹、油飯，但屹立百年老店',
            actions=[
                URIAction(label='點餐', uri='https://liff.line.me/2000144386-Ax8WZ8k2/zh/shop/8')
            ]
        )
        carousel_columns.append(carousel_column9)

        carousel_column10 = CarouselColumn(
            thumbnail_image_url='https://g.udn.com.tw/upfiles/B_JO/josh091029/PSN_PHOTO/833/f_27254833_1.JPG',
            title='福島屋圓圓燒',
            text='原汁原味日本大阪燒，圓圓的造型，豐富又多層次的口感',
            actions=[
                URIAction(label='點餐', uri='https://liff.line.me/2000144386-Ax8WZ8k2/zh/shop/9')
            ]
        )
        carousel_columns.append(carousel_column10)


    elif language == "ja":
        carousel_column1 = CarouselColumn(
            thumbnail_image_url='https://leafyeh.com/wp-content/uploads/flickr/47417246271_9679a79ba4_b.jpg',
            title='福州世祖胡椒餅',
            text='豚ひき肉とネギが入った肉まんを焼いたような 「焼まんじゅう」は、饒河街夜市の名物！',
            actions=[
                URIAction(label='注文', uri='https://liff.line.me/2000144386-Ax8WZ8k2/jp/shop/0')
            ]
        )
        carousel_columns.append(carousel_column1)

        carousel_column2 = CarouselColumn(
            thumbnail_image_url='https://cdn2.ettoday.net/images/6280/d6280464.jpg',
            title='老芋仔芋頭酥',
            text='古式手工製作、厳選された材料',
            actions=[
                URIAction(label='注文', uri='https://liff.line.me/2000144386-Ax8WZ8k2/jp/shop/1')
            ]
        )
        carousel_columns.append(carousel_column2)

        carousel_column3 = CarouselColumn(
            thumbnail_image_url='https://ak-d.tripcdn.com/images/100s0z000000n2at66F03.jpg',
            title='施老板臭豆腐',
            text='麻辣な食べ物で有名で、例えば辛くて香ばしい臭豆腐などがあります',
            actions=[
                URIAction(label='注文', uri='https://liff.line.me/2000144386-Ax8WZ8k2/jp/shop/2')
            ]
        )
        carousel_columns.append(carousel_column3)

        carousel_column4 = CarouselColumn(
            thumbnail_image_url='https://lordcat.tw/wp-content/uploads/2022/04/1651325631-1622d5c737a238168a234103228b3e2d.jpg',
            title='下港名彭臭豆腐',
            text='臭豆腐とカキオムレツで有名です',
            actions=[
                URIAction(label='注文', uri='https://liff.line.me/2000144386-Ax8WZ8k2/jp/shop/3')
            ]
        )
        carousel_columns.append(carousel_column4)

        carousel_column5 = CarouselColumn(
            thumbnail_image_url='https://lordcat.tw/wp-content/uploads/2019/04/1652191927-fecf413191371cf259cfb131a00c24b6.jpg',
            title='阿國滷味',
            text='多種多様な食材が合理的で手頃な価格で提供されています',
            actions=[
                URIAction(label='注文', uri='https://liff.line.me/2000144386-Ax8WZ8k2/jp/shop/4')
            ]
        )
        carousel_columns.append(carousel_column5)

        carousel_column6 = CarouselColumn(
            thumbnail_image_url='https://lordcat.tw/wp-content/uploads/2016/08/1652285181-0d3e4265b5fcf5f82d5add629469f506.jpg',
            title='連家豚足のクリアースープ麺線',
            text='クリアスープで煮込んだ豚足が有名で、伝統的な煮豚足とは異なります',
            actions=[
                URIAction(label='注文', uri='https://liff.line.me/2000144386-Ax8WZ8k2/jp/shop/5')
            ]
        )
        carousel_columns.append(carousel_column6)

        carousel_column7 = CarouselColumn(
            thumbnail_image_url='https://lh3.googleusercontent.com/xnzWNm7IiHeveS1grP5p_YZs9N_jfaJTiT0cakJSQqLwMgJlU-DD31ZzGHOYXTwZ_IWllGQ_N9QusU15oUiILW7dtOsrxp3Gj-jcM8styxDS8Q=s600',
            title='麻糬寶寶',
            text='麻糬と野菜燕を販売しています',
            actions=[
                URIAction(label='注文', uri='https://liff.line.me/2000144386-Ax8WZ8k2/jp/shop/6')
            ]
        )
        carousel_columns.append(carousel_column7)

        carousel_column8 = CarouselColumn(
            thumbnail_image_url='https://lordcat.tw/wp-content/uploads/2019/07/1652286920-242e52376d32d3137a236f1236f57adf.jpg',
            title='紅燒牛肉麵牛雜湯',
            text='牛肉麵とは、牛骨や香味野菜を煮込んだスープに、麺と牛肉が入った料理 です',
            actions=[
                URIAction(label='注文', uri='https://liff.line.me/2000144386-Ax8WZ8k2/jp/shop/7')
            ]
        )
        carousel_columns.append(carousel_column8)

        carousel_column9 = CarouselColumn(
            thumbnail_image_url='https://margaret.tw/wp-content/uploads/2020/09/nEO_IMG_DSC09917.jpg',
            title='東發號',
            text='麺線、肉羹、油飯で有名です',
            actions=[
                URIAction(label='注文', uri='https://liff.line.me/2000144386-Ax8WZ8k2/jp/shop/8')
            ]
        )
        carousel_columns.append(carousel_column9)

        carousel_column10 = CarouselColumn(
            thumbnail_image_url='https://g.udn.com.tw/upfiles/B_JO/josh091029/PSN_PHOTO/833/f_27254833_1.JPG',
            title='まるまる焼',
            text='豊富で多層的な食感を持つ素材',
            actions=[
                URIAction(label='注文', uri='https://liff.line.me/2000144386-Ax8WZ8k2/jp/shop/9')
            ]
        )
        carousel_columns.append(carousel_column10)

    elif language == "en":
        carousel_column1 = CarouselColumn(
            thumbnail_image_url='https://leafyeh.com/wp-content/uploads/flickr/47417246271_9679a79ba4_b.jpg',
            title='Fuzhou Black Pepper Bun',
            text='Crunchy and crispy outer layer with flavorful meat filling',
            actions=[
                URIAction(label='Order Link', uri='https://liff.line.me/2000144386-Ax8WZ8k2/en/shop/0')
            ]
        )
        carousel_columns.append(carousel_column1)

        carousel_column2 = CarouselColumn(
            thumbnail_image_url='https://cdn2.ettoday.net/images/6280/d6280464.jpg',
            title='Taro Pastry',
            text='Traditional handcrafted production',
            actions=[
                URIAction(label='Order Link', uri='https://liff.line.me/2000144386-Ax8WZ8k2/en/shop/1')
            ]
        )
        carousel_columns.append(carousel_column2)

        carousel_column3 = CarouselColumn(
            thumbnail_image_url='https://ak-d.tripcdn.com/images/100s0z000000n2at66F03.jpg',
            title='Shi Boss Spicy Tofu',
            text='Famous for spicy and hot food, such as spicy stinky tofu',
            actions=[
                URIAction(label='Order Link', uri='https://liff.line.me/2000144386-Ax8WZ8k2/en/shop/2')
            ]
        )
        carousel_columns.append(carousel_column3)

        carousel_column4 = CarouselColumn(
            thumbnail_image_url='https://lordcat.tw/wp-content/uploads/2022/04/1651325631-1622d5c737a238168a234103228b3e2d.jpg',
            title='Xiaogangmingpeng Stinky Tofu',
            text='Famous for crispy stinky tofu and oyster omelette',
            actions=[
                URIAction(label='Order Link', uri='https://liff.line.me/2000144386-Ax8WZ8k2/en/shop/3')
            ]
        )
        carousel_columns.append(carousel_column4)

        carousel_column5 = CarouselColumn(
            thumbnail_image_url='https://lordcat.tw/wp-content/uploads/2019/04/1652191927-fecf413191371cf259cfb131a00c24b6.jpg',
            title='A Kuo Lu Wei',
            text='Variety of ingredients at reasonable and affordable prices',
            actions=[
                URIAction(label='Order Link', uri='https://liff.line.me/2000144386-Ax8WZ8k2/en/shop/4')
            ]
        )
        carousel_columns.append(carousel_column5)

        carousel_column6 = CarouselColumn(
            thumbnail_image_url='https://lordcat.tw/wp-content/uploads/2016/08/1652285181-0d3e4265b5fcf5f82d5add629469f506.jpg',
            title='Lian\'s Stewed Pig Knuckle',
            text='Famous for stewed pork knuckles broth',
            actions=[
                URIAction(label='Order Link', uri='https://liff.line.me/2000144386-Ax8WZ8k2/en/shop/5')
            ]
        )
        carousel_columns.append(carousel_column6)

        carousel_column7 = CarouselColumn(
            thumbnail_image_url='https://lh3.googleusercontent.com/xnzWNm7IiHeveS1grP5p_YZs9N_jfaJTiT0cakJSQqLwMgJlU-DD31ZzGHOYXTwZ_IWllGQ_N9QusU15oUiILW7dtOsrxp3Gj-jcM8styxDS8Q=s600',
            title='Mochi Baby',
            text='Only sell mochi and sweetened white gourd jelly',
            actions=[
                URIAction(label='Order Link', uri='https://liff.line.me/2000144386-Ax8WZ8k2/en/shop/6')
            ]
        )
        carousel_columns.append(carousel_column7)

        carousel_column8 = CarouselColumn(
            thumbnail_image_url='https://lordcat.tw/wp-content/uploads/2019/07/1652286920-242e52376d32d3137a236f1236f57adf.jpg',
            title='Beef Noodles and Beef Entrails Soup',
            text='Famous for beef dishes, such as beef noodles',
            actions=[
                URIAction(label='Order Link', uri='https://liff.line.me/2000144386-Ax8WZ8k2/en/shop/7')
            ]
        )
        carousel_columns.append(carousel_column8)

        carousel_column9 = CarouselColumn(
            thumbnail_image_url='https://margaret.tw/wp-content/uploads/2020/09/nEO_IMG_DSC09917.jpg',
            title='Tung-Fa-Hao',
            text='Famous for vermicelli, pork-meat stew, and oily rice',
            actions=[
                URIAction(label='Order Link', uri='https://liff.line.me/2000144386-Ax8WZ8k2/en/shop/8')
            ]
        )
        carousel_columns.append(carousel_column9)

        carousel_column10 = CarouselColumn(
            thumbnail_image_url='https://g.udn.com.tw/upfiles/B_JO/josh091029/PSN_PHOTO/833/f_27254833_1.JPG',
            title='Fukushimaya Okonomiyaki',
            text='Rich and multi-layered texture with abundant ingredients',
            actions=[
                URIAction(label='Order Link', uri='https://liff.line.me/2000144386-Ax8WZ8k2/en/shop/9')
            ]
        )
        carousel_columns.append(carousel_column10)

    carousel_template = CarouselTemplate(columns=carousel_columns)
    return carousel_template

# 訂餐連結字典
menu_links = {
    0: {
        'zh': 'https://liff.line.me/2000144386-Ax8WZ8k2/zh/shop/0',
        'ja': 'https://liff.line.me/2000144386-Ax8WZ8k2/jp/shop/0',
        'en': 'https://liff.line.me/2000144386-Ax8WZ8k2/en/shop/0'
    },
    1: {
        'zh': 'https://liff.line.me/2000144386-Ax8WZ8k2/zh/shop/1',
        'ja': 'https://liff.line.me/2000144386-Ax8WZ8k2/jp/shop/1',
        'en': 'https://liff.line.me/2000144386-Ax8WZ8k2/en/shop/1'
    },
    2: {
        'zh': 'https://liff.line.me/2000144386-Ax8WZ8k2/zh/shop/2',
        'ja': 'https://liff.line.me/2000144386-Ax8WZ8k2/jp/shop/2',
        'en': 'https://liff.line.me/2000144386-Ax8WZ8k2/en/shop/2'
    },
    3: {
        'zh': 'https://liff.line.me/2000144386-Ax8WZ8k2/zh/shop/3',
        'ja': 'https://liff.line.me/2000144386-Ax8WZ8k2/jp/shop/3',
        'en': 'https://liff.line.me/2000144386-Ax8WZ8k2/en/shop/3'
    },
    4: {
        'zh': 'https://liff.line.me/2000144386-Ax8WZ8k2/zh/shop/4',
        'ja': 'https://liff.line.me/2000144386-Ax8WZ8k2/jp/shop/4',
        'en': 'https://liff.line.me/2000144386-Ax8WZ8k2/en/shop/4'
    },
    5: {
        'zh': 'https://liff.line.me/2000144386-Ax8WZ8k2/zh/shop/5',
        'ja': 'https://liff.line.me/2000144386-Ax8WZ8k2/jp/shop/5',
        'en': 'https://liff.line.me/2000144386-Ax8WZ8k2/en/shop/5'
    },
    6: {
        'zh': 'https://liff.line.me/2000144386-Ax8WZ8k2/zh/shop/6',
        'ja': 'https://liff.line.me/2000144386-Ax8WZ8k2/jp/shop/6',
        'en': 'https://liff.line.me/2000144386-Ax8WZ8k2/en/shop/6'
    },
    7: {
        'zh': 'https://liff.line.me/2000144386-Ax8WZ8k2/zh/shop/7',
        'ja': 'https://liff.line.me/2000144386-Ax8WZ8k2/jp/shop/7',
        'en': 'https://liff.line.me/2000144386-Ax8WZ8k2/en/shop/7'
    },
    8: {
        'zh': 'https://liff.line.me/2000144386-Ax8WZ8k2/zh/shop/8',
        'ja': 'https://liff.line.me/2000144386-Ax8WZ8k2/jp/shop/8',
        'en': 'https://liff.line.me/2000144386-Ax8WZ8k2/en/shop/8'
    },
    9: {
        'zh': 'https://liff.line.me/2000144386-Ax8WZ8k2/zh/shop/9',
        'ja': 'https://liff.line.me/2000144386-Ax8WZ8k2/jp/shop/9',
        'en': 'https://liff.line.me/2000144386-Ax8WZ8k2/en/shop/9'
    },
    None:{
        'zh': '辨識失敗\n請對準招牌再拍一次',
        'ja': '認識失敗です\n看板に合わせてもう一度撮ってみてください',
        'en': 'Recognition failed.\nPlease aim at the signboard and take another shot'
    }

}

#後端連結，可將圖片存到 vm 用 vm 內的模型判斷
url = 'https://backend.locostall.shop/api/predict'

# 處理接收到的訊息事件
@handler.add(MessageEvent, message=ImageMessage)
def handle_image_message(event):
    message_content = line_bot_api.get_message_content(event.message.id)
    with open(event.message.id+'.jpg', 'wb') as fd:
        for chunk in message_content.iter_content():
            fd.write(chunk)
    with open(event.message.id + '.jpg', 'rb') as file:
        files = {'file': file}
        response = requests.post(url, files=files)
        data = response.json()
        object_types = data.get('predicted_class')
        with open("tmp/"+ event.source.user_id + ".txt","r") as f:
            language = f.read()
        link = get_link_by_label_and_language(object_types, language)
        flex_message = create_flex_message(link)
        if object_types is None:
            failed = get_link_by_label_and_language(object_types, language)
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=failed)
        )
        else:
            line_bot_api.reply_message(
            event.reply_token,
            flex_message
        )


def get_link_by_label_and_language(object_types, language):
    if language == "zh":
        menu_link = menu_links.get(object_types, {}).get('zh', '')
        return menu_link
    elif language == "ja":
        menu_link = menu_links.get(object_types, {}).get('ja', '')
        return menu_link
    elif language == "en":
        menu_link = menu_links.get(object_types, {}).get('en', '')
        return menu_link

def create_flex_message(link):
  if link == "https://liff.line.me/2000144386-Ax8WZ8k2/zh/shop/0":
    # Hero Image
    hero_image = ImageComponent(
        url="https://leafyeh.com/wp-content/uploads/flickr/47417246271_9679a79ba4_b.jpg",
        size="full",
        aspect_ratio="20:13",
        aspect_mode="cover"
    )

    # Body Text Components
    title_text = TextComponent(
        text="福州世祖胡椒餅",
        weight="bold",
        size="xl"
    )

    rating_stars = [
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png", size="sm"),
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png", size="sm"),
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png", size="sm"),
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gray_star_28.png", size="sm"),
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gray_star_28.png", size="sm"),
        TextComponent(text="3.5", size="sm", color="#999999", margin="md", flex=0)
    ]
    rating_stars_box = BoxComponent(layout="baseline", margin="md", contents=rating_stars)

    recommended_dish = BoxComponent(
        layout="baseline",
        spacing="sm",
        contents=[
            TextComponent(text="推薦餐點", color="#aaaaaa", size="sm", flex=2),
            TextComponent(text="胡椒餅", wrap=True, color="#666666", size="sm", flex=5)
        ]
    )

    operating_hours = BoxComponent(
        layout="baseline",
        spacing="sm",
        contents=[
            TextComponent(text="營業時間", color="#aaaaaa", size="sm", flex=2),
            TextComponent(text="15:30 - 23:00", wrap=True, color="#666666", size="sm", flex=5)
        ]
    )

    body_contents = [
        title_text,
        rating_stars_box,
        recommended_dish,
        operating_hours
    ]
    body_box = BoxComponent(layout="vertical", contents=body_contents)

    # Footer Button
    website_button = ButtonComponent(
        style="link",
        height="sm",
        action=URIAction(label="菜單", uri=link)
    )
    footer_contents = [website_button]
    footer_box = BoxComponent(layout="vertical", spacing="sm", contents=footer_contents)

    # Bubble Container
    bubble = BubbleContainer(
        body=body_box,
        hero=hero_image,
        footer=footer_box
    )

    # Return the Flex Message
    return FlexSendMessage(alt_text="福州世祖胡椒餅菜單", contents=bubble)

  elif link == "https://liff.line.me/2000144386-Ax8WZ8k2/en/shop/0":
    # Hero Image
    hero_image = ImageComponent(
        url="https://leafyeh.com/wp-content/uploads/flickr/47417246271_9679a79ba4_b.jpg",
        size="full",
        aspect_ratio="20:13",
        aspect_mode="cover"
    )

    # Body Text Components
    title_text = TextComponent(
        text="Fuzhou Black Pepper Bun",
        weight="bold",
        size="xl"
    )

    rating_stars = [
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png", size="sm"),
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png", size="sm"),
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png", size="sm"),
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gray_star_28.png", size="sm"),
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gray_star_28.png", size="sm"),
        TextComponent(text="3.5", size="sm", color="#999999", margin="md", flex=0)
    ]
    rating_stars_box = BoxComponent(layout="baseline", margin="md", contents=rating_stars)

    recommended_dish = BoxComponent(
        layout="baseline",
        spacing="sm",
        contents=[
            TextComponent(text="Best Items", color="#aaaaaa", size="sm", flex=2),
            TextComponent(text="Pepper Bun", wrap=True, color="#666666", size="sm", flex=5)
        ]
    )

    operating_hours = BoxComponent(
        layout="baseline",
        spacing="sm",
        contents=[
            TextComponent(text="Hours", color="#aaaaaa", size="sm", flex=2),
            TextComponent(text="15:30 - 23:00", wrap=True, color="#666666", size="sm", flex=5)
        ]
    )

    body_contents = [
        title_text,
        rating_stars_box,
        recommended_dish,
        operating_hours
    ]
    body_box = BoxComponent(layout="vertical", contents=body_contents)

    # Footer Button
    website_button = ButtonComponent(
        style="link",
        height="sm",
        action=URIAction(label="Menu", uri=link)
    )
    footer_contents = [website_button]
    footer_box = BoxComponent(layout="vertical", spacing="sm", contents=footer_contents)

    # Bubble Container
    bubble = BubbleContainer(
        body=body_box,
        hero=hero_image,
        footer=footer_box
    )

    # Return the Flex Message
    return FlexSendMessage(alt_text="Fuzhou Black Pepper Bun Menu", contents=bubble)

  elif link == "https://liff.line.me/2000144386-Ax8WZ8k2/jp/shop/0":
    # Hero Image
    hero_image = ImageComponent(
        url="https://leafyeh.com/wp-content/uploads/flickr/47417246271_9679a79ba4_b.jpg",
        size="full",
        aspect_ratio="20:13",
        aspect_mode="cover"
    )

    # Body Text Components
    title_text = TextComponent(
        text="福州世祖胡椒餅",
        weight="bold",
        size="xl"
    )

    rating_stars = [
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png", size="sm"),
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png", size="sm"),
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png", size="sm"),
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gray_star_28.png", size="sm"),
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gray_star_28.png", size="sm"),
        TextComponent(text="3.5", size="sm", color="#999999", margin="md", flex=0)
    ]
    rating_stars_box = BoxComponent(layout="baseline", margin="md", contents=rating_stars)

    recommended_dish = BoxComponent(
        layout="baseline",
        spacing="sm",
        contents=[
            TextComponent(text="おすすめ", color="#aaaaaa", size="sm", flex=2),
            TextComponent(text="胡椒餅", wrap=True, color="#666666", size="sm", flex=5)
        ]
    )

    operating_hours = BoxComponent(
        layout="baseline",
        spacing="sm",
        contents=[
            TextComponent(text="営業時間", color="#aaaaaa", size="sm", flex=2),
            TextComponent(text="15:30 - 23:00", wrap=True, color="#666666", size="sm", flex=5)
        ]
    )

    body_contents = [
        title_text,
        rating_stars_box,
        recommended_dish,
        operating_hours
    ]
    body_box = BoxComponent(layout="vertical", contents=body_contents)

    # Footer Button
    website_button = ButtonComponent(
        style="link",
        height="sm",
        action=URIAction(label="メニュー", uri=link)
    )
    footer_contents = [website_button]
    footer_box = BoxComponent(layout="vertical", spacing="sm", contents=footer_contents)

    # Bubble Container
    bubble = BubbleContainer(
        body=body_box,
        hero=hero_image,
        footer=footer_box
    )

    # Return the Flex Message
    return FlexSendMessage(alt_text="福州世祖胡椒餅メニュー", contents=bubble)

  elif link == "https://liff.line.me/2000144386-Ax8WZ8k2/zh/shop/1":
    # Hero Image
    hero_image = ImageComponent(
        url="https://cdn2.ettoday.net/images/6280/d6280464.jpg",
        size="full",
        aspect_ratio="20:13",
        aspect_mode="cover"
    )

    # Body Text Components
    title_text = TextComponent(
        text="老芋仔芋頭酥",
        weight="bold",
        size="xl"
    )

    rating_stars = [
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png", size="sm"),
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png", size="sm"),
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png", size="sm"),
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png", size="sm"),
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gray_star_28.png", size="sm"),
        TextComponent(text="4.3", size="sm", color="#999999", margin="md", flex=0)
    ]
    rating_stars_box = BoxComponent(layout="baseline", margin="md", contents=rating_stars)

    recommended_dish = BoxComponent(
        layout="baseline",
        spacing="sm",
        contents=[
            TextComponent(text="推薦餐點", color="#aaaaaa", size="sm", flex=2),
            TextComponent(text="芋頭酥", wrap=True, color="#666666", size="sm", flex=5)
        ]
    )

    operating_hours = BoxComponent(
        layout="baseline",
        spacing="sm",
        contents=[
            TextComponent(text="營業時間", color="#aaaaaa", size="sm", flex=2),
            TextComponent(text="17:20 - 23:00", wrap=True, color="#666666", size="sm", flex=5)
        ]
    )

    body_contents = [
        title_text,
        rating_stars_box,
        recommended_dish,
        operating_hours
    ]
    body_box = BoxComponent(layout="vertical", contents=body_contents)

    # Footer Button
    website_button = ButtonComponent(
        style="link",
        height="sm",
        action=URIAction(label="菜單", uri=link)
    )
    footer_contents = [website_button]
    footer_box = BoxComponent(layout="vertical", spacing="sm", contents=footer_contents)

    # Bubble Container
    bubble = BubbleContainer(
        body=body_box,
        hero=hero_image,
        footer=footer_box
    )

    # Return the Flex Message
    return FlexSendMessage(alt_text="老芋仔芋頭酥菜單", contents=bubble)

  elif link == "https://liff.line.me/2000144386-Ax8WZ8k2/en/shop/1":
    # Hero Image
    hero_image = ImageComponent(
        url="https://cdn2.ettoday.net/images/6280/d6280464.jpg",
        size="full",
        aspect_ratio="20:13",
        aspect_mode="cover"
    )

    # Body Text Components
    title_text = TextComponent(
        text="Taro Pastry",
        weight="bold",
        size="xl"
    )

    rating_stars = [
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png", size="sm"),
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png", size="sm"),
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png", size="sm"),
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png", size="sm"),
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gray_star_28.png", size="sm"),
        TextComponent(text="4.3", size="sm", color="#999999", margin="md", flex=0)
    ]
    rating_stars_box = BoxComponent(layout="baseline", margin="md", contents=rating_stars)

    recommended_dish = BoxComponent(
        layout="baseline",
        spacing="sm",
        contents=[
            TextComponent(text="Best Items", color="#aaaaaa", size="sm", flex=2),
            TextComponent(text="Taro Ball", wrap=True, color="#666666", size="sm", flex=5)
        ]
    )

    operating_hours = BoxComponent(
        layout="baseline",
        spacing="sm",
        contents=[
            TextComponent(text="Hours", color="#aaaaaa", size="sm", flex=2),
            TextComponent(text="17:20 - 23:00", wrap=True, color="#666666", size="sm", flex=5)
        ]
    )

    body_contents = [
        title_text,
        rating_stars_box,
        recommended_dish,
        operating_hours
    ]
    body_box = BoxComponent(layout="vertical", contents=body_contents)

    # Footer Button
    website_button = ButtonComponent(
        style="link",
        height="sm",
        action=URIAction(label="Menu", uri=link)
    )
    footer_contents = [website_button]
    footer_box = BoxComponent(layout="vertical", spacing="sm", contents=footer_contents)

    # Bubble Container
    bubble = BubbleContainer(
        body=body_box,
        hero=hero_image,
        footer=footer_box
    )

    # Return the Flex Message
    return FlexSendMessage(alt_text="Taro Pastry Menu", contents=bubble)

  elif link == "https://liff.line.me/2000144386-Ax8WZ8k2/jp/shop/1":
    # Hero Image
    hero_image = ImageComponent(
        url="https://cdn2.ettoday.net/images/6280/d6280464.jpg",
        size="full",
        aspect_ratio="20:13",
        aspect_mode="cover"
    )

    # Body Text Components
    title_text = TextComponent(
        text="老芋仔タロイモペイストリー",
        weight="bold",
        size="xl"
    )

    rating_stars = [
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png", size="sm"),
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png", size="sm"),
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png", size="sm"),
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png", size="sm"),
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gray_star_28.png", size="sm"),
        TextComponent(text="4.3", size="sm", color="#999999", margin="md", flex=0)
    ]
    rating_stars_box = BoxComponent(layout="baseline", margin="md", contents=rating_stars)

    recommended_dish = BoxComponent(
        layout="baseline",
        spacing="sm",
        contents=[
            TextComponent(text="おすすめ", color="#aaaaaa", size="sm", flex=2),
            TextComponent(text="タロイモペイストリー", wrap=True, color="#666666", size="sm", flex=5)
        ]
    )

    operating_hours = BoxComponent(
        layout="baseline",
        spacing="sm",
        contents=[
            TextComponent(text="営業時間", color="#aaaaaa", size="sm", flex=2),
            TextComponent(text="17:20 - 23:00", wrap=True, color="#666666", size="sm", flex=5)
        ]
    )

    body_contents = [
        title_text,
        rating_stars_box,
        recommended_dish,
        operating_hours
    ]
    body_box = BoxComponent(layout="vertical", contents=body_contents)

    # Footer Button
    website_button = ButtonComponent(
        style="link",
        height="sm",
        action=URIAction(label="メニュー", uri=link)
    )
    footer_contents = [website_button]
    footer_box = BoxComponent(layout="vertical", spacing="sm", contents=footer_contents)

    # Bubble Container
    bubble = BubbleContainer(
        body=body_box,
        hero=hero_image,
        footer=footer_box
    )

    # Return the Flex Message
    return FlexSendMessage(alt_text="老芋仔タロイモペイストリーメニュー", contents=bubble)
  
  elif link == "https://liff.line.me/2000144386-Ax8WZ8k2/zh/shop/2":
    # Hero Image
    hero_image = ImageComponent(
        url="https://ak-d.tripcdn.com/images/100s0z000000n2at66F03.jpg",
        size="full",
        aspect_ratio="20:13",
        aspect_mode="cover"
    )

    # Body Text Components
    title_text = TextComponent(
        text="施老闆麻辣臭豆腐",
        weight="bold",
        size="xl"
    )

    rating_stars = [
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png", size="sm"),
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png", size="sm"),
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gray_star_28.png", size="sm"),
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gray_star_28.png", size="sm"),
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gray_star_28.png", size="sm"),
        TextComponent(text="2.4", size="sm", color="#999999", margin="md", flex=0)
    ]
    rating_stars_box = BoxComponent(layout="baseline", margin="md", contents=rating_stars)

    recommended_dish = BoxComponent(
        layout="baseline",
        spacing="sm",
        contents=[
            TextComponent(text="推薦餐點", color="#aaaaaa", size="sm", flex=2),
            TextComponent(text="臭豆腐、鴨血", wrap=True, color="#666666", size="sm", flex=5)
        ]
    )

    operating_hours = BoxComponent(
        layout="baseline",
        spacing="sm",
        contents=[
            TextComponent(text="營業時間", color="#aaaaaa", size="sm", flex=2),
            TextComponent(text="16:30 - 22:00", wrap=True, color="#666666", size="sm", flex=5)
        ]
    )

    body_contents = [
        title_text,
        rating_stars_box,
        recommended_dish,
        operating_hours
    ]
    body_box = BoxComponent(layout="vertical", contents=body_contents)

    # Footer Button
    website_button = ButtonComponent(
        style="link",
        height="sm",
        action=URIAction(label="菜單", uri=link)
    )
    footer_contents = [website_button]
    footer_box = BoxComponent(layout="vertical", spacing="sm", contents=footer_contents)

    # Bubble Container
    bubble = BubbleContainer(
        body=body_box,
        hero=hero_image,
        footer=footer_box
    )

    # Return the Flex Message
    return FlexSendMessage(alt_text="施老闆麻辣臭豆腐菜單", contents=bubble)

  elif link == "https://liff.line.me/2000144386-Ax8WZ8k2/en/shop/2":
    # Hero Image
    hero_image = ImageComponent(
        url="https://ak-d.tripcdn.com/images/100s0z000000n2at66F03.jpg",
        size="full",
        aspect_ratio="20:13",
        aspect_mode="cover"
    )

    # Body Text Components
    title_text = TextComponent(
        text="Mr. Shi's Spicy Stinky Tofu",
        weight="bold",
        size="xl"
    )

    rating_stars = [
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png", size="sm"),
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png", size="sm"),
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gray_star_28.png", size="sm"),
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gray_star_28.png", size="sm"),
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gray_star_28.png", size="sm"),
        TextComponent(text="2.4", size="sm", color="#999999", margin="md", flex=0)
    ]
    rating_stars_box = BoxComponent(layout="baseline", margin="md", contents=rating_stars)

    recommended_dish = BoxComponent(
        layout="baseline",
        spacing="sm",
        contents=[
            TextComponent(text="Best Items", color="#aaaaaa", size="sm", flex=2),
            TextComponent(text="Spicy Stinky Tofu", wrap=True, color="#666666", size="sm", flex=5)
        ]
    )

    operating_hours = BoxComponent(
        layout="baseline",
        spacing="sm",
        contents=[
            TextComponent(text="Hours", color="#aaaaaa", size="sm", flex=2),
            TextComponent(text="16:30 - 22:00", wrap=True, color="#666666", size="sm", flex=5)
        ]
    )

    body_contents = [
        title_text,
        rating_stars_box,
        recommended_dish,
        operating_hours
    ]
    body_box = BoxComponent(layout="vertical", contents=body_contents)

    # Footer Button
    website_button = ButtonComponent(
        style="link",
        height="sm",
        action=URIAction(label="Menu", uri=link)
    )
    footer_contents = [website_button]
    footer_box = BoxComponent(layout="vertical", spacing="sm", contents=footer_contents)

    # Bubble Container
    bubble = BubbleContainer(
        body=body_box,
        hero=hero_image,
        footer=footer_box
    )

    # Return the Flex Message
    return FlexSendMessage(alt_text="Mr. Shi's Spicy Stinky Tofu Menu", contents=bubble)

  elif link == "https://liff.line.me/2000144386-Ax8WZ8k2/jp/shop/2":
    # Hero Image
    hero_image = ImageComponent(
        url="https://ak-d.tripcdn.com/images/100s0z000000n2at66F03.jpg",
        size="full",
        aspect_ratio="20:13",
        aspect_mode="cover"
    )

    # Body Text Components
    title_text = TextComponent(
        text="施老板臭豆腐",
        weight="bold",
        size="xl"
    )

    rating_stars = [
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png", size="sm"),
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png", size="sm"),
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gray_star_28.png", size="sm"),
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gray_star_28.png", size="sm"),
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gray_star_28.png", size="sm"),
        TextComponent(text="2.4", size="sm", color="#999999", margin="md", flex=0)
    ]
    rating_stars_box = BoxComponent(layout="baseline", margin="md", contents=rating_stars)

    recommended_dish = BoxComponent(
        layout="baseline",
        spacing="sm",
        contents=[
            TextComponent(text="おすすめ", color="#aaaaaa", size="sm", flex=2),
            TextComponent(text="ば辛くて香ばしい臭豆腐", wrap=True, color="#666666", size="sm", flex=5)
        ]
    )

    operating_hours = BoxComponent(
        layout="baseline",
        spacing="sm",
        contents=[
            TextComponent(text="営業時間", color="#aaaaaa", size="sm", flex=2),
            TextComponent(text="16:30 - 22:00", wrap=True, color="#666666", size="sm", flex=5)
        ]
    )

    body_contents = [
        title_text,
        rating_stars_box,
        recommended_dish,
        operating_hours
    ]
    body_box = BoxComponent(layout="vertical", contents=body_contents)

    # Footer Button
    website_button = ButtonComponent(
        style="link",
        height="sm",
        action=URIAction(label="メニュー", uri=link)
    )
    footer_contents = [website_button]
    footer_box = BoxComponent(layout="vertical", spacing="sm", contents=footer_contents)

    # Bubble Container
    bubble = BubbleContainer(
        body=body_box,
        hero=hero_image,
        footer=footer_box
    )

    # Return the Flex Message
    return FlexSendMessage(alt_text="施老板臭豆腐メニュー", contents=bubble)

  elif link == "https://liff.line.me/2000144386-Ax8WZ8k2/zh/shop/3":
    # Hero Image
    hero_image = ImageComponent(
        url="https://lordcat.tw/wp-content/uploads/2022/04/1651325631-1622d5c737a238168a234103228b3e2d.jpg",
        size="full",
        aspect_ratio="20:13",
        aspect_mode="cover"
    )

    # Body Text Components
    title_text = TextComponent(
        text="下港名彭臭豆腐",
        weight="bold",
        size="xl"
    )

    rating_stars = [
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png", size="sm"),
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png", size="sm"),
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png", size="sm"),
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gray_star_28.png", size="sm"),
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gray_star_28.png", size="sm"),
        TextComponent(text="3.2", size="sm", color="#999999", margin="md", flex=0)
    ]
    rating_stars_box = BoxComponent(layout="baseline", margin="md", contents=rating_stars)

    recommended_dish = BoxComponent(
        layout="baseline",
        spacing="sm",
        contents=[
            TextComponent(text="推薦餐點", color="#aaaaaa", size="sm", flex=2),
            TextComponent(text="蚵仔煎、脆皮臭豆腐", wrap=True, color="#666666", size="sm", flex=5)
        ]
    )

    operating_hours = BoxComponent(
        layout="baseline",
        spacing="sm",
        contents=[
            TextComponent(text="營業時間", color="#aaaaaa", size="sm", flex=2),
            TextComponent(text="18:00 - 23:00", wrap=True, color="#666666", size="sm", flex=5)
        ]
    )

    body_contents = [
        title_text,
        rating_stars_box,
        recommended_dish,
        operating_hours
    ]
    body_box = BoxComponent(layout="vertical", contents=body_contents)

    # Footer Button
    website_button = ButtonComponent(
        style="link",
        height="sm",
        action=URIAction(label="菜單", uri=link)
    )
    footer_contents = [website_button]
    footer_box = BoxComponent(layout="vertical", spacing="sm", contents=footer_contents)

    # Bubble Container
    bubble = BubbleContainer(
        body=body_box,
        hero=hero_image,
        footer=footer_box
    )

    # Return the Flex Message
    return FlexSendMessage(alt_text="下港名彭臭豆腐菜單", contents=bubble)

  elif link == "https://liff.line.me/2000144386-Ax8WZ8k2/en/shop/3":
    # Hero Image
    hero_image = ImageComponent(
        url="https://lordcat.tw/wp-content/uploads/2022/04/1651325631-1622d5c737a238168a234103228b3e2d.jpg",
        size="full",
        aspect_ratio="20:13",
        aspect_mode="cover"
    )

    # Body Text Components
    title_text = TextComponent(
        text="Pengxiagang Stinky Tofu",
        weight="bold",
        size="xl"
    )

    rating_stars = [
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png", size="sm"),
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png", size="sm"),
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png", size="sm"),
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gray_star_28.png", size="sm"),
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gray_star_28.png", size="sm"),
        TextComponent(text="3.2", size="sm", color="#999999", margin="md", flex=0)
    ]
    rating_stars_box = BoxComponent(layout="baseline", margin="md", contents=rating_stars)

    recommended_dish = BoxComponent(
        layout="baseline",
        spacing="sm",
        contents=[
            TextComponent(text="Best Items", color="#aaaaaa", size="sm", flex=2),
            TextComponent(text="Stinky Tofu, Oyster Omelette", wrap=True, color="#666666", size="sm", flex=5)
        ]
    )

    operating_hours = BoxComponent(
        layout="baseline",
        spacing="sm",
        contents=[
            TextComponent(text="Hours", color="#aaaaaa", size="sm", flex=2),
            TextComponent(text="18:00 - 23:00", wrap=True, color="#666666", size="sm", flex=5)
        ]
    )

    body_contents = [
        title_text,
        rating_stars_box,
        recommended_dish,
        operating_hours
    ]
    body_box = BoxComponent(layout="vertical", contents=body_contents)

    # Footer Button
    website_button = ButtonComponent(
        style="link",
        height="sm",
        action=URIAction(label="Menu", uri=link)
    )
    footer_contents = [website_button]
    footer_box = BoxComponent(layout="vertical", spacing="sm", contents=footer_contents)

    # Bubble Container
    bubble = BubbleContainer(
        body=body_box,
        hero=hero_image,
        footer=footer_box
    )

    # Return the Flex Message
    return FlexSendMessage(alt_text="Pengxiagang Stinky Tofu Menu", contents=bubble)

  elif link == "https://liff.line.me/2000144386-Ax8WZ8k2/jp/shop/3":
    # Hero Image
    hero_image = ImageComponent(
        url="https://lordcat.tw/wp-content/uploads/2022/04/1651325631-1622d5c737a238168a234103228b3e2d.jpg",
        size="full",
        aspect_ratio="20:13",
        aspect_mode="cover"
    )

    # Body Text Components
    title_text = TextComponent(
        text="下港名彭臭豆腐",
        weight="bold",
        size="xl"
    )

    rating_stars = [
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png", size="sm"),
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png", size="sm"),
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png", size="sm"),
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gray_star_28.png", size="sm"),
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gray_star_28.png", size="sm"),
        TextComponent(text="3.2", size="sm", color="#999999", margin="md", flex=0)
    ]
    rating_stars_box = BoxComponent(layout="baseline", margin="md", contents=rating_stars)

    recommended_dish = BoxComponent(
        layout="baseline",
        spacing="sm",
        contents=[
            TextComponent(text="おすすめ", color="#aaaaaa", size="sm", flex=2),
            TextComponent(text="臭豆腐 牡蠣オムレツ", wrap=True, color="#666666", size="sm", flex=5)
        ]
    )

    operating_hours = BoxComponent(
        layout="baseline",
        spacing="sm",
        contents=[
            TextComponent(text="営業時間", color="#aaaaaa", size="sm", flex=2),
            TextComponent(text="18:00 - 23:00", wrap=True, color="#666666", size="sm", flex=5)
        ]
    )

    body_contents = [
        title_text,
        rating_stars_box,
        recommended_dish,
        operating_hours
    ]
    body_box = BoxComponent(layout="vertical", contents=body_contents)

    # Footer Button
    website_button = ButtonComponent(
        style="link",
        height="sm",
        action=URIAction(label="メニュー", uri=link)
    )
    footer_contents = [website_button]
    footer_box = BoxComponent(layout="vertical", spacing="sm", contents=footer_contents)

    # Bubble Container
    bubble = BubbleContainer(
        body=body_box,
        hero=hero_image,
        footer=footer_box
    )

    # Return the Flex Message
    return FlexSendMessage(alt_text="下港名彭臭豆腐メニュー", contents=bubble)

  elif link == "https://liff.line.me/2000144386-Ax8WZ8k2/zh/shop/4":
    # Hero Image
    hero_image = ImageComponent(
        url="https://lordcat.tw/wp-content/uploads/2019/04/1652191927-fecf413191371cf259cfb131a00c24b6.jpg",
        size="full",
        aspect_ratio="20:13",
        aspect_mode="cover"
    )

    # Body Text Components
    title_text = TextComponent(
        text="阿國滷味",
        weight="bold",
        size="xl"
    )

    rating_stars = [
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png", size="sm"),
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png", size="sm"),
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png", size="sm"),
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gray_star_28.png", size="sm"),
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gray_star_28.png", size="sm"),
        TextComponent(text="3.6", size="sm", color="#999999", margin="md", flex=0)
    ]
    rating_stars_box = BoxComponent(layout="baseline", margin="md", contents=rating_stars)

    recommended_dish = BoxComponent(
        layout="baseline",
        spacing="sm",
        contents=[
            TextComponent(text="推薦餐點", color="#aaaaaa", size="sm", flex=2),
            TextComponent(text="鴨翅、脆腸", wrap=True, color="#666666", size="sm", flex=5)
        ]
    )

    operating_hours = BoxComponent(
        layout="baseline",
        spacing="sm",
        contents=[
            TextComponent(text="營業時間", color="#aaaaaa", size="sm", flex=2),
            TextComponent(text="16:30 - 23:30", wrap=True, color="#666666", size="sm", flex=5)
        ]
    )

    body_contents = [
        title_text,
        rating_stars_box,
        recommended_dish,
        operating_hours
    ]
    body_box = BoxComponent(layout="vertical", contents=body_contents)

    # Footer Button
    website_button = ButtonComponent(
        style="link",
        height="sm",
        action=URIAction(label="菜單", uri=link)
    )
    footer_contents = [website_button]
    footer_box = BoxComponent(layout="vertical", spacing="sm", contents=footer_contents)

    # Bubble Container
    bubble = BubbleContainer(
        body=body_box,
        hero=hero_image,
        footer=footer_box
    )

    # Return the Flex Message
    return FlexSendMessage(alt_text="阿國滷味菜單", contents=bubble)

  elif link == "https://liff.line.me/2000144386-Ax8WZ8k2/en/shop/4":
    # Hero Image
    hero_image = ImageComponent(
        url="https://lordcat.tw/wp-content/uploads/2019/04/1652191927-fecf413191371cf259cfb131a00c24b6.jpg",
        size="full",
        aspect_ratio="20:13",
        aspect_mode="cover"
    )

    # Body Text Components
    title_text = TextComponent(
        text="Ah Guo Braised Dish",
        weight="bold",
        size="xl"
    )

    rating_stars = [
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png", size="sm"),
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png", size="sm"),
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png", size="sm"),
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gray_star_28.png", size="sm"),
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gray_star_28.png", size="sm"),
        TextComponent(text="3.6", size="sm", color="#999999", margin="md", flex=0)
    ]
    rating_stars_box = BoxComponent(layout="baseline", margin="md", contents=rating_stars)

    recommended_dish = BoxComponent(
        layout="baseline",
        spacing="sm",
        contents=[
            TextComponent(text="Best Items", color="#aaaaaa", size="sm", flex=2),
            TextComponent(text="Duck Wings, Duck Tendon", wrap=True, color="#666666", size="sm", flex=5)
        ]
    )

    operating_hours = BoxComponent(
        layout="baseline",
        spacing="sm",
        contents=[
            TextComponent(text="Hours", color="#aaaaaa", size="sm", flex=2),
            TextComponent(text="16:30 - 23:30", wrap=True, color="#666666", size="sm", flex=5)
        ]
    )

    body_contents = [
        title_text,
        rating_stars_box,
        recommended_dish,
        operating_hours
    ]
    body_box = BoxComponent(layout="vertical", contents=body_contents)

    # Footer Button
    website_button = ButtonComponent(
        style="link",
        height="sm",
        action=URIAction(label="Menu", uri=link)
    )
    footer_contents = [website_button]
    footer_box = BoxComponent(layout="vertical", spacing="sm", contents=footer_contents)

    # Bubble Container
    bubble = BubbleContainer(
        body=body_box,
        hero=hero_image,
        footer=footer_box
    )

    # Return the Flex Message
    return FlexSendMessage(alt_text="Ah Guo Braised Dish Menu", contents=bubble)

  elif link == "https://liff.line.me/2000144386-Ax8WZ8k2/jp/shop/4":
    # Hero Image
    hero_image = ImageComponent(
        url="https://lordcat.tw/wp-content/uploads/2019/04/1652191927-fecf413191371cf259cfb131a00c24b6.jpg",
        size="full",
        aspect_ratio="20:13",
        aspect_mode="cover"
    )

    # Body Text Components
    title_text = TextComponent(
        text="阿國滷味",
        weight="bold",
        size="xl"
    )

    rating_stars = [
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png", size="sm"),
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png", size="sm"),
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png", size="sm"),
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gray_star_28.png", size="sm"),
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gray_star_28.png", size="sm"),
        TextComponent(text="3.6", size="sm", color="#999999", margin="md", flex=0)
    ]
    rating_stars_box = BoxComponent(layout="baseline", margin="md", contents=rating_stars)

    recommended_dish = BoxComponent(
        layout="baseline",
        spacing="sm",
        contents=[
            TextComponent(text="おすすめ", color="#aaaaaa", size="sm", flex=2),
            TextComponent(text="アヒルの手羽先 すじ", wrap=True, color="#666666", size="sm", flex=5)
        ]
    )

    operating_hours = BoxComponent(
        layout="baseline",
        spacing="sm",
        contents=[
            TextComponent(text="営業時間", color="#aaaaaa", size="sm", flex=2),
            TextComponent(text="16:30 - 23:30", wrap=True, color="#666666", size="sm", flex=5)
        ]
    )

    body_contents = [
        title_text,
        rating_stars_box,
        recommended_dish,
        operating_hours
    ]
    body_box = BoxComponent(layout="vertical", contents=body_contents)

    # Footer Button
    website_button = ButtonComponent(
        style="link",
        height="sm",
        action=URIAction(label="メニュー", uri=link)
    )
    footer_contents = [website_button]
    footer_box = BoxComponent(layout="vertical", spacing="sm", contents=footer_contents)

    # Bubble Container
    bubble = BubbleContainer(
        body=body_box,
        hero=hero_image,
        footer=footer_box
    )

    # Return the Flex Message
    return FlexSendMessage(alt_text="阿國滷味メニュー", contents=bubble)

  elif link == "https://liff.line.me/2000144386-Ax8WZ8k2/zh/shop/5":
    # Hero Image
    hero_image = ImageComponent(
        url="https://lordcat.tw/wp-content/uploads/2016/08/1652285181-0d3e4265b5fcf5f82d5add629469f506.jpg",
        size="full",
        aspect_ratio="20:13",
        aspect_mode="cover"
    )

    # Body Text Components
    title_text = TextComponent(
        text="連家清燉豬腳",
        weight="bold",
        size="xl"
    )

    rating_stars = [
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png", size="sm"),
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png", size="sm"),
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png", size="sm"),
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gray_star_28.png", size="sm"),
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gray_star_28.png", size="sm"),
        TextComponent(text="3.1", size="sm", color="#999999", margin="md", flex=0)
    ]
    rating_stars_box = BoxComponent(layout="baseline", margin="md", contents=rating_stars)

    recommended_dish = BoxComponent(
        layout="baseline",
        spacing="sm",
        contents=[
            TextComponent(text="推薦餐點", color="#aaaaaa", size="sm", flex=2),
            TextComponent(text="豬腳", wrap=True, color="#666666", size="sm", flex=5)
        ]
    )

    operating_hours = BoxComponent(
        layout="baseline",
        spacing="sm",
        contents=[
            TextComponent(text="營業時間", color="#aaaaaa", size="sm", flex=2),
            TextComponent(text="17:00 - 00:00", wrap=True, color="#666666", size="sm", flex=5)
        ]
    )

    body_contents = [
        title_text,
        rating_stars_box,
        recommended_dish,
        operating_hours
    ]
    body_box = BoxComponent(layout="vertical", contents=body_contents)

    # Footer Button
    website_button = ButtonComponent(
        style="link",
        height="sm",
        action=URIAction(label="菜單", uri=link)
    )
    footer_contents = [website_button]
    footer_box = BoxComponent(layout="vertical", spacing="sm", contents=footer_contents)

    # Bubble Container
    bubble = BubbleContainer(
        body=body_box,
        hero=hero_image,
        footer=footer_box
    )

    # Return the Flex Message
    return FlexSendMessage(alt_text="連家清燉豬腳菜單", contents=bubble)

  elif link == "https://liff.line.me/2000144386-Ax8WZ8k2/en/shop/5":
    # Hero Image
    hero_image = ImageComponent(
        url="https://lordcat.tw/wp-content/uploads/2016/08/1652285181-0d3e4265b5fcf5f82d5add629469f506.jpg",
        size="full",
        aspect_ratio="20:13",
        aspect_mode="cover"
    )

    # Body Text Components
    title_text = TextComponent(
        text="Lian\'s Stewed Pig Knuckle",
        weight="bold",
        size="xl"
    )

    rating_stars = [
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png", size="sm"),
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png", size="sm"),
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png", size="sm"),
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gray_star_28.png", size="sm"),
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gray_star_28.png", size="sm"),
        TextComponent(text="3.1", size="sm", color="#999999", margin="md", flex=0)
    ]
    rating_stars_box = BoxComponent(layout="baseline", margin="md", contents=rating_stars)

    recommended_dish = BoxComponent(
        layout="baseline",
        spacing="sm",
        contents=[
            TextComponent(text="Best Items", color="#aaaaaa", size="sm", flex=2),
            TextComponent(text="Stewed Pig Knuckle", wrap=True, color="#666666", size="sm", flex=5)
        ]
    )

    operating_hours = BoxComponent(
        layout="baseline",
        spacing="sm",
        contents=[
            TextComponent(text="Hours", color="#aaaaaa", size="sm", flex=2),
            TextComponent(text="17:00 - 00:00", wrap=True, color="#666666", size="sm", flex=5)
        ]
    )

    body_contents = [
        title_text,
        rating_stars_box,
        recommended_dish,
        operating_hours
    ]
    body_box = BoxComponent(layout="vertical", contents=body_contents)

    # Footer Button
    website_button = ButtonComponent(
        style="link",
        height="sm",
        action=URIAction(label="Menu", uri=link)
    )
    footer_contents = [website_button]
    footer_box = BoxComponent(layout="vertical", spacing="sm", contents=footer_contents)

    # Bubble Container
    bubble = BubbleContainer(
        body=body_box,
        hero=hero_image,
        footer=footer_box
    )

    # Return the Flex Message
    return FlexSendMessage(alt_text="Lian\'s Stewed Pig Knuckle Menu", contents=bubble)

  elif link == "https://liff.line.me/2000144386-Ax8WZ8k2/jp/shop/5":
    # Hero Image
    hero_image = ImageComponent(
        url="https://lordcat.tw/wp-content/uploads/2016/08/1652285181-0d3e4265b5fcf5f82d5add629469f506.jpg",
        size="full",
        aspect_ratio="20:13",
        aspect_mode="cover"
    )

    # Body Text Components
    title_text = TextComponent(
        text="連家豚足のクリアースープ",
        weight="bold",
        size="xl"
    )

    rating_stars = [
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png", size="sm"),
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png", size="sm"),
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png", size="sm"),
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gray_star_28.png", size="sm"),
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gray_star_28.png", size="sm"),
        TextComponent(text="3.1", size="sm", color="#999999", margin="md", flex=0)
    ]
    rating_stars_box = BoxComponent(layout="baseline", margin="md", contents=rating_stars)

    recommended_dish = BoxComponent(
        layout="baseline",
        spacing="sm",
        contents=[
            TextComponent(text="おすすめ", color="#aaaaaa", size="sm", flex=2),
            TextComponent(text="豚足のクリアースープ", wrap=True, color="#666666", size="sm", flex=5)
        ]
    )

    operating_hours = BoxComponent(
        layout="baseline",
        spacing="sm",
        contents=[
            TextComponent(text="営業時間", color="#aaaaaa", size="sm", flex=2),
            TextComponent(text="17:00 - 00:00", wrap=True, color="#666666", size="sm", flex=5)
        ]
    )

    body_contents = [
        title_text,
        rating_stars_box,
        recommended_dish,
        operating_hours
    ]
    body_box = BoxComponent(layout="vertical", contents=body_contents)

    # Footer Button
    website_button = ButtonComponent(
        style="link",
        height="sm",
        action=URIAction(label="メニュー", uri=link)
    )
    footer_contents = [website_button]
    footer_box = BoxComponent(layout="vertical", spacing="sm", contents=footer_contents)

    # Bubble Container
    bubble = BubbleContainer(
        body=body_box,
        hero=hero_image,
        footer=footer_box
    )

    # Return the Flex Message
    return FlexSendMessage(alt_text="連家豚足のクリアースープメニュー", contents=bubble)

  elif link == "https://liff.line.me/2000144386-Ax8WZ8k2/zh/shop/6":
    # Hero Image
    hero_image = ImageComponent(
        url="https://lh3.googleusercontent.com/xnzWNm7IiHeveS1grP5p_YZs9N_jfaJTiT0cakJSQqLwMgJlU-DD31ZzGHOYXTwZ_IWllGQ_N9QusU15oUiILW7dtOsrxp3Gj-jcM8styxDS8Q=s600",
        size="full",
        aspect_ratio="20:13",
        aspect_mode="cover"
    )

    # Body Text Components
    title_text = TextComponent(
        text="古早味寶寶麻糬",
        weight="bold",
        size="xl"
    )

    rating_stars = [
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png", size="sm"),
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png", size="sm"),
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png", size="sm"),
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png", size="sm"),
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gray_star_28.png", size="sm"),
        TextComponent(text="4.8", size="sm", color="#999999", margin="md", flex=0)
    ]
    rating_stars_box = BoxComponent(layout="baseline", margin="md", contents=rating_stars)

    recommended_dish = BoxComponent(
        layout="baseline",
        spacing="sm",
        contents=[
            TextComponent(text="推薦餐點", color="#aaaaaa", size="sm", flex=2),
            TextComponent(text="麻糬、菜燕", wrap=True, color="#666666", size="sm", flex=5)
        ]
    )

    operating_hours = BoxComponent(
        layout="baseline",
        spacing="sm",
        contents=[
            TextComponent(text="營業時間", color="#aaaaaa", size="sm", flex=2),
            TextComponent(text="17:00 - 23:30", wrap=True, color="#666666", size="sm", flex=5)
        ]
    )

    body_contents = [
        title_text,
        rating_stars_box,
        recommended_dish,
        operating_hours
    ]
    body_box = BoxComponent(layout="vertical", contents=body_contents)

    # Footer Button
    website_button = ButtonComponent(
        style="link",
        height="sm",
        action=URIAction(label="菜單", uri=link)
    )
    footer_contents = [website_button]
    footer_box = BoxComponent(layout="vertical", spacing="sm", contents=footer_contents)

    # Bubble Container
    bubble = BubbleContainer(
        body=body_box,
        hero=hero_image,
        footer=footer_box
    )

    # Return the Flex Message
    return FlexSendMessage(alt_text="古早味寶寶麻糬菜單", contents=bubble)

  elif link == "https://liff.line.me/2000144386-Ax8WZ8k2/en/shop/6":
    # Hero Image
    hero_image = ImageComponent(
        url="https://lh3.googleusercontent.com/xnzWNm7IiHeveS1grP5p_YZs9N_jfaJTiT0cakJSQqLwMgJlU-DD31ZzGHOYXTwZ_IWllGQ_N9QusU15oUiILW7dtOsrxp3Gj-jcM8styxDS8Q=s600",
        size="full",
        aspect_ratio="20:13",
        aspect_mode="cover"
    )

    # Body Text Components
    title_text = TextComponent(
        text="Traditional Mochi",
        weight="bold",
        size="xl"
    )

    rating_stars = [
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png", size="sm"),
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png", size="sm"),
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png", size="sm"),
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png", size="sm"),
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gray_star_28.png", size="sm"),
        TextComponent(text="4.8", size="sm", color="#999999", margin="md", flex=0)
    ]
    rating_stars_box = BoxComponent(layout="baseline", margin="md", contents=rating_stars)

    recommended_dish = BoxComponent(
        layout="baseline",
        spacing="sm",
        contents=[
            TextComponent(text="Best Items", color="#aaaaaa", size="sm", flex=2),
            TextComponent(text="Mochi ,Sweetened White Gourd Jelly", wrap=True, color="#666666", size="sm", flex=5)
        ]
    )

    operating_hours = BoxComponent(
        layout="baseline",
        spacing="sm",
        contents=[
            TextComponent(text="Hours", color="#aaaaaa", size="sm", flex=2),
            TextComponent(text="17:00 - 23:30", wrap=True, color="#666666", size="sm", flex=5)
        ]
    )

    body_contents = [
        title_text,
        rating_stars_box,
        recommended_dish,
        operating_hours
    ]
    body_box = BoxComponent(layout="vertical", contents=body_contents)

    # Footer Button
    website_button = ButtonComponent(
        style="link",
        height="sm",
        action=URIAction(label="Menu", uri=link)
    )
    footer_contents = [website_button]
    footer_box = BoxComponent(layout="vertical", spacing="sm", contents=footer_contents)

    # Bubble Container
    bubble = BubbleContainer(
        body=body_box,
        hero=hero_image,
        footer=footer_box
    )

    # Return the Flex Message
    return FlexSendMessage(alt_text="Traditional Mochi Menu", contents=bubble)

  elif link == "https://liff.line.me/2000144386-Ax8WZ8k2/jp/shop/6":
    # Hero Image
    hero_image = ImageComponent(
        url="https://lh3.googleusercontent.com/xnzWNm7IiHeveS1grP5p_YZs9N_jfaJTiT0cakJSQqLwMgJlU-DD31ZzGHOYXTwZ_IWllGQ_N9QusU15oUiILW7dtOsrxp3Gj-jcM8styxDS8Q=s600",
        size="full",
        aspect_ratio="20:13",
        aspect_mode="cover"
    )

    # Body Text Components
    title_text = TextComponent(
        text="麻糬寶寶",
        weight="bold",
        size="xl"
    )

    rating_stars = [
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png", size="sm"),
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png", size="sm"),
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png", size="sm"),
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png", size="sm"),
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gray_star_28.png", size="sm"),
        TextComponent(text="4.8", size="sm", color="#999999", margin="md", flex=0)
    ]
    rating_stars_box = BoxComponent(layout="baseline", margin="md", contents=rating_stars)

    recommended_dish = BoxComponent(
        layout="baseline",
        spacing="sm",
        contents=[
            TextComponent(text="おすすめ", color="#aaaaaa", size="sm", flex=2),
            TextComponent(text="麻糬 冬瓜茶ゼリー", wrap=True, color="#666666", size="sm", flex=5)
        ]
    )

    operating_hours = BoxComponent(
        layout="baseline",
        spacing="sm",
        contents=[
            TextComponent(text="営業時間", color="#aaaaaa", size="sm", flex=2),
            TextComponent(text="17:00 - 23:30", wrap=True, color="#666666", size="sm", flex=5)
        ]
    )

    body_contents = [
        title_text,
        rating_stars_box,
        recommended_dish,
        operating_hours
    ]
    body_box = BoxComponent(layout="vertical", contents=body_contents)

    # Footer Button
    website_button = ButtonComponent(
        style="link",
        height="sm",
        action=URIAction(label="メニュー", uri=link)
    )
    footer_contents = [website_button]
    footer_box = BoxComponent(layout="vertical", spacing="sm", contents=footer_contents)

    # Bubble Container
    bubble = BubbleContainer(
        body=body_box,
        hero=hero_image,
        footer=footer_box
    )

    # Return the Flex Message
    return FlexSendMessage(alt_text="麻糬寶寶メニュー", contents=bubble)

  elif link == "https://liff.line.me/2000144386-Ax8WZ8k2/zh/shop/7":
    # Hero Image
    hero_image = ImageComponent(
        url="https://lordcat.tw/wp-content/uploads/2019/07/1652286920-242e52376d32d3137a236f1236f57adf.jpg",
        size="full",
        aspect_ratio="20:13",
        aspect_mode="cover"
    )

    # Body Text Components
    title_text = TextComponent(
        text="紅燒麵牛雜湯",
        weight="bold",
        size="xl"
    )

    rating_stars = [
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png", size="sm"),
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png", size="sm"),
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gray_star_28.png", size="sm"),
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gray_star_28.png", size="sm"),
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gray_star_28.png", size="sm"),
        TextComponent(text="2.8", size="sm", color="#999999", margin="md", flex=0)
    ]
    rating_stars_box = BoxComponent(layout="baseline", margin="md", contents=rating_stars)

    recommended_dish = BoxComponent(
        layout="baseline",
        spacing="sm",
        contents=[
            TextComponent(text="推薦餐點", color="#aaaaaa", size="sm", flex=2),
            TextComponent(text="牛肉麵", wrap=True, color="#666666", size="sm", flex=5)
        ]
    )

    operating_hours = BoxComponent(
        layout="baseline",
        spacing="sm",
        contents=[
            TextComponent(text="營業時間", color="#aaaaaa", size="sm", flex=2),
            TextComponent(text="11:00 - 01:00", wrap=True, color="#666666", size="sm", flex=5)
        ]
    )

    body_contents = [
        title_text,
        rating_stars_box,
        recommended_dish,
        operating_hours
    ]
    body_box = BoxComponent(layout="vertical", contents=body_contents)

    # Footer Button
    website_button = ButtonComponent(
        style="link",
        height="sm",
        action=URIAction(label="菜單", uri=link)
    )
    footer_contents = [website_button]
    footer_box = BoxComponent(layout="vertical", spacing="sm", contents=footer_contents)

    # Bubble Container
    bubble = BubbleContainer(
        body=body_box,
        hero=hero_image,
        footer=footer_box
    )

    # Return the Flex Message
    return FlexSendMessage(alt_text="紅燒牛肉麵牛雜湯菜單", contents=bubble)

  elif link == "https://liff.line.me/2000144386-Ax8WZ8k2/en/shop/7":
    # Hero Image
    hero_image = ImageComponent(
        url="https://lordcat.tw/wp-content/uploads/2019/07/1652286920-242e52376d32d3137a236f1236f57adf.jpg",
        size="full",
        aspect_ratio="20:13",
        aspect_mode="cover"
    )

    # Body Text Components
    title_text = TextComponent(
        text="Beef Noodle and Beef Tripe Soup",
        weight="bold",
        size="xl"
    )

    rating_stars = [
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png", size="sm"),
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png", size="sm"),
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gray_star_28.png", size="sm"),
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gray_star_28.png", size="sm"),
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gray_star_28.png", size="sm"),
        TextComponent(text="2.8", size="sm", color="#999999", margin="md", flex=0)
    ]
    rating_stars_box = BoxComponent(layout="baseline", margin="md", contents=rating_stars)

    recommended_dish = BoxComponent(
        layout="baseline",
        spacing="sm",
        contents=[
            TextComponent(text="Best Items", color="#aaaaaa", size="sm", flex=2),
            TextComponent(text="Beef Noodle", wrap=True, color="#666666", size="sm", flex=5)
        ]
    )

    operating_hours = BoxComponent(
        layout="baseline",
        spacing="sm",
        contents=[
            TextComponent(text="Hours", color="#aaaaaa", size="sm", flex=2),
            TextComponent(text="11:00 - 01:00", wrap=True, color="#666666", size="sm", flex=5)
        ]
    )

    body_contents = [
        title_text,
        rating_stars_box,
        recommended_dish,
        operating_hours
    ]
    body_box = BoxComponent(layout="vertical", contents=body_contents)

    # Footer Button
    website_button = ButtonComponent(
        style="link",
        height="sm",
        action=URIAction(label="Menu", uri=link)
    )
    footer_contents = [website_button]
    footer_box = BoxComponent(layout="vertical", spacing="sm", contents=footer_contents)

    # Bubble Container
    bubble = BubbleContainer(
        body=body_box,
        hero=hero_image,
        footer=footer_box
    )

    # Return the Flex Message
    return FlexSendMessage(alt_text="Beef Noodle and Beef Tripe Soup Menu", contents=bubble)

  elif link == "https://liff.line.me/2000144386-Ax8WZ8k2/jp/shop/7":
    # Hero Image
    hero_image = ImageComponent(
        url="https://lordcat.tw/wp-content/uploads/2019/07/1652286920-242e52376d32d3137a236f1236f57adf.jpg",
        size="full",
        aspect_ratio="20:13",
        aspect_mode="cover"
    )

    # Body Text Components
    title_text = TextComponent(
        text="紅燒牛肉麵牛雜湯",
        weight="bold",
        size="xl"
    )

    rating_stars = [
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png", size="sm"),
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png", size="sm"),
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gray_star_28.png", size="sm"),
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gray_star_28.png", size="sm"),
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gray_star_28.png", size="sm"),
        TextComponent(text="2.8", size="sm", color="#999999", margin="md", flex=0)
    ]
    rating_stars_box = BoxComponent(layout="baseline", margin="md", contents=rating_stars)

    recommended_dish = BoxComponent(
        layout="baseline",
        spacing="sm",
        contents=[
            TextComponent(text="おすすめ", color="#aaaaaa", size="sm", flex=2),
            TextComponent(text="牛肉麵", wrap=True, color="#666666", size="sm", flex=5)
        ]
    )

    operating_hours = BoxComponent(
        layout="baseline",
        spacing="sm",
        contents=[
            TextComponent(text="営業時間", color="#aaaaaa", size="sm", flex=2),
            TextComponent(text="11:00 - 01:00", wrap=True, color="#666666", size="sm", flex=5)
        ]
    )

    body_contents = [
        title_text,
        rating_stars_box,
        recommended_dish,
        operating_hours
    ]
    body_box = BoxComponent(layout="vertical", contents=body_contents)

    # Footer Button
    website_button = ButtonComponent(
        style="link",
        height="sm",
        action=URIAction(label="メニュー", uri=link)
    )
    footer_contents = [website_button]
    footer_box = BoxComponent(layout="vertical", spacing="sm", contents=footer_contents)

    # Bubble Container
    bubble = BubbleContainer(
        body=body_box,
        hero=hero_image,
        footer=footer_box
    )

    # Return the Flex Message
    return FlexSendMessage(alt_text="紅燒牛肉麵牛雜湯メニュー", contents=bubble)

  elif link == "https://liff.line.me/2000144386-Ax8WZ8k2/zh/shop/8":
    # Hero Image
    hero_image = ImageComponent(
        url="https://margaret.tw/wp-content/uploads/2020/09/nEO_IMG_DSC09917.jpg",
        size="full",
        aspect_ratio="20:13",
        aspect_mode="cover"
    )

    # Body Text Components
    title_text = TextComponent(
        text="東發號油飯麵線",
        weight="bold",
        size="xl"
    )

    rating_stars = [
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png", size="sm"),
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png", size="sm"),
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png", size="sm"),
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gray_star_28.png", size="sm"),
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gray_star_28.png", size="sm"),
        TextComponent(text="3.6", size="sm", color="#999999", margin="md", flex=0)
    ]
    rating_stars_box = BoxComponent(layout="baseline", margin="md", contents=rating_stars)

    recommended_dish = BoxComponent(
        layout="baseline",
        spacing="sm",
        contents=[
            TextComponent(text="推薦餐點", color="#aaaaaa", size="sm", flex=2),
            TextComponent(text="油飯、麵線、肉羹", wrap=True, color="#666666", size="sm", flex=5)
        ]
    )

    operating_hours = BoxComponent(
        layout="baseline",
        spacing="sm",
        contents=[
            TextComponent(text="營業時間", color="#aaaaaa", size="sm", flex=2),
            TextComponent(text="08:30 - 00:00", wrap=True, color="#666666", size="sm", flex=5)
        ]
    )

    body_contents = [
        title_text,
        rating_stars_box,
        recommended_dish,
        operating_hours
    ]
    body_box = BoxComponent(layout="vertical", contents=body_contents)

    # Footer Button
    website_button = ButtonComponent(
        style="link",
        height="sm",
        action=URIAction(label="菜單", uri=link)
    )
    footer_contents = [website_button]
    footer_box = BoxComponent(layout="vertical", spacing="sm", contents=footer_contents)

    # Bubble Container
    bubble = BubbleContainer(
        body=body_box,
        hero=hero_image,
        footer=footer_box
    )

    # Return the Flex Message
    return FlexSendMessage(alt_text="東發號菜單", contents=bubble)

  elif link == "https://liff.line.me/2000144386-Ax8WZ8k2/en/shop/8":
    # Hero Image
    hero_image = ImageComponent(
        url="https://margaret.tw/wp-content/uploads/2020/09/nEO_IMG_DSC09917.jpg",
        size="full",
        aspect_ratio="20:13",
        aspect_mode="cover"
    )

    # Body Text Components
    title_text = TextComponent(
        text="Oyster Vermicelli and Glutinous Oil Rice",
        weight="bold",
        size="xl"
    )

    rating_stars = [
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png", size="sm"),
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png", size="sm"),
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png", size="sm"),
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gray_star_28.png", size="sm"),
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gray_star_28.png", size="sm"),
        TextComponent(text="3.6", size="sm", color="#999999", margin="md", flex=0)
    ]
    rating_stars_box = BoxComponent(layout="baseline", margin="md", contents=rating_stars)

    recommended_dish = BoxComponent(
        layout="baseline",
        spacing="sm",
        contents=[
            TextComponent(text="Best Items", color="#aaaaaa", size="sm", flex=2),
            TextComponent(text="Vermicelli, Oily Rice", wrap=True, color="#666666", size="sm", flex=5)
        ]
    )

    operating_hours = BoxComponent(
        layout="baseline",
        spacing="sm",
        contents=[
            TextComponent(text="Hours", color="#aaaaaa", size="sm", flex=2),
            TextComponent(text="08:30 - 00:00", wrap=True, color="#666666", size="sm", flex=5)
        ]
    )

    body_contents = [
        title_text,
        rating_stars_box,
        recommended_dish,
        operating_hours
    ]
    body_box = BoxComponent(layout="vertical", contents=body_contents)

    # Footer Button
    website_button = ButtonComponent(
        style="link",
        height="sm",
        action=URIAction(label="Menu", uri=link)
    )
    footer_contents = [website_button]
    footer_box = BoxComponent(layout="vertical", spacing="sm", contents=footer_contents)

    # Bubble Container
    bubble = BubbleContainer(
        body=body_box,
        hero=hero_image,
        footer=footer_box
    )

    # Return the Flex Message
    return FlexSendMessage(alt_text="Oyster Vermicelli and Glutinous Oil Rice Menu", contents=bubble)

  elif link == "https://liff.line.me/2000144386-Ax8WZ8k2/jp/shop/8":
    # Hero Image
    hero_image = ImageComponent(
        url="https://margaret.tw/wp-content/uploads/2020/09/nEO_IMG_DSC09917.jpg",
        size="full",
        aspect_ratio="20:13",
        aspect_mode="cover"
    )

    # Body Text Components
    title_text = TextComponent(
        text="東發號",
        weight="bold",
        size="xl"
    )

    rating_stars = [
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png", size="sm"),
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png", size="sm"),
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png", size="sm"),
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gray_star_28.png", size="sm"),
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gray_star_28.png", size="sm"),
        TextComponent(text="3.6", size="sm", color="#999999", margin="md", flex=0)
    ]
    rating_stars_box = BoxComponent(layout="baseline", margin="md", contents=rating_stars)

    recommended_dish = BoxComponent(
        layout="baseline",
        spacing="sm",
        contents=[
            TextComponent(text="おすすめ", color="#aaaaaa", size="sm", flex=2),
            TextComponent(text="麺線、肉羹、油飯", wrap=True, color="#666666", size="sm", flex=5)
        ]
    )

    operating_hours = BoxComponent(
        layout="baseline",
        spacing="sm",
        contents=[
            TextComponent(text="営業時間", color="#aaaaaa", size="sm", flex=2),
            TextComponent(text="08:30 - 00:00", wrap=True, color="#666666", size="sm", flex=5)
        ]
    )

    body_contents = [
        title_text,
        rating_stars_box,
        recommended_dish,
        operating_hours
    ]
    body_box = BoxComponent(layout="vertical", contents=body_contents)

    # Footer Button
    website_button = ButtonComponent(
        style="link",
        height="sm",
        action=URIAction(label="メニュー", uri=link)
    )
    footer_contents = [website_button]
    footer_box = BoxComponent(layout="vertical", spacing="sm", contents=footer_contents)

    # Bubble Container
    bubble = BubbleContainer(
        body=body_box,
        hero=hero_image,
        footer=footer_box
    )

    # Return the Flex Message
    return FlexSendMessage(alt_text="東發號メニュー", contents=bubble)

  elif link == "https://liff.line.me/2000144386-Ax8WZ8k2/zh/shop/9":
    # Hero Image
    hero_image = ImageComponent(
        url="https://g.udn.com.tw/upfiles/B_JO/josh091029/PSN_PHOTO/833/f_27254833_1.JPG",
        size="full",
        aspect_ratio="20:13",
        aspect_mode="cover"
    )

    # Body Text Components
    title_text = TextComponent(
        text="福島屋圓圓燒",
        weight="bold",
        size="xl"
    )

    rating_stars = [
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png", size="sm"),
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png", size="sm"),
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png", size="sm"),
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gray_star_28.png", size="sm"),
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gray_star_28.png", size="sm"),
        TextComponent(text="3.8", size="sm", color="#999999", margin="md", flex=0)
    ]
    rating_stars_box = BoxComponent(layout="baseline", margin="md", contents=rating_stars)

    recommended_dish = BoxComponent(
        layout="baseline",
        spacing="sm",
        contents=[
            TextComponent(text="推薦餐點", color="#aaaaaa", size="sm", flex=2),
            TextComponent(text="圓圓燒", wrap=True, color="#666666", size="sm", flex=5)
        ]
    )

    operating_hours = BoxComponent(
        layout="baseline",
        spacing="sm",
        contents=[
            TextComponent(text="營業時間", color="#aaaaaa", size="sm", flex=2),
            TextComponent(text="17:00 - 23:30", wrap=True, color="#666666", size="sm", flex=5)
        ]
    )

    body_contents = [
        title_text,
        rating_stars_box,
        recommended_dish,
        operating_hours
    ]
    body_box = BoxComponent(layout="vertical", contents=body_contents)

    # Footer Button
    website_button = ButtonComponent(
        style="link",
        height="sm",
        action=URIAction(label="菜單", uri=link)
    )
    footer_contents = [website_button]
    footer_box = BoxComponent(layout="vertical", spacing="sm", contents=footer_contents)

    # Bubble Container
    bubble = BubbleContainer(
        body=body_box,
        hero=hero_image,
        footer=footer_box
    )

    # Return the Flex Message
    return FlexSendMessage(alt_text="福島屋圓圓燒菜單", contents=bubble)

  elif link == "https://liff.line.me/2000144386-Ax8WZ8k2/en/shop/9":
    # Hero Image
    hero_image = ImageComponent(
        url="https://g.udn.com.tw/upfiles/B_JO/josh091029/PSN_PHOTO/833/f_27254833_1.JPG",
        size="full",
        aspect_ratio="20:13",
        aspect_mode="cover"
    )

    # Body Text Components
    title_text = TextComponent(
        text="Fukushimaya Okonomiyaki",
        weight="bold",
        size="xl"
    )

    rating_stars = [
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png", size="sm"),
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png", size="sm"),
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png", size="sm"),
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gray_star_28.png", size="sm"),
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gray_star_28.png", size="sm"),
        TextComponent(text="3.8", size="sm", color="#999999", margin="md", flex=0)
    ]
    rating_stars_box = BoxComponent(layout="baseline", margin="md", contents=rating_stars)

    recommended_dish = BoxComponent(
        layout="baseline",
        spacing="sm",
        contents=[
            TextComponent(text="Best Items", color="#aaaaaa", size="sm", flex=2),
            TextComponent(text="Okonomiyaki", wrap=True, color="#666666", size="sm", flex=5)
        ]
    )

    operating_hours = BoxComponent(
        layout="baseline",
        spacing="sm",
        contents=[
            TextComponent(text="Hours", color="#aaaaaa", size="sm", flex=2),
            TextComponent(text="17:00 - 23:30", wrap=True, color="#666666", size="sm", flex=5)
        ]
    )

    body_contents = [
        title_text,
        rating_stars_box,
        recommended_dish,
        operating_hours
    ]
    body_box = BoxComponent(layout="vertical", contents=body_contents)

    # Footer Button
    website_button = ButtonComponent(
        style="link",
        height="sm",
        action=URIAction(label="Menu", uri=link)
    )
    footer_contents = [website_button]
    footer_box = BoxComponent(layout="vertical", spacing="sm", contents=footer_contents)

    # Bubble Container
    bubble = BubbleContainer(
        body=body_box,
        hero=hero_image,
        footer=footer_box
    )

    # Return the Flex Message
    return FlexSendMessage(alt_text="Fukushimaya Okonomiyaki Menu", contents=bubble)

  elif link == "https://liff.line.me/2000144386-Ax8WZ8k2/jp/shop/9":
    # Hero Image
    hero_image = ImageComponent(
        url="https://g.udn.com.tw/upfiles/B_JO/josh091029/PSN_PHOTO/833/f_27254833_1.JPG",
        size="full",
        aspect_ratio="20:13",
        aspect_mode="cover"
    )

    # Body Text Components
    title_text = TextComponent(
        text="まるまる焼",
        weight="bold",
        size="xl"
    )

    rating_stars = [
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png", size="sm"),
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png", size="sm"),
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png", size="sm"),
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gray_star_28.png", size="sm"),
        IconComponent(url="https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gray_star_28.png", size="sm"),
        TextComponent(text="3.8", size="sm", color="#999999", margin="md", flex=0)
    ]
    rating_stars_box = BoxComponent(layout="baseline", margin="md", contents=rating_stars)

    recommended_dish = BoxComponent(
        layout="baseline",
        spacing="sm",
        contents=[
            TextComponent(text="おすすめ", color="#aaaaaa", size="sm", flex=2),
            TextComponent(text="まるまる焼", wrap=True, color="#666666", size="sm", flex=5)
        ]
    )

    operating_hours = BoxComponent(
        layout="baseline",
        spacing="sm",
        contents=[
            TextComponent(text="営業時間", color="#aaaaaa", size="sm", flex=2),
            TextComponent(text="17:00 - 23:30", wrap=True, color="#666666", size="sm", flex=5)
        ]
    )

    body_contents = [
        title_text,
        rating_stars_box,
        recommended_dish,
        operating_hours
    ]
    body_box = BoxComponent(layout="vertical", contents=body_contents)

    # Footer Button
    website_button = ButtonComponent(
        style="link",
        height="sm",
        action=URIAction(label="メニュー", uri=link)
    )
    footer_contents = [website_button]
    footer_box = BoxComponent(layout="vertical", spacing="sm", contents=footer_contents)

    # Bubble Container
    bubble = BubbleContainer(
        body=body_box,
        hero=hero_image,
        footer=footer_box
    )

    # Return the Flex Message
    return FlexSendMessage(alt_text="まるまる焼メニュー", contents=bubble)

# handle text message with LLM
import openai

openai.api_key = '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'


@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    qa = open('qa.csv', 'r').read()
    
    lang = open("tmp/"+ event.source.user_id + ".txt","r").read()

    prompt = f"""You are a helpful question-answer assistant, you determine which question in qa.csv most possibly is the user question, and return the string of the question's answer in qa.csv in {lang}.
    If the user question don't match any question in qa.csv(the highest possibility is less than 30%), you generate an answer in {lang} within 60 charactors.
    qa.csv :
    {qa}
    """

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": prompt,
            },
            {
                "role": "user",
                "content": event.message.text,
            },
        ],
    )

    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=completion.choices[0].message.content))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))