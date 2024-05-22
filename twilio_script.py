from twilio_config import *
from utils import get_date, request_wapi, get_forecast, create_df, send_message

def main():
    query = 'Bogota'
    api_key = API_KEY_WAPI

    input_date, format_date = get_date()
    response = request_wapi(api_key, query)

    if response:
        data = [get_forecast(response, i) for i in range(24)]
        df_rain = create_df(data)
        message_id = send_message(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, format_date, df_rain, query)
        print(f'Message sent successfully with ID: {message_id}')
    else:
        print("Failed to retrieve weather data")

if __name__ == "__main__":
    main()
