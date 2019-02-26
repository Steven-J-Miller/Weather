"""
Steven Miller
DSC 510
Final Project - Weather
Application will retrieve weather information from OpenWeatherMap and display information to the user
"""
import requests
from datetime import datetime


def get_weather_city(city):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid=297f37e36a2be40a8cb374f3a628a07d&units=imperial'
    try:
        r = requests.get(url)
        weather_data = r.json()
        return weather_data
    except requests.exceptions.RequestException as e:
        print(e)
        return 0


def get_weather_zip(zip_code, key, country='us'):
    url = f'http://api.openweathermap.org/data/2.5/weather?zip={zip_code},{country}&appid={key}&units=imperial'
    try:
        r = requests.get(url)
        weather_data = r.json()
        return weather_data
    except requests.exceptions.RequestException as e:
        print(e)
        return 0


def get_forecast_zip(zip_code, key, country='us'):
    url = f'http://api.openweathermap.org/data/2.5/forecast?zip={zip_code},{country}&appid={key}&units=imperial'
    try:
        r = requests.get(url)
        weather_data = r.json()
        return weather_data
    except requests.exceptions.RequestException as e:
        print(e)
        return 0


def parse_weather(weather):
    """Weather, temp, pressure, humidity, wind, rainfall"""
    city = weather['name']
    country = weather['sys']['country']
    desc = weather['weather'][0]['main']

    temp = weather['main']['temp']
    temp_c = temp - 273.15
    temp_f = temp_c*1.8+32

    pressure = weather['main']['pressure']
    humidity = weather['main']['humidity']

    sunrise = datetime.fromtimestamp(weather['sys']['sunrise'])
    sunrise = datetime.strftime(sunrise, '%I:%M %p')
    sunset = datetime.fromtimestamp(weather['sys']['sunset'])
    sunset = datetime.strftime(sunset, '%I:%M %p')

    print(desc, temp, pressure, humidity, sunrise, sunset)
    print(f"Weather Information For {city}, {country}")
    dashes = 26+len(city)+len(country)
    print(f'{"-"*dashes}')
    print(f'Currently: {desc}\nTemperature: {temp_f:.0f}°F ({temp_c:.0f}°C)')
    print(f'Humidity: {humidity}%')
    print(f"Wind Speed: {weather['wind']['speed']} m/s")
    print(f"Wind Direction: {weather['wind']['deg']}°")


def parse_forecast(forecast):
    print(f"Forecast for {forecast['city']['name']}")
    print('-'*80)
    for row in forecast['list']:
        time = datetime.fromtimestamp(row['dt'])
        time = datetime.strftime(time, '%a %m/%d | %I:%M %p')
        time = f"{time:^10}"

        if len(row['rain']) > 0:
            rain = row['rain']['3h']
        else:
            rain = 0
        temp = f"{row['main']['temp']:.0f}°"
        weather_status = row['weather'][0]['main']
        wind = f"{row['wind']['speed']} mph"
        print(f"| {time} | {temp} | {weather_status:^9} | {wind:^7} | "
              f"{row['clouds']['all']}% | {rain:.2f}\" |")


key = '297f37e36a2be40a8cb374f3a628a07d'  # temporarily hard-code, to be stored separately
weather = get_weather_zip(32819, key)
parse_weather(weather)

forecast = get_forecast_zip(32819, key)
parse_forecast(forecast)
"""
Sample Output
Weather information for London, GB
------------------------------
Current Weather: light intensity drizzle
Current Temperature: 212°F (100°C)
Atmospheric Pressure: 1012 hPa 
Humidity: 81%
Wind Speed: 4.1 m/s
Wind Direction: 80°
Rain (past hour): 1"

--------------------------------------------------------------------------------
| Date       | Time     | Temp. | Weather | Wind  | Cloud Cover | Rainfall     |
| Tues 02/26 | 04:00 AM | 48*   | Clear   | 4 m/s |     92%     |     0.02"    |
"""
