from flask import Flask, render_template, request
import requests
from datetime import datetime
import pytz
from tzwhere import tzwhere

app = Flask(__name__, template_folder='templates')


def kelvin_to_celcius(temp: float) -> int:
    k = float(temp)
    c = k - 273.15
    return int(c)


def timezone(lt, lng):
    w = tzwhere.tzwhere()
    return datetime.now(pytz.timezone(w.tzNameAt(lt, lng))).strftime('%I:%M %p')


def api_weather(town):
    resp = requests.get(
        f'https://openweathermap.org/data/2.5/find?q={town}&appid=439d4b804bc8187953eb36d2a8c26a02&units=metric')
    data = resp.json()
    resp.raise_for_status()
    main_data = data['list'][0]['main']
    weather = data['list'][0]['weather'][0]

    coord = data['list'][0]['coord']
    lat = coord['lat']
    lon = coord['lon']
    time = timezone(lat,lon)
    feels_like = kelvin_to_celcius(main_data['feels_like'])
    humidity = main_data['humidity']
    temp = kelvin_to_celcius(main_data['temp'])
    name = data['list'][0]['name']
    description = weather['description']
    icon = f'https://openweathermap.org/img/wn/{weather["icon"]}@2x.png'
    wind = data['list'][0]['wind']['speed']
    return time, feels_like, humidity, temp, description, icon, wind, name


@app.route('/', methods=["POST", "GET"])
def homepage():
    if request.method == 'POST':
        town_name = request.form['town']
        time, feels_like, humidity, temp, description, icon, wind, name = api_weather(town_name)
        context = {
            'name': name,
            'time': time,
            'feels_like': feels_like,
            'humidity': humidity,
            'temp': temp,
            'description': description,
            'icon': icon,
            'wind': wind
        }

        return render_template('main.html', **context)
    else:
        time, feels_like, humidity, temp, description, icon, wind, name = api_weather('London')
        context = {
            'name': name,
            'time': time,
            'feels_like': feels_like,
            'humidity': humidity,
            'temp': temp,
            'description': description,
            'icon': icon,
            'wind': wind
        }
        return render_template('main.html', **context)


if __name__ == '__main__':
    TEMPLATES_AUTO_RELOAD = True
    app.run(use_reloader=True)
