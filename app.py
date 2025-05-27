from flask import Flask, request, abort
import os

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

# 環境変数からアクセストークンとシークレットを取得
line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = event.message.text.lower()

    if any(keyword in message for keyword in ["渡航費", "マッチングアプリ", "外国人", "会ったことがない", "手術費"]):
        reply_text = (
            "ご相談ありがとうございます。\n"
            "もしかしたら、いま少し混乱されているかもしれませんね。\n"
            "「信じたい気持ち」と「どこかで不安な気持ち」が入り混じって、\n"
            "とても苦しい状況だと思います。\n\n"
            "そのやり取りですが、「ロマンス詐欺」と呼ばれる手口とよく似ています。\n\n"
            "これは、SNSやマッチングアプリなどで親しくなった相手が、\n"
            "しばらくしてから「会いたいけど渡航費が足りない」「手術費を立て替えて」などと\n"
            "言ってくるのが典型的な流れです。\n\n"
            "実際に、こうした相談は非常に多く寄せられており、\n"
            "一度も会っていないのにお金を送ってしまい、大きな被害を受けた方も少なくありません。\n\n"
            "不安があるのは、あなたの感覚が正常だからです。\n"
            "以下のリンクに、同様の被害事例や警告情報がまとめられています。\n"
            "ぜひ一度、ご自身のペースで確認してみてください。\n\n"
            "【参考リンク】\n"
            "- 消費者庁： https://www.caa.go.jp/policies/policy/consumer_policy/caution/internet_trouble_001/\n"
            "- 国民生活センター： https://www.kokusen.go.jp/t_box/data/t_box-faq_qa2023_02.html\n"
            "- ANNニュース： https://www.youtube.com/watch?v=5T1YVGwPmqg\n\n"
            "あなたがもし本当に悩んでいるのなら、\n"
            "どうか1人で抱え込まず、信頼できる人や公的機関に相談してくださいね。\n"
            "あなたが悪いわけではありません。信じる ​:contentReference[oaicite:0]{index=0}​
