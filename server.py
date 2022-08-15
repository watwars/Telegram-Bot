
from flask import Flask, jsonify, request
import os
import json

import process_message
from helpers import utils, telegram_api


placeholder_response = {"status": "ok"}

app = Flask(__name__)
app.config["DEBUG"] = os.environ.get("ENV") == "dev"


@app.before_first_request
def setup():
    telegram_api.set_webhook()


@app.route('/')
def index():
    ok = telegram_api.get_webhook_info()
    return jsonify({"status": ok})


@app.route('/updates', methods=['POST'])
def process_webhook():
    data = json.loads(request.data)
    if utils.did_processed_message(data):
        return jsonify(placeholder_response)
    utils.save_log(utils.format_incoming_request_log(data))
    message = process_message.determine_response_message(data)
    telegram_api.send_message(message)
    return jsonify(placeholder_response)
