from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError, LineBotApiError
)
from linebot.models import *

import sys
import os
import configparser
import sys
sys.setrecursionlimit(2000)

# Add the directory containing your module to the Python path (wants absolute paths)
scriptpath = '/app'
sys.path.append(os.path.abspath(scriptpath))
import ImageScrapper
from IfoodieCrawler import IFoodie

app = Flask(__name__)
conf = configparser.ConfigParser()
conf.read("config.ini")


line_bot_api = LineBotApi(conf["LineBot"]["channelaccesstoken"])    # Channel Access Token
handler = WebhookHandler(conf["LineBot"]["channelsecret"])          # Channel Secret

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
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
        abort(400)
    return 'OK'

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    if event.message.text == "找菜單":

        #food = IFoodie("台中市" ,"雞排")  #使用者傳入的訊息文字

        #line_bot_api.reply_message(  # 回應前五間最高人氣且營業中的餐廳訊息文字
        #    event.reply_token,
        #    TextSendMessage(text=food.scrape())
        #)
        
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="請輸入餐廳名稱:")
        )
         
        if event.message.type == 'text':
            GoogleImageUrlQuery = ImageScrapper.GoogleImageUrl(event.message.text + " 菜單")
            ImageUrl = GoogleImageUrlQuery.GetGoogleImageUrlByKeyword()

            image = ImageSendMessage(original_content_url=ImageUrl, preview_image_url=ImageUrl)
            line_bot_api.reply_message(event.reply_token, image)
    
    else:
        GoogleImageUrlQuery = ImageScrapper.GoogleImageUrl(event.message.text + " 菜單")
        ImageUrl = GoogleImageUrlQuery.GetGoogleImageUrlByKeyword()

        image = ImageSendMessage(original_content_url=ImageUrl, preview_image_url=ImageUrl)
        line_bot_api.reply_message(event.reply_token, image)


    # elif event.message.text == "影片":
        # video = VideoSendMessage(original_content_url='影片網址', preview_image_url='預覽的圖片網址')
        # line_bot_api.reply_message(event.reply_token, video)


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
