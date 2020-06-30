import httpretty
import json
import functools
import numpy as np
from urllib.parse import urljoin
from os import path
from django.conf import settings
from .factories.temperature import temperature_factory, weather_factory


def mock_api(fn):
    @functools.wraps(fn)
    @httpretty.activate
    def wrapper(*args, **kwargs):
        register_uri()
        response = fn(*args, **kwargs)
        return response
    return wrapper


def register_uri():
    api_list = fake_api()
    for api in api_list:
        httpretty.register_uri(
            httpretty.GET,
            uri=api['uri'],
            body=api['body']
        )


def make_path(resource='', version='v0'):
    today = np.datetime64('today')
    datetime_delta = np.timedelta64(1, 'D')
    yesterday = today - datetime_delta
    date_ini = str(yesterday)
    date_end = str(today)
    return path.join(version, resource, date_ini, date_end)


def mock_uri(resource=''):
    url = getattr(settings, 'API_URL')
    uri = urljoin(url, make_path(resource))
    return uri


temperature_min = dict(temp_min=temperature_factory(6))


temperature_max = dict(temp_max=temperature_factory(6))


weather = weather_factory()


def fake_api():
    return [
        {
            'uri': mock_uri('temperature_min'),
            'body': json.dumps(temperature_min)
        },
        {
            'uri': mock_uri('temperature_max'),
            'body': json.dumps(temperature_max)
        },
        {
            'uri': getattr(settings, 'API_URL'),
            'body': json.dumps(weather)
        }
    ]
