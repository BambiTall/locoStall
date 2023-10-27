from flask import Flask, request, abort, jsonify

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models.events import FollowEvent
from linebot.models import (
    MessageEvent,
    TextMessage,
    TextSendMessage,
    PostbackEvent,
    TemplateSendMessage,
    QuickReplyButton,
    PostbackAction,
    QuickReply,
    RichMenu,
    ImageMessage,
    FlexSendMessage,
)
from templates import (
    shop_detail_flex_message,
    shoplist_carousel_template,
    instruction_text,
    order_detail_flex_message,
)

import requests
import json
import os
import re
from dotenv import load_dotenv

import logging
import google.cloud.logging
from google.cloud.logging.handlers import CloudLoggingHandler

import openai


client = google.cloud.logging.Client()
load_dotenv()

# 建立line event log，用來記錄line event
bot_event_handler = CloudLoggingHandler(client, name="bot_event")
bot_event_logger = logging.getLogger('bot_event')
bot_event_logger.setLevel(logging.INFO)
bot_event_logger.addHandler(bot_event_handler)

app = Flask(__name__)
line_bot_api = LineBotApi(f"{os.environ.get('LINE_ACCESS_TOKEN')}")
handler = WebhookHandler(f"{os.environ.get('LINE_CHANNEL_SECRET')}")
openai.api_key = f"{os.environ.get('OPENAI_KEY')}"
backend_url = f"{os.environ.get('BACKEND_URL')}"

language = "en"  # 預設語言為英文


@app.route("/", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    # print(body)
    bot_event_logger.info(body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


def setup_rich_menu(user_id, langcode):
    menuJson = json.load(open(f'static/richmenu_{langcode}.json', 'r'))
    lineRichMenuId = line_bot_api.create_rich_menu(
        rich_menu=RichMenu.new_from_json_dict(menuJson)
    )
    uploadImageFile = open(f'static/richmenu_{langcode}.jpg', 'rb')
    line_bot_api.set_rich_menu_image(lineRichMenuId, 'image/jpeg', uploadImageFile)
    line_bot_api.link_rich_menu_to_user(user_id, lineRichMenuId)


# Save user IDs to a file when they interact with the rich menu
@handler.add(FollowEvent)
def reply_text_and_get_user_profile(event):
    open('tmp/' + event.source.user_id + '.txt', 'w').write('en')
    setup_rich_menu(event.source.user_id, 'en')


@handler.add(PostbackEvent)
def handle_postback(event):
    user_id = event.source.user_id

    with open("tmp/" + user_id + ".txt", "r") as f:
        language = f.read()

    # Get Started 功能
    if event.postback.data == 'data1':
        reply_text = instruction_text(language)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))
        return

    # 選擇語言功能
    elif event.postback.data == 'data2':
        quick_reply = QuickReply(
            items=[
                QuickReplyButton(action=PostbackAction(label="中文", data="zh")),
                QuickReplyButton(action=PostbackAction(label="English", data="en")),
                QuickReplyButton(action=PostbackAction(label="日本語", data="ja")),
            ]
        )
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='Language Setting', quick_reply=quick_reply),
        )
        return

    # explore 清單
    elif event.postback.data == 'data3':
        carousel_template = shoplist_carousel_template(language)
        template_message = TemplateSendMessage(
            alt_text='Carousel Template', template=carousel_template
        )
        line_bot_api.reply_message(event.reply_token, template_message)
        return

    elif event.postback.data == 'zh':
        language = "zh"
        with open("tmp/" + user_id + ".txt", "w") as f:
            f.write('zh')
        setup_rich_menu(user_id, 'zh')
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='設定完成'))
        return

    elif event.postback.data == 'ja':
        language = "ja"  # 更新語言設定為日文
        with open("tmp/" + user_id + ".txt", "w") as f:
            f.write('ja')
        setup_rich_menu(user_id, 'ja')
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text='セットアップが完了しました')
        )
        return

    elif event.postback.data == 'en':
        language = "en"  # 更新語言設定為英文
        with open("tmp/" + user_id + ".txt", "w") as f:
            f.write('en')
        setup_rich_menu(user_id, 'en')
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text='Setup complete')
        )
        return


# 處理接收到的訊息事件
@handler.add(MessageEvent, message=ImageMessage)
def handle_image_message(event):
    message_content = line_bot_api.get_message_content(event.message.id)
    language = open("tmp/" + event.source.user_id + ".txt", "r").read()

    with open('tmp/' + event.message.id + '.jpg', 'wb') as fd:
        for chunk in message_content.iter_content():
            fd.write(chunk)

    with open('tmp/' + event.message.id + '.jpg', 'rb') as file:
        files = {'file': file}
        response = requests.post(backend_url + '/predict', files=files)
        data = response.json()
        shop_id = data.get('predicted_class')

        if shop_id is None:
            failed_message = {
                'zh': '辨識失敗\n請對準招牌再拍一次',
                'ja': '認識失敗です\n看板に合わせてもう一度撮ってみてください',
                'en': 'Recognition failed.\nPlease aim at the signboard and take another shot',
            }
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text=failed_message[language])
            )
        else:
            flex_message = shop_detail_flex_message(shop_id, language)
            line_bot_api.reply_message(event.reply_token, flex_message)
    os.remove('tmp/' + event.message.id + '.jpg')


def get_order_detail(order_id, language, user_id):
    language = 'jp' if language == 'ja' else language
    response = requests.get(f"{backend_url}/{language}/order_detail/{order_id}")

    if response.status_code == 200:
        data = response.json()
        order = data['data']
        if user_id != order['user_id']:
            return None
        item_list = json.loads(order['item_list'])

        order['item_list'] = [
            {
                'qty': item['qty'],
                'name': item['name'],
                'price': item['price'],
            }
            for item in item_list
        ]

        order['total_price'] = sum(int(item['price']) for item in order['item_list'])

        return order
    else:
        return None


# 接到訂單訊息後，擷取訊息編號 = order number，如果成功擷取訂單訊息，會發 flex msg，錯誤則有訂單編號錯誤重新下定
@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    user_id = event.source.user_id
    text = event.message.text

    # handle text message with LLM
    if text[:4] == '@bot':
        qa = open('qa.csv', 'r').read()
        prompt = f"""qa.csv: 
{qa}
(end of file)
You are a question-answering assistant. Find the most likely user question in qa.csv and return its answer. If no match (probability < 30%), generate a concise answer within 60 characters, using info from qa.csv for accuracy. Translate final answer to the user's language."""

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

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=completion.choices[0].message.content),
        )

    elif "訂單" in text or "注文" in text or "Order" in text:
        language = open('tmp/' + user_id + '.txt', 'r').read()
        user = requests.get(f'{backend_url}/line_user/{user_id}').json()
        alt_text_ = {'zh': '訂單訊息', 'ja': '注文履歷', 'en': 'User Order'}
        error_ = {
            'zh': '訂單未成立，請重新下訂',
            'ja': 'Please order again(Japanese)',
            'en': 'Please order again',
        }
        pattern = r'\d+'
        match = re.search(pattern, text)
        if match:
            order_id = int(match.group())
            order = get_order_detail(order_id, language, user['id'])

            if order:
                flex_message = order_detail_flex_message(
                    order['id'],
                    order['shop_id'],
                    order['total_price'],
                    order['payment'],
                    order['created_at'][:19],
                    order['item_list'],
                    order['paid'],
                    language,
                )
                line_bot_api.reply_message(
                    event.reply_token,
                    FlexSendMessage(
                        alt_text=alt_text_[language], contents=flex_message
                    ),
                )
            else:
                line_bot_api.reply_message(
                    event.reply_token, TextSendMessage(text=error_[language])
                )


application = app

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
