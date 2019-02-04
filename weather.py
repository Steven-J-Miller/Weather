"""
Steven Miller
DSC 510
Final Project - Weather
Application will retrieve weather information from OpenWeatherMap and display information to the user
"""
import requests
from datetime import datetime

def get_weather_city(city):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid=297f37e36a2be40a8cb374f3a628a07d'
    try:
        r = requests.get(url)
        weather_data = r.json()
        return weather_data
    except requests.exceptions.RequestException as e:
        print(e)
        return 0


def get_weather_zip(zip_code, country='us'):
    url = f'api.openweathermap.org/data/2.5/weather?zip={zip_code},{country}&appid=297f37e36a2be40a8cb374f3a628a07d'
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

key = '297f37e36a2be40a8cb374f3a628a07d'  # temporarily hard-code, to be stored separately

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
"""