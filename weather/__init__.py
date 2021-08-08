import os
import requests
from dotenv import load_dotenv
from decimal import Decimal

load_dotenv()

BASE_URL = 'https://api.openweathermap.org/data/2.5/onecall'
API_KEY = os.getenv('OPEN_WEATHER_API_KEY')
LAT = 36.5
LONG = 137.8667

class Temp:
  current: Decimal
  min: Decimal
  max: Decimal

class Weather():
  def __init__(self) -> None:
    self.weather: str
    self.icon: str
    self.temp = Temp
    self.pressure: int
    self.humidity: int
    self.wind: int

  def get_weather(self):
    if API_KEY is None:
      print('OPEN_WEATHER_API_KEY is not found')
      return
    preload = { 'lat': LAT, 'lon': LONG, 'units': 'metric', 'exclude': 'minutely,hourly,alert', 'appid': API_KEY }
    r = requests.get(BASE_URL, params = preload)
    data = r.json()
    print(r.json())
    self.weather = data['current']['weather'][0]['main']
    self.icon = data['current']['weather'][0]['icon']
    self.temp.current = Decimal(str(data['current']['temp'])).quantize(Decimal('0.1'))
    self.temp.min = Decimal(str(data['daily'][0]['temp']['min'])).quantize(Decimal('0.1'))
    self.temp.max = Decimal(str(data['daily'][0]['temp']['max'])).quantize(Decimal('0.1'))
    self.pressure = data['current']['pressure']
    self.humidity = data['current']['humidity']
    self.wind = data['current']['wind_speed']
