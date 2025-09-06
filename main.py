# 必要な道具をインポートする
from flask import Flask, request, abort
from line_bot_sdk import LineBotApi, WebhookHandler
from line_bot_sdk.exceptions import InvalidSignatureError
from line_bot_sdk.models import MessageEvent, TextMessage, TextSendMessage
import os

# Flaskアプリの準備
app = Flask(__name__)

# あなたの「チャネルアクセストークン」と「チャネルシークレット」をここに設定
# ※実際には直接書き込まず、後述するサーバーの環境変数に設定します
channel_access_token = os.environ.get('LINE_CHANNEL_ACCESS_TOKEN', None)
channel_secret = os.environ.get('LINE_CHANNEL_SECRET', None)

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

# '/callback'というURLにPOSTリクエストが来た時の処理
@app.route("/callback", methods=['POST'])
def callback():
    # リクエストヘッダーから署名検証のための値を取得
    signature = request.headers['X-Line-Signature']

    # リクエストボディを取得
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # 署名を検証し、問題なければhandleに定義されている関数を呼び出す
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400) # 署名が不正な場合は400エラー

    return 'OK'

# メッセージイベントの処理
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # 受け取ったメッセージをそのまま送り返す
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))

# プログラムの実行
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)