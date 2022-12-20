import os
import sys
import globalvar

from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage


from fsm import TocMachine
from utils import send_text_message

load_dotenv()
globalvar.initialize()
globalvar.set("mode", 0)
globalvar.set("enterstart", 0)
print(globalvar.get("mode"))

machine = TocMachine(
    states=["user", "start", "mypic", "search", "searchingname",
            "getpic", "picname", "changepic", "savepic"],
    transitions=[
        {
            "trigger": "advance",
            "source": "user",
            "dest": "start",
            "conditions": "is_going_to_start",
        },
        {
            "trigger": "advance",
            "source": "start",
            "dest": "mypic",
            "conditions": "is_going_to_mypic",
        },
        {
            "trigger": "advance",
            "source": "mypic",
            "dest": "start",
            "conditions": "is_going_to_start",
        },
        {
            "trigger": "advance",
            "source": "start",
            "dest": "search",
            "conditions": "is_going_to_search",
        },
        {
            "trigger": "advance",
            "source": "search",
            "dest": "searchingname",
            "conditions": "is_going_to_searchingname",
        },
        {
            "trigger": "advance",
            "source": "searchingname",
            "dest": "start",
            "conditions": "is_going_to_start",
        },
        {
            "trigger": "advance",
            "source": "mypic",
            "dest": "getpic",
            "conditions": "is_going_to_getpic",
        },
        {
            "trigger": "advance",
            "source": "getpic",
            "dest": "start",
            "conditions": "is_going_to_start",
        },
        {
            "trigger": "advance",
            "source": "mypic",
            "dest": "picname",
            "conditions": "is_going_to_picname",
        },
        {
            "trigger": "advance",
            "source": "picname",
            "dest": "changepic",
            "conditions": "is_going_to_changepic",
        },
        {
            "trigger": "advance",
            "source": "changepic",
            "dest": "savepic",
            "conditions": "is_going_to_savepic",
        },
        {"trigger": "go_back", "source": "savepic", "dest": "start"},
    ],
    initial="user",
    auto_transitions=False,
    show_conditions=True,
)

app = Flask(__name__, static_url_path="")


# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv("LINE_CHANNEL_SECRET", None)
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
if channel_secret is None:
    print("Specify LINE_CHANNEL_SECRET as environment variable.")
    sys.exit(1)
if channel_access_token is None:
    print("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)


@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue

        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=event.message.text)
        )

    return "OK"


@app.route("/webhook", methods=["POST"])
def webhook_handler():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info(f"Request body: {body}")
    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if globalvar.get("mode") == 0:
            print("No Picture")
            print(globalvar.get("mode"))
            if not isinstance(event.message, TextMessage):
                continue
            if not isinstance(event.message.text, str):
                continue
        else:
            print("Picture allowed")
            print(globalvar.get("mode"))
        print(f"\nFSM STATE: {machine.state}")
        print(f"REQUEST BODY: \n{body}")
        response = machine.advance(event)
        if response == False:
            send_text_message(event.reply_token, "請輸入正確指令")

    return "OK"


@app.route("/show-fsm", methods=["GET"])
def show_fsm():
    machine.get_graph().draw("fsm.png", prog="dot", format="png")
    return send_file("fsm.png", mimetype="image/png")


if __name__ == "__main__":
    machine.get_graph().draw("fsm.png", prog="dot", format="png")
    port = os.environ.get("PORT", 8000)
    app.run(host="0.0.0.0", port=port, debug=True)
