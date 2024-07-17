from django.shortcuts import render
import requests
import os
from django.contrib import messages

def get_weather(city):
     base_url = f'https://api.openweathermap.org/data/2.5/weather'
     api_key = os.getenv('API_KEY')
     parameters = {
          'q':city, 
          'appid':api_key, 
          'units':'metric', 
     }
     response = requests.get(base_url, params=parameters)
     if response.status_code == 200:
          return response.json()
     else:
          return None 




def index(request):
     city = request.GET.get('city', 'Kyiv')
     if not city:
          messages.error(request, "Please enter a city name.")
          return render(request, 'weatherapp/index.html')

     weather_data_result = get_weather(city)

     if weather_data_result is None:
          messages.error(request, f"City '{city}' not found.")
          return render(request, 'weatherapp/index.html')
     
     weather = weather_data_result['weather'][0]['main']
     weather_description = weather_data_result['weather'][0]['description']
     city_name = weather_data_result['name']
     country = weather_data_result['sys']['country']
     wind_speed = weather_data_result['wind']['speed']
     pressure = weather_data_result['main']['pressure']
     humidity = weather_data_result['main']['humidity']
     temperature = weather_data_result['main']['temp']
     icon = weather_data_result['weather'][0]['icon']
     icon_url = f'http://openweathermap.org/img/w/{icon}.png'

     return render(request, 'weatherapp/index.html', {
          'weather': weather,
          'weather_description': weather_description,
          'city': city_name,
          'country': country,
          'wind_speed': wind_speed,
          'pressure': pressure,
          'humidity': humidity,
          'temperature': temperature,
          'icon_url': icon_url,
    })