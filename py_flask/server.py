from html import escape
from flask import Flask, render_template, request
from urllib.request import urlopen
from urllib.error import HTTPError
import json


app = Flask(__name__)


def get_weather_data(city):
    try:
        url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid=b22d3e5ca3f379627e04afd55f5623c4&units=metric'.format(city)
        response = urlopen(url)
        raw_data = json.loads(response.read().decode('utf-8'))
        data = {
            'city': raw_data['name'],
            'weather': raw_data['weather'][0]['description'],
            'temp': raw_data['main']['temp']
        }
    except HTTPError:
        data = {
            'city' : 'Not Found',
            'weather' : '',
            'temp': ''
        }
    return data



@app.route('/', methods=['GET', 'POST'])
def index():
    city = request.form.get('city', None)
    data = get_weather_data(escape(city))
    return render_template('index_page.html', **data )


app.run(host='localhost', port=8124)