from flask import Blueprint, Flask, request, jsonify, make_response, abort
import requests
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


@linebot_bp.route(f'{os.environ["API_BASE"]}/backend/token', methods=['POST'])
def send_message():
    data = request.get_json()
    access_token = data['accessToken']
    
    verify_response = verify_access_token(access_token)
    if verify_response.status_code != 200:
        print("検証エラー")
        return "検証エラー", 400
    
    profile_response = get_profile(access_token)
    if profile_response.status_code != 200:
        print("プロフィール取得エラー")
        return "プロフィール取得エラー", 400
    
    user_id = profile_response.json()['userId']
    message_response = liff_line_message_push(user_id)
    if message_response.status_code != 200:
        print("メッセージ送信エラー")
        return "メッセージ送信エラー", 400
    
    print("送信完了")
    return "送信完了"

def verify_access_token(id_token):
    response = requests.get(f'https://api.line.me/oauth2/v2.1/verify?access_token={id_token}')
    return response

def get_profile(accessToken):
    headers = {
        "Content-type": "application/x-www-form-urlencoded",
        "Authorization": "Bearer " + accessToken
    }
    response = requests.get('https://api.line.me/v2/profile', headers=headers)
    return response

def liff_line_message_push(user_id):
    headers = {
        "Content-type": "application/json",
        "Authorization": "Bearer " + "チャネルアクセストークン"
    }
    payload = {
        "to": user_id,
        "messages": [
            {
                "type": "text",
                "text": "管理者からメッセージ送信したしん！"
            }
        ]
    }
    response = requests.post('https://api.line.me/v2/bot/message/push', json=payload, headers=headers)
    return response

# 學你說話
@handler.add(MessageEvent,message=TextMessage)
def echo_message(event):
    if isinstance(event.message, TextMessage):
        msg=event.message.text
        Line_bot_api.reply_message(event.reply_token, TextSendMessage(text=msg))