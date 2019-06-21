import re
from html import escape
from string import Template
from urllib.parse import parse_qs
from wsgiref.simple_server import make_server
import pprint
from urllib import request, error
import json

def get_req_data(environ):
    try:
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
    except ValueError:
        request_body_size = 0
    request_body = environ['wsgi.input'].read(request_body_size)
    return parse_qs(request_body.decode('utf-8'))


def get_weather_data(city):
    try:
        url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid=b22d3e5ca3f379627e04afd55f5623c4&units=metric'.format(city)
        response = request.urlopen(url)
        raw_data = json.loads(response.read().decode('utf-8'))
        data = {
            'city': raw_data['name'],
            'weather': raw_data['weather'][0]['description'],
            'temp': raw_data['main']['temp']
        }
    except error.HTTPError:
        data = {
            'city' : 'Not Found',
            'weather' : '',
            'temp': ''
        }
    return data



def index(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    d = get_req_data(environ)
    city = escape(d.get('city', ['Moscow'])[0])
    data = get_weather_data(city)
    with open('./templates/index_page.html') as template_file:
        template = Template(template_file.read())
    return [bytes(template.substitute(data), encoding='utf-8')]


def not_found(environ, start_response):
    start_response('404 NOT FOUND', [('Content-Type', 'text/plain')])
    return [bytes('Not Found', encoding='utf-8')]


def serve_static_css(environ, start_response, file):
    try:
        with open('static/{}'.format(file.split('/')[-1]), 'rb') as f:
            file_data = f.read()
            start_response('200 OK', [('Content-Type', 'text/css')])
            return [file_data]
    except FileNotFoundError:
        return not_found(environ, start_response)


def serve_static_img(environ, start_response, file):
    try:
        with open('static/{}'.format(file).split('/')[-1], 'rb') as f:
            file_data = f.read()
            start_response('200 OK', [('Content-Type', 'text/image/jpeg')])
            return [file_data]
    except FileNotFoundError:
        return not_found(environ, start_response)


urls = [
    (r'^$', index),
]

files = [
    (r'.*\.jpe?g', serve_static_img),
    (r'.*\.css', serve_static_css)
]


def application(environ, start_response):
    path = environ.get('PATH_INFO', '').lstrip('/')
    for regex, callback in urls:
        match = re.search(regex, path)
        if match is not None:
            return callback(environ, start_response)
    for regex, callback in files:
        match = re.search(regex, path)
        if match is not None:
            return callback(environ, start_response, path)
    return not_found(environ, start_response)


httpd = make_server('', 8123, application)
print("Serving on port 8123...")
httpd.serve_forever()
