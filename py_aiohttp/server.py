from html import escape
from urllib.request import urlopen
from urllib.error import HTTPError
import json
from aiohttp import web
import aiohttp_jinja2
import jinja2


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



async def index(request):
    data = await request.post()
    try:
        city = data['city']
    except Exception:
        city = ''
    data = get_weather_data(escape(city))
    response = aiohttp_jinja2.render_template('index_page.html',
                                              request,
                                              data)
    response.headers['Content-Language'] = 'en'
    return response


app = web.Application()
aiohttp_jinja2.setup(app,
    loader=jinja2.FileSystemLoader('./templates/'))
app.add_routes([web.get('/', index),
                web.post('/', index)
                ])

app.add_routes([web.static('/static', './static')])

web.run_app(app, path='localhost', port=8127)
