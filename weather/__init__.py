import os
import requests
from dotenv import load_dotenv
from decimal import Decimal

load_dotenv()

BASE_URL = 'https://api.openweathermap.org/data/2.5/weather'
API_KEY = os.getenv('OPEN_WEATHER_API_KEY')

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
    preload = { 'id': 1854186, 'units': 'metric', 'appid': API_KEY }
    r = requests.get(BASE_URL, params = preload)
    data = r.json()
    print(r.json())
    self.weather = data['weather'][0]['main']
    self.icon = data['weather'][0]['icon']
    self.temp.current = Decimal(str(data['main']['temp'])).quantize(Decimal('0.1'))
    self.temp.min = Decimal(str(data['main']['temp_min'])).quantize(Decimal('0.1'))
    self.temp.max = Decimal(str(data['main']['temp_max'])).quantize(Decimal('0.1'))
    self.pressure = data['main']['pressure']
    self.humidity = data['main']['humidity']
    self.wind = data['wind']['speed']
