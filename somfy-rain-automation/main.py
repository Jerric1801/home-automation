import time
from dotenv import load_dotenv
import os

from somfy.api import SomfyAPI
from somfy.commands import SomfyCommands
from weather.weather_api import WeatherAPI

# Load environment variables
load_dotenv()

# Somfy Configuration
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
DEVICE_URL = os.getenv("DEVICE_URL")
DEVICE_NAME = os.getenv("DEVICE_NAME")

# Weather API Configuration
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
LATITUDE = os.getenv("LATITUDE")
LONGITUDE = os.getenv("LONGITUDE")

# Check interval in seconds (e.g., every 15 minutes)
CHECK_INTERVAL = 900

def main():
    try:
        # Initialize Somfy API
        somfy_api = SomfyAPI(USERNAME, PASSWORD, DEVICE_URL)
        somfy_commands = SomfyCommands(somfy_api, DEVICE_NAME)

        # Initialize Weather API
        weather_api = WeatherAPI(WEATHER_API_KEY, LATITUDE, LONGITUDE)

        while True:
            # Get weather forecast
            forecast_data = weather_api.get_weather_forecast()

            # Check for rain
            if weather_api.is_rain_imminent(forecast_data):
                somfy_commands.close_blinds()

            # Wait for the next check
            print(f"Waiting for {CHECK_INTERVAL} seconds before the next check...")
            time.sleep(CHECK_INTERVAL)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()