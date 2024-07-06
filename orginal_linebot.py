from flask import Flask, request
import json
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

# 讀取配置文件中的資訊
with open('config.json', 'r') as f:
    config = json.load(f)
    access_token = config['access_token']
    secret = config['secret']

line_bot_api = LineBotApi(access_token)
handler = WebhookHandler(secret)

@app.route("/", methods=['POST'])
def linebot():
    body = request.get_data(as_text=True)
    signature = request.headers['X-Line-Signature']

    try:
        handler.handle(body, signature)
        json_data = json.loads(body)
        
        reply_token = json_data['events'][0]['replyToken']
        message_type = json_data['events'][0]['message']['type']

        if message_type == 'text':
            message_text = json_data['events'][0]['message']['text']
            reply = message_text
        else:
            reply = '你傳的不是文字呦～'

        line_bot_api.reply_message(reply_token, TextSendMessage(text=reply))
    except Exception as e:
        print(str(e))
        return 'Error'

    return 'OK'

if __name__ == "__main__":
    app.run(debug=True)
