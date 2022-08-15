import finnhub
import os
import datetime
from helpers import utils


env = os.environ.get("ENV")
api_key = os.environ.get("FINNHUB_API_KEY")
finnhub_client = finnhub.Client(api_key)


def get_stock_quote(symbol):
    try:
        stock_price_info = finnhub_client.quote(symbol)
        return f"""
        Here are the info for {symbol}:
        Current Price: ${stock_price_info['c']}
        Change: ${stock_price_info['d']}
        Percent Change: {stock_price_info['dp']}%
        High: ${stock_price_info['h']}
        Low: ${stock_price_info['l']}
        Open: ${stock_price_info['o']}
        Previous: ${stock_price_info['pc']}
        """
    except Exception as e:
        utils.save_log(
            {"action": "get_stock_quote", "error": str(e)})
        return "Something went wrong. Please try again later"


def get_stock_news(symbol):
    today = datetime.date.today()
    seven_days_ago = today - datetime.timedelta(days=7)
    try:
        news_info = finnhub_client.company_news(
            symbol, _from=str(seven_days_ago), to=str(today))
        if len(news_info) == 0:
            return "No news found for the given symbol"
        news_string = f"Here are the latest top news for {symbol}:\n\n"
        latest_news = news_info[:10]
        for news in latest_news:
            news_string += f"{news['headline']}\n"
            news_string += f"{news['url']}\n\n"
        return news_string
    except Exception as e:
        utils.save_log(
            {"action": "get_stock_news", "error": str(e)})
        return "Something went wrong. Please try again later"


def get_recommendation_trends(symbol):
    try:
        trends = finnhub_client.recommendation_trends(symbol)
        if len(trends) == 0:
            return "No recommendation trends found for the given symbol"
        latest_trend = trends[0]
        return f"""
            Recommendations for {symbol} -  {latest_trend['period']}:
            Strong Buy: {latest_trend['strongBuy']}
            Buy: {latest_trend['buy']}
            Hold: {latest_trend['hold']}
            Sell: {latest_trend['sell']}
            Strong Sell: {latest_trend['strongSell']}
        """
    except Exception as e:
        utils.save_log(
            {"action": "get_recommendation_trends", "error": str(e)})
        return "Something went wrong. Please try again later"


failure_message = "Invalid use of the /stock command"


def determine_response(entire_text):
    if len(entire_text) < 3:
        return failure_message
    command = entire_text[1].lower()
    if command == 'quote':
        return get_stock_quote(entire_text[2].upper())
    elif command == "news":
        return get_stock_news(entire_text[2].upper())
    elif command == "trends":
        return get_recommendation_trends(entire_text[2].upper())
    else:
        return failure_message
