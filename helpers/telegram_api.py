import requests
from dotenv import load_dotenv
import os
from helpers import utils

load_dotenv()
BASE_URL = f'https://api.telegram.org/bot{os.environ.get("API_TOKEN")}/'


def set_webhook(attempts=5):
    requests_url = BASE_URL + 'setWebhook'
    requests_data = {
        "url": os.environ.get("WEBHOOK_URL"),
        "drop_pending_updates": True,
        "max_connections": 2
    }
    response = requests.post(requests_url, json=requests_data).json()
    print(response)
    ok = response["ok"]
    if ok:
        return True
    if not ok and attempts > 0:
        return set_webhook(attempts-1)
    return False


def get_webhook_info():
    requests_url = BASE_URL + 'getWebhookInfo'
    response = requests.get(requests_url).json()
    ok = response["ok"]
    return ok


def send_message(message):
    request_url = BASE_URL + 'sendMessage'
    response = requests.post(request_url, json=message).json()
    ok = response["ok"]
    if not ok:
        print(response)
    log = {
        "action": "send_message",
        "ok": ok,
        "message": message["text"]
    }
    utils.save_log(log)
