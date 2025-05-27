from flask import Flask, request, abort
import os

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

# Flask アプリの初期化
app = Flask(__name__)

# 環境変数からLINEチャンネルのアクセストークンとシークレットを取得
line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))

# LINEからのWebhookイベントを受け取るエンドポイント
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers.get("X-Line-Signature")
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return "OK"

# メッセージを受信した時の処理
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = event.message.text.lower()

    if any(keyword in message for keyword in ["渡航費", "マッチングアプリ", "外国人", "会ったことがない", "手術費"]):
        reply_text = (
            "ご相談ありがとうございます。\n"
            "その内容は、ロマンス詐欺の典型的なパターンに非常に近いものです。\n"
            "実際に会ったことのない相手にお金を送るのは、どれだけ信じていても非常に危険です。\n"
            "今一度、冷静に考えてみてください。信じたい気持ちを悪用するのが詐欺師の常套手段です。"
        )
    else:
        reply_text = "メッセージを受け取りました。現在内容を確認しています。"

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_text)
    )

# Renderで正しく起動するためのポート設定
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
