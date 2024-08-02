from flask import Flask, request, abort, jsonify
from pymongo import MongoClient
from bson.json_util import dumps
from flask_cors import CORS
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage,
)
from linebot.v3.webhooks import MessageEvent, TextMessageContent

app = Flask(__name__)
CORS(app)
# 連接到 MongoDB
client = MongoClient(
    "mongodb+srv://jimmy147156:stvuKn16iQp8jehy@cluster0.zbbv4pu.mongodb.net/"
)
db = client["test"]  # 替換為您的資料庫名稱
collection = db["formdatas"]

configuration = Configuration(
    access_token="rHn0jkQT3FF3BpQe93lxUHsJAgCqXPIVNu2qyFF1kz6SLnEpUmc06iwyahqC0hPt0r2vo5gfYB5lujENTfwL4R7BIggFsAtJTioEukAmJeIHS7V5fTgI9Yzt3ICcICgQILBKb90gVjb4Cqy4lIU2YgdB04t89/1O/w1cDnyilFU="
)
handler = WebhookHandler("8d75ddf606f1775889e3ab1b6ef7960b")


@app.route("/data", methods=["GET"])
def get_data():
	try:
		HotKeyword = (db["keywords"].find())[0]
		WordcloudImage = (db["wordcloud_images"].find())[0]
		return jsonify({"HotKeyword": dumps(HotKeyword), "WordcloudImage": dumps(WordcloudImage)})
	except Exception as e:
		return str(e), 400

# 儲存資料的變數
@app.route("/", methods=["POST"])
def save_data():
	try:
		# 從 request.json 獲取數據並插入到 MongoDB
		form_data = request.json
		result = collection.insert_one(form_data)
		# 儲存資料到變數

		return jsonify({"message": "Data saved", "data": dumps(form_data)}), 201
	except Exception as error:
		print("Error saving data:", error)
		return jsonify({"error": "Error saving data"}), 500


@app.route("/", methods=["GET"])
def show_data():
	return "Hello, World!"


@app.route("/callback", methods=["POST"])
def callback():
	# get X-Line-Signature header value
	signature = request.headers["X-Line-Signature"]

	# get request body as text
	body = request.get_data(as_text=True)
	app.logger.info("Request body: " + body)

	# handle webhook body
	try:
		handler.handle(body, signature)
	except InvalidSignatureError:
		app.logger.info(
				"Invalid signature. Please check your channel access token/channel secret."
		)
		abort(400)

	return "OK"


@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text="hello world")],
            )
        )


if __name__ == "__main__":
    app.run(debug=True)

# https://b1da-2001-b011-8012-5636-303b-5a04-a047-b711.ngrok-free.app/callbackngrok config add-authtoken 2Ptq2vGVnvGqUJ2mOZkNQka6FKY_6Z4wUzdgXrtFatCRRSrch
#
