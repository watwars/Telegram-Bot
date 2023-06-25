
import datetime
import json
from helpers import custom_types


def format_date(time_stamp):
    return str(datetime.datetime.fromtimestamp(time_stamp))


def get_user_name(message):
    user_name = message["from"]["first_name"] + \
        " " + message["from"]["last_name"]
    return user_name


def save_log(data):
    date = datetime.date.today()
    log_file_name = f"logs/{date}.log"
    with open(log_file_name, 'a', encoding='utf-8') as f:
        f.write(str(data) + "\n")


recent_file_name = "processed.json"


def fetch_recent_processed_updates():
    with open(recent_file_name, "r") as f:
        data = f.read()
        processed = json.loads(data)
    return processed


recent = fetch_recent_processed_updates()


def did_processed_message(data):
    if "message" not in data:
        return True
    update_id = data["update_id"]
    chat_id = str(data["message"]["chat"]["id"])
    if chat_id not in recent or update_id != recent[chat_id]:
        recent[chat_id] = update_id
        with open(recent_file_name, 'w') as f:
            f.write(json.dumps(recent))
        return False
    return True


def format_incoming_request_log(data):
    message = data["message"]
    return {
        "update_id": data["update_id"],
        "chat_id": message["chat"]["id"],
        "date": format_date(message["date"]),
        "user_name": get_user_name(message),
        "text": message["text"],
    }


def parse_error_message(err):
    lines = err.split("\n")
    for line in lines:
        if "Error" in line:
            return line
    return "Unknown error"


LanguageSpecs = custom_types.LanguageSpecs


def get_language_specs(language):
    if language == "javascript":
        return LanguageSpecs(["node"], "js")
    elif language == "python":
        return LanguageSpecs(["python3"], "py")
    elif language == "c++":
        return LanguageSpecs(["g++", "-std=c++17"], "cpp")
    else:
        return None
