from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageSendMessage, ImagemapSendMessage, BaseSize
)
# import configparser 
import time

from opggcrawl import crawlRecordMap

app = Flask(__name__)


# config = configparser.ConfigParser()
# config.read('config.ini')

# line_bot_api = LineBotApi(config.get('line-bot', 'channel_access_token')) #已存於config.ini
# handler = WebhookHandler(config.get('line-bot', 'channel_secret'))
line_bot_api = LineBotApi('JzCdzRnikorc4nBZEwaDHZb+w1+2mcoqnRVmBLDCMAlm+QWIOX+J/OLOuAXw3D++xX3CPFtrlecYIWjc2NgBRJq/hi//KhuoVK3+pznDjZg8sKKGe/7RQdaja52lQRK1Qyq8y5fEQKzr5GGWDGtgFwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('d6f8fc00e2dc748ab95afd8e3e7f13f5')

@app.route("/", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'



# import pyimgur

# IMGUR_CLIENT_ID = 'c53d343d9ed9cc5'



@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.message.text[:1].upper() == "R":
        # input_word = event.message.text.replace(" ","") #合併字串取消空白
        summoner_name = event.message.text[1:]
        # content = crawlRecord(IMGUR_CLIENT_ID,summoner_name)
        # message = ImageSendMessage(original_content_url=content,preview_image_url=content)
        # line_bot_api.reply_message(event.reply_token, message)
        public_url=crawlRecordMap(summoner_name)
        imagemap_message = ImagemapSendMessage(
            base_url=public_url,
            alt_text=summoner_name+'的戰績',
            base_size=BaseSize(height=819, width=1040),
        )
        # 回覆 Imagmap 訊息
        try:
            line_bot_api.reply_message(event.reply_token,imagemap_message)
        except LineBotApiError as e:
            # 处理错误
            print(f"LINE Bot 回復失敗: {e.status_code} {e.error.message}")
            
    if event.message.text[:1].upper() == "G":
        imagemap_message = ImagemapSendMessage(
            base_url='https://storage.googleapis.com/linebot-pic-opgg/test3',
            alt_text='的戰績',
            base_size=BaseSize(height=819, width=1040),
        )
        # 回覆 Imagmap 訊息
        line_bot_api.reply_message(event.reply_token,imagemap_message)
    # else: line_bot_api.reply_message(event.reply_token,
    #                                  TextSendMessage(text=event.message.text))

if __name__ == "__main__":
    app.run(host='0.0.0.0')