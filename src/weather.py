
import argparse

from diagram import generate_mermaid_markdown
from weather_api import get_weather_forecast, get_location

def main():
    parser = argparse.ArgumentParser(prog='Weather',
                                     description='Shows the current weather for the given location and generates a mermaid markdown file based on that data.')
    parser.add_argument("-z", "--zip_code", type = int, help="The zip code for the desired weather forecast. Required option.")
    parser.add_argument("-c", "--country_code", help="Country code. Optional for U.S.")
    parser.add_argument("--api_key", help="Valid API key for weather api.")

    
    args = parser.parse_args()
    cc = None
    zip_code = None
    api_key = None

    if args.country_code:
        cc = args.country_code

    zip_code = args.zip_code
    if not args.zip_code:
        print("Zip code is a required option")
        exit(1)

    api_key  = args.api_key
    if not api_key:
        print("A valid API key is required.")
        exit(1)

    try:
        location = get_location(zip_code, country_code = cc, api_key = api_key)
    except Exception as e:
        print("Unable to get the location info at this time. Please try later.")
        print(e)
        exit(1)

    try:
        forecast = get_weather_forecast(lat=location.get('lat'), lon = location.get('lon'), api_key = api_key)
    except Exception as e:
        print("Having a problem getting the weather right now. Please try later.")
        print(e)
        exit(1)

    place = forecast.get('name')
    temp  = forecast.get('main').get('temp')
    weather = forecast.get('weather')[0].get('description')
    print(f"Weather for {place} is {weather}. Current temp is {temp}")

    generate_mermaid_markdown(zip_code, country_code=cc, api_key = api_key)

if __name__ == "__main__":
    main()