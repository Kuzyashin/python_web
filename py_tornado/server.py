from html import escape
from urllib.request import urlopen
from urllib.error import HTTPError
import json
from tornado import ioloop, web
from tornado.escape import json_decode
from tornado.web import StaticFileHandler


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



class Index(web.RequestHandler):
    city = ''
    data = get_weather_data(escape(city))
    def get(self):
        self.render('templates/index_page.html', **self.data)
    def post(self):
        city = self.request.body.decode().split('=')[-1]
        self.data = get_weather_data(escape(city))
        self.render('templates/index_page.html', **self.data)

def make_app():
    return web.Application([
        (r"/", Index),
        (r'/static/(.*)', StaticFileHandler, {
            "path": "static/"
        })
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8126)
    ioloop.IOLoop.current().start()