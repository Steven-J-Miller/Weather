"""
Steven Miller
DSC 510
Final Project - Weather
Application will retrieve weather information from OpenWeatherMap and display information to the user
"""
import requests
from datetime import datetime


def get_weather_city(city, key):
    """Returns dictionary item of current weather of city by city name"""
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={key}&units=imperial'
    try:
        r = requests.get(url)
        weather_data = r.json()
        return weather_data
    except requests.exceptions.RequestException as e:
        print(e)
        return 0


def get_weather_zip(zip_code, key, country='us'):
    """Returns dictionary item of current weather of city by zip code"""
    url = f'http://api.openweathermap.org/data/2.5/weather?zip={zip_code},{country}&appid={key}&units=imperial'
    try:
        r = requests.get(url)
        weather_data = r.json()
        return weather_data
    except requests.exceptions.RequestException as e:
        print(e)
        return 0


def get_forecast_city(city, key, country='us'):
    """Returns dictionary item of weather forecast of city by city name"""
    url = f'http://api.openweathermap.org/data/2.5/forecast?q={city},{country}&appid={key}&units=imperial'
    try:
        r = requests.get(url)
        weather_data = r.json()
        return weather_data
    except requests.exceptions.RequestException as e:
        print(e)
        return 0


def get_forecast_zip(zip_code, key, country='us'):
    """Returns dictionary item of weather forecast of city by zip code"""
    url = f'http://api.openweathermap.org/data/2.5/forecast?zip={zip_code},{country}&appid={key}&units=imperial'
    try:
        r = requests.get(url)
        weather_data = r.json()
        return weather_data
    except requests.exceptions.RequestException as e:
        print(e)
        return 0


def parse_weather(weather):
    """Prints weather information"""
    if weather['cod'] == '404':  # returns error message if API call doesn't find valid city
        print(weather['message'])
        return 0

    city = weather['name']
    country = weather['sys']['country']
    desc = weather['weather'][0]['main']

    temp = weather['main']['temp']
    temp_c = (temp - 32)/1.8
    temp_f = temp

    humidity = weather['main']['humidity']

    sunrise = datetime.fromtimestamp(weather['sys']['sunrise'])
    sunrise = datetime.strftime(sunrise, '%I:%M %p')
    sunset = datetime.fromtimestamp(weather['sys']['sunset'])
    sunset = datetime.strftime(sunset, '%I:%M %p')

    if 'rain' in weather.keys():  # gets rainfall total if data exists, otherwise 0
        if len(weather['rain']) > 0:
            rain = weather['rain']['1h']
        else:
            rain = '0.00"'
    else:
        rain = 0

    print(f"Weather Information For {city}, {country}")
    dashes = 26+len(city)+len(country)
    print(f'{"-"*dashes}')
    print(f'Currently: {desc}\nTemperature: {temp_f:.0f}°F ({temp_c:.0f}°C)')
    print(f'Humidity: {humidity}%')
    print(f"Wind Speed: {weather['wind']['speed']} mph")
    print(f"Wind Direction: {weather['wind']['deg']}°")
    print(f"Rainfall past hour: {rain:.2f}\"")
    print(f"Sunrise: {sunrise}")
    print(f"Sunset: {sunset}")


def parse_forecast(forecast):
    """Prints forecast dictionary into a table"""
    if forecast['cod'] == '404':  # returns error message if API call doesn't find valid city
        print(forecast['message'])
        return 0
    print(f"Forecast for {forecast['city']['name']}")
    print('-'*80)
    print('|   Date    |   Time   | Temp|   Weather  |   Wind   | Cloud %  |   Rainfall   |')
    print('|'+'='*78+'|')
    for row in forecast['list']:
        time = datetime.fromtimestamp(row['dt'])
        time = datetime.strftime(time, '%a %m/%d | %I:%M %p')
        time = f"{time:^10}"
        cloud_cover = f"{row['clouds']['all']:.0f}%"

        if 'rain' in row.keys():
            if len(row['rain']) > 0:
                rain = f"{row['rain']['3h']:.2f}\""
            else:
                rain = '0.00"'
        else:
            rain = '0.00"'
        temp = f"{row['main']['temp']:.0f}°"
        weather_status = row['weather'][0]['main']
        wind = f"{row['wind']['speed']:.1f} mph"
        print(f'| {time} | {temp:^4} | {weather_status:^9} | {wind:^8} | {cloud_cover:^8} | {rain:^12} |')
    print('-' * 80)


if __name__ == "__main__":
    api_key = open('key.txt', 'r').read()
    while True:
        location = input("Welcome! To receive weather information please enter a zip code or city name, or 'exit' to exit: ")

        if location == 'exit':
            print("Thanks for stopping by!")
            break

        weather_info = input("Would you like to receive (c)urrent weather, a (f)orecast, or (b)oth? Use 'c', 'f', or 'b' to choose: ")

        if location.isnumeric():
            if weather_info[0] == 'c' or weather_info[0] == 'b':
                weather = get_weather_zip(location, api_key)
                parse_weather(weather)
            if weather_info[0] == 'f' or weather_info[0] == 'b':
                forecast = get_forecast_zip(location, api_key)
                parse_forecast(forecast)
        else:
            if weather_info[0] == 'c' or weather_info[0] == 'b':
                weather = get_weather_city(location, api_key)
                parse_weather(weather)
            if weather_info[0] == 'f' or weather_info[0] == 'b':
                forecast = get_forecast_city(location, api_key)
                parse_forecast(forecast)
