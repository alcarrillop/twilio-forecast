import pandas as pd
from twilio.rest import Client
from twilio_config import FROM_WP_NUMBER, TO_WP_NUMBER
from datetime import datetime
import requests

def get_date():
    init_date = datetime.now()
    input_date = init_date.strftime("%Y-%m-%d")
    format_date = init_date.strftime("%-d de %B")
    return input_date, format_date

def request_wapi(api_key, query):
    url_clima = f'http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={query}&days=1&aqi=no&alerts=no'
    try:
        response = requests.get(url_clima)
        response.raise_for_status()  # Raise HTTPError for bad responses
        return response.json()
    except (ConnectionError, requests.exceptions.RequestException) as e:
        print(f"Error fetching weather data: {e}")
        return None

def get_forecast(response, i):
    forecast_hour = response['forecast']['forecastday'][0]['hour'][i]
    time = forecast_hour['time']
    index = int(time.split()[1].split(':')[0])
    date = time.split()[0]
    hour = time.split()[1]
    condition = forecast_hour['condition']['text']
    temp = float(forecast_hour['temp_c'])
    rain = forecast_hour['will_it_rain']
    chance_of_rain = forecast_hour['chance_of_rain']
    return index, date, hour, condition, temp, rain, chance_of_rain

def create_df(data):
    columns = ['Count', 'Date', 'Hour', 'Condition', 'Temp', 'Rain', 'Chance of Rain']
    df = pd.DataFrame(data, columns=columns)
    df = df.sort_values(by='Count', ascending=True)
    df_rain = df[(df['Rain'] == 1) & (df['Count'] > 4) & (df['Count'] < 22)]
    df_rain = df_rain[['Hour', 'Condition', 'Temp']]
    df_rain.set_index('Hour', inplace=True)
    return df_rain

def send_message(account_sid, auth_token, format_date, df, query):
    client = Client(account_sid, auth_token)
    content = (
        f"The forecast for today *{format_date}* in {query} is {round(df['Temp'].mean(), 2)} °C\n"
        f"*Max Temperature:* {df['Temp'].max()} °C\n"
        f"*Min Temperature:* {df['Temp'].min()} °C\n\n"
        "Chance of rain could occur in:\n\n"
        f"{str(df)}"
    )
    message = client.messages.create(body=content, from_=FROM_WP_NUMBER, to=TO_WP_NUMBER)
    return message.sid
