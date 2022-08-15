import os
from math import *

from helpers import run_code, utils, stocks, weather

ENV = os.environ.get("ENV")


def calculate_equation(entire_text):
    equation = ' '.join(entire_text[1:])
    try:
        return eval(equation)
    except Exception as e:
        return "Invalid equation: " + str(e)


def determine_response_message(update):
    if ENV == "dev":
        print(update)  # for debugging
    message = update["message"]
    entire_text = message["text"].split(' ')
    command = entire_text[0].lower()
    chat_id = message["chat"]["id"]
    response_text = ""

    if command == "/start":
        response_text = f"Hello {utils.get_user_name(message)}! Nice to meet you! You can use the /help command to find more about my features."
    elif command == '/greet':
        response_text = f"Hello {utils.get_user_name(message)}! Nice to meet you!"
    elif command == '/help':
        # NEED UPDATE
        response_text = "You can use the following commands: /greet, /help, /python, /cpp, /javascript"
    elif command == '/python':
        response_text = run_code.run_interpreted_code(entire_text, "python")
    elif command == '/javascript':
        response_text = run_code.run_interpreted_code(
            entire_text, "javascript")
    elif command == '/cpp':
        response_text = run_code.run_compiled_code(entire_text, "c++")
    elif command == '/calc':
        response_text = calculate_equation(entire_text)
    elif command == "/stock":
        response_text = stocks.determine_response(entire_text)
    elif command == "/weather":
        response_text = weather.determine_response(entire_text)
    else:
        response_text = "Invalid command, use /help to see the list of commands"

    return {
        "chat_id": chat_id,
        "text": response_text
    }
