from html import escape
from bottle import Bottle, run, template, static_file, request
from urllib.request import urlopen
from urllib.error import HTTPError
import json


app = Bottle()

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


@app.route('/', method='GET')
@app.route('/', method='POST')
def index():
    city = request.forms.get('city', None)
    data = get_weather_data(escape(city))
    return template('./templates/index_page.html', **data )


@app.route('/static/<filename>')
def serve_static(filename):
    return static_file(filename, root='./static')



run(app, host='localhost', port=8125)