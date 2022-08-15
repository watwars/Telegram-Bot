import requests
import os

api_key = os.environ.get("WEATHER_API_KEY")
base_url = "http://api.weatherapi.com/v1/"
key_parameter = "?key=" + api_key


failure_message = "Invalid use of /weather command"


def get_current_weather(city):
    url = base_url + "current.json" + key_parameter + "&q=" + city
    data = requests.get(url).json()
    current = data["current"]
    return f"""
    Current weather in {city.capitalize()}:
    Temperature: {round(current["temp_c"])}°C
    Feels like: {round(current["feelslike_c"])}°C
    Wind: {current["wind_kph"]}km/h
    Precipitation: {round(current["precip_mm"])}mm
    """


def determine_response(entire_text):
    if len(entire_text) < 3:
        return failure_message
    command = entire_text[1].lower()
    city = entire_text[2].lower()
    if command == "current":
        return get_current_weather(city)
