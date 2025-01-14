import requests

class WeatherAPI:
    def __init__(self, api_key, latitude, longitude):
        self.api_key = api_key
        self.latitude = latitude
        self.longitude = longitude
        self.base_url = "https://api.openweathermap.org/data/3.0/onecall" # Note the 3.0 for One Call API

    def get_weather_forecast(self):
        """Get the hyperlocal weather forecast using latitude and longitude."""
        url = f"{self.base_url}?lat={self.latitude}&lon={self.longitude}&appid={self.api_key}&units=metric" # Added units=metric
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to retrieve weather data: {response.text}")
            return None

    def is_rain_imminent(self, forecast_data, hours_ahead=3):
        """
        Check if rain is expected within the next few hours in the hyperlocal forecast.
        """
        if not forecast_data:
            return False

        # Check hourly forecast data
        for forecast in forecast_data.get("hourly", []):
            # Check within the specified timeframe
            if forecast["dt"] <= forecast_data["hourly"][0]["dt"] + hours_ahead * 3600:
                if any(weather["main"] == "Rain" for weather in forecast.get("weather", [])):
                    print("Rain is expected soon!")
                    return True
        print("No rain expected in the near future.")
        return False