from flask import Blueprint, Flask, request, jsonify, make_response, abort
import os
import sys

from dotenv import load_dotenv
load_dotenv()

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

linebot_bp = Blueprint('linebot_bp', __name__)


# setting
line_bot_api = LineBotApi(f'{os.environ.get("LINE_ACCESS_TOKEN")}')
handler = WebhookHandler(f'{os.environ.get("LINE_CHANNEL_SECRET")}')

# Get linebot list
@linebot_bp.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body=request.get_data(as_text=True)
    try:
        print(body, signature)
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


# 學你說話
@handler.add(MessageEvent,message=TextMessage)
def echo_message(event):
    if isinstance(event.message, TextMessage):
        msg=event.message.text
        Line_bot_api.reply_message(event.reply_token, TextSendMessage(text=msg))