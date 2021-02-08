from django.shortcuts import render
import requests
from .models import WeatherAreas
from .forms import CityForm

# Create your views here.

def index(request):
    multiple_cities = WeatherAreas.objects.all()
    if request.method == 'POST':
        form = CityForm(request.POST)
        form.save()
    form = CityForm() # this is because after they submitting the form it will refresh it and make it blank..
    # if we won't use this the city name will be there itself...
    all_cities = []
    for cities in multiple_cities:
        print(cities)
        try:
            url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid=2330c697a2eb9a824770ffa65ca99977'
            # city = 'Tirupati'
            response = requests.get(url.format(cities.name)).json()
            if response['cod'] == '404':
                continue
            else:
                print(response)
            current_weather = {
                'city': cities.name,  # .name --> as defined in models
                'temperture': response['main']['temp'],
                'description': response['weather'][0]['description'],
                'icon': response['weather'][0]['icon']
            }
            all_cities.append(current_weather)
        except KeyError:
            continue


    # print(response)
    current_weather = {'current_weather': all_cities, 'form': form}
    return render(request, 'weatherapp/weathertemp.html', context=current_weather)
