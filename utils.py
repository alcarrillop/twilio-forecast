import pandas as pd
from twilio.rest import Client
from twilio_config import FROM_WP_NUMBER, TO_WP_NUMBER
from datetime import datetime
import requests
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json


def get_date():

    init_date = datetime.now()
    input_date = init_date.strftime("%Y-%m-%d")
    format_date = init_date.strftime("%-d de %B")

    return input_date, format_date

def request_wapi(api_key,query):

    url_clima = 'http://api.weatherapi.com/v1/forecast.json?key='+api_key+'&q='+query+'&days=1&aqi=no&alerts=no'

    try :
        response = requests.get(url_clima).json()
    except Exception as e:
        print(e)

    return response

def get_forecast(response,i):
    
    index = int(response['forecast']['forecastday'][0]['hour'][i]['time'].split()[1].split(':')[0])
    fecha = response['forecast']['forecastday'][0]['hour'][i]['time'].split()[0]
    hora = response['forecast']['forecastday'][0]['hour'][i]['time'].split()[1]
    condicion = response['forecast']['forecastday'][0]['hour'][i]['condition']['text']
    tempe = float(response['forecast']['forecastday'][0]['hour'][i]['temp_c'])
    rain = response['forecast']['forecastday'][0]['hour'][i]['will_it_rain']
    prob_rain = response['forecast']['forecastday'][0]['hour'][i]['chance_of_rain']
    
    return index,fecha,hora,condicion,tempe,rain,prob_rain

def create_df(data):

    col = ['Count','Date','Hour','Condition','Temp','Rain','Chance of Rain']
    df = pd.DataFrame(data,columns=col)
    df = df.sort_values(by = 'Count',ascending = True)

    df_rain =  df[(df['Rain']==1) & (df['Count']>4) & (df['Count']< 22)]
    df_rain = df_rain[['Hour','Condition', 'Temp']]
    df_rain.set_index('Hour', inplace = True)

    return df_rain

def send_message(TWILIO_ACCOUNT_SID,TWILIO_AUTH_TOKEN,format_date,df,query):

    account_sid = TWILIO_ACCOUNT_SID
    auth_token = TWILIO_AUTH_TOKEN

    client = Client(account_sid, auth_token)

    content = (
    "Hi handsome!\n"
    f"The forecast for today *{format_date}* in {query} is {round(df['Temp'].mean(), 2)} °C\n"
    f"*Max Temperature:* {df['Temp'].max()} °C\n"
    f"*Min Temperature:* {df['Temp'].min()} °C\n\n"
    "Chance of rain could occurs in:\n\n"
    f"{str(df)}"
    )

    message = client.messages \
                    .create(
                        body= content,
                        from_=FROM_WP_NUMBER,
                        to=TO_WP_NUMBER
                    )

    return message.sid
