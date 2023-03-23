import requests
import os
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv("/Users/adamstyles/Documents/Dev/100 Days - Python/RainAlert/.env")

account_sid = os.environ.get("ACCOUNT_SID")
auth_token = os.environ.get("AUTH_TOKEN")


api_key = os.environ.get("API_KEY")
OWM_Endpoint = "https://api.openweathermap.org/data/2.5/forecast"

twilio_number = os.environ.get("TWILIO_NUMBER")
my_number = os.environ.get("MY_NUMBER")

weather_params = {
    "lat": 39.952583,
    "lon": -75.165222,
    "appid": api_key,
    "units": "imperial"
}
response = requests.get(url=OWM_Endpoint, params=weather_params)
response.raise_for_status()
weather_data = response.json()
weather_list = weather_data["list"][:4]

will_rain = False

for weather_dict in weather_list:
    weather = weather_dict["weather"]
    condition_code = weather[0]["id"]
    if int(condition_code) < 700:
        will_rain = True

if will_rain:
    client = Client(account_sid, auth_token)
    message = client.messages \
        .create(
            body="It's going to rain today, bring an umbrella.",
            from_=twilio_number,
            to=my_number
        )

    print(message.status)
