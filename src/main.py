import weather_api

def main():
    location_info = weather_api.get_location('02760')
    lat = location_info.get('lat')
    lon = location_info.get('lon')

    weather_info = weather_api.get_weather_forecast(lat, lon)

    print(f"{weather_info}")


if __name__ == "__main__":
    main()