import requests

OPENWEATHER_URL = "http://api.openweathermap.org/data/2.5/weather"


def get_weather(city: str, api_key: str):
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric",
        "lang": "ru"
    }
    response = requests.get(OPENWEATHER_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        weather_info = {
            "temp": data['main']['temp'],
            "feels_like": data['main']['feels_like'],
            "description": data['weather'][0]['description'],
            "icon": data['weather'][0]['icon'],
            "humidity": data['main']['humidity'],
            "wind_speed": data['wind']['speed']
        }
        return weather_info
    else:
        if response.status_code == 404 and response.json()['message'] == 'city not found':
            raise Exception("Такого города не существует")
        else:
            print(response.text)
            raise Exception("Произошла ошибка. Попробуйте еще раз")


def get_weather_icon_url(icon_code):
    return f"http://openweathermap.org/img/w/{icon_code}.png"
