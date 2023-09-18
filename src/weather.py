
import argparse
from multiprocessing.context import ForkContext
from diagram import generate_mermaid_markdown
from weather_api import get_weather_forecast, get_location

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-z", "--zip_code", type = int, help="The zip code for the desired weather forecast. Required option.")
    parser.add_argument("-c", "--country_code", help="Country code. Optional for U.S.")

    
    args = parser.parse_args()
    cc = None
    zip_code = None

    if args.country_code:
        cc = args.country_code

    if args.zip_code:
        zip_code = args.zip_code
    else:
        print("Zip code is a required option")
        exit(1)
    
    try:
        location = get_location(zip_code, country_code = cc)
    except Exception as e:
        print("Unable to get the location info at this time. Please try later.")
        exit(1)

    try:
        forecast = get_weather_forecast(lat=location.get('lat'), lon = location.get('lon'))
    except Exception as e:
        print("Having a problem getting the weather right now. Please try later.")
        exit(1)

    place = forecast.get('name')
    temp  = forecast.get('main').get('temp')
    weather = forecast.get('weather')[0].get('description')
    print(f"Weather for {place} is {weather}. Current temp is {temp}")

    generate_mermaid_markdown(zip_code, country_code=cc)

if __name__ == "__main__":
    main()