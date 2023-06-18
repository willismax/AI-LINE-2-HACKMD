import os
# from dotenv import load_dotenv
from flask import Flask, request, abort, jsonify
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, FlexSendMessage
)

# load_dotenv()
# 使用自訂的模組(資料夾-檔案)
import my_moduls.hackmd_bot as hb
import my_moduls.my_functions as mf
from my_moduls.openai_bot import OpenAIBot


app = Flask(__name__)

line_bot_api = LineBotApi(os.environ.get("CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.environ.get("CHANNEL_SECRET"))
chatgpt = OpenAIBot()


# Messages on start and restart
line_bot_api.push_message(
    os.environ.get("LINE_USER_ID"), 
    TextSendMessage(text='Bot Starting')
    )

@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        return jsonify({"message": "Invalid signature."}), 400
    return jsonify({"message": "Success"})


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    """LINE MessageAPI message processing"""
    text = event.message.text
    if event.source.user_id =='Udeadbeefdeadbeefdeadbeefdeadbeef':
        return 'OK'
    
    # 處裡圖片的方式: 上傳圖床、存HackMD暫存筆記
    if event.message.type=='image':
        image = line_bot_api.get_message_content(event.message.id)
        content = hb.flex_reply_image(image)
        message = FlexSendMessage(
            alt_text = "圖片已上傳至HackMD",
            contents = content
        )
        line_bot_api.reply_message(event.reply_token, message)
    
    if event.message.type=='text':
        text =  str(event.message.text)
        content = hb.add_temp_note(text)
        message = TextSendMessage(text=content)
        line_bot_api.reply_message(event.reply_token, message)

    # if "http" in text or "https" in text:
    #     url = text
    #     title, first_subtitle, first_paragraph = mf.extract_url_content(url)
    #     summary, hashtags = mf.generate_summary_and_hashtags(title + " " + first_subtitle + " " + first_paragraph, openai_api_key)
    #     new_note = mf.process_summary_and_create_hackmd(url, title, first_subtitle, first_paragraph, summary, hashtags)
    #     # Send a Flex Message with the new HackMD note information
    # flex_message = {
    #     "type": "bubble",
    #     "header": {
    #         "type": "box",
    #         "layout": "vertical",
    #         "contents": [
    #             {
    #                 "type": "text",
    #                 "text": "Summary",
    #                 "size": "xl",
    #                 "weight": "bold"
    #             }
    #         ]
    #     },
    #     "body": {
    #         "type": "box",
    #         "layout": "vertical",
    #         "contents": [
    #             {
    #                 "type": "text",
    #                 "text": title,
    #                 "weight": "bold"
    #             },
    #             {
    #                 "type": "text",
    #                 "text": summary
    #             }
    #         ]
    #     },
    #     "footer": {
    #         "type": "box",
    #         "layout": "vertical",
    #         "contents": [
    #             {
    #                 "type": "button",
    #                 "action": {
    #                     "type": "uri",
    #                     "label": "View on HackMD",
    #                     "uri": new_note["noteUrl"]
    #                 },
    #                 "style": "primary"
    #             }
    #         ]
    #     }
    # }
    # line_bot_api.reply_message(event.reply_token, FlexSendMessage(alt_text="Summary", contents=flex_message))

if __name__ == "__main__":
    app.run()