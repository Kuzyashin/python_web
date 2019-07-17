from html import escape
from urllib.error import HTTPError
import json
from tornado import ioloop, web
from tornado.escape import json_decode
from tornado.httpclient import AsyncHTTPClient
from tornado.web import StaticFileHandler



async def get_weather_data(city):
    http_client = AsyncHTTPClient()
    try:
        url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid=b22d3e5ca3f379627e04afd55f5623c4&units=metric'.format(city)
        response = await http_client.fetch(url)
        raw_data = json.loads(response.body.decode('utf-8'))
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
    async def get(self):
        city = 'Moscow'
        data = await get_weather_data(escape(city))
        self.render('templates/index_page.html', **data)
    async def post(self):
        city = self.request.body.decode().split('=')[-1]
        data = await get_weather_data(escape(city))
        self.render('templates/index_page.html', **data)

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