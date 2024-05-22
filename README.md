# Twilio Forecast

Twilio Forecast is a Python application that sends weather forecasts via SMS using the Twilio API. This project demonstrates how to integrate weather data with Twilio to automate SMS notifications.

## Features

- Fetches weather forecasts from a weather API
- Sends weather forecasts via SMS using Twilio
- Configurable recipient phone numbers and message schedules

## Requirements

- Python 3.6+
- Twilio Account (with SID and Auth Token)
- Weather API Key

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/alcarrillop/twilio_forecast.git
    cd twilio_forecast
    ```

2. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

## Configuration

1. Create a `twilio_config.py` file in the project root with your Twilio credentials:
    ```python
    TWILIO_ACCOUNT_SID = 'your_account_sid'
    TWILIO_AUTH_TOKEN = 'your_auth_token'
    TWILIO_PHONE_NUMBER = 'your_twilio_phone_number'
    RECIPIENT_PHONE_NUMBER = 'recipient_phone_number'
    WEATHER_API_KEY = 'your_weather_api_key'
    ```

2. Update the `twilio_script.py` file with your preferred weather API endpoint and parameters.

## Usage

Run the script to send a weather forecast SMS:
```sh
python twilio_script.py
