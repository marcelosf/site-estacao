import httpretty
import json
import functools
import numpy as np
from urllib.parse import urljoin
from os import path
from django.conf import settings


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


def make_path(resource=''):
    today = np.datetime64('today')
    datetime_delta = np.timedelta64(1, 'D')
    yesterday = today - datetime_delta
    date_ini = str(yesterday)
    date_end = str(today)
    return path.join('/v0/', resource, date_ini, date_end)


def mock_uri(resource=''):
    url = getattr(settings, 'API_URL')
    uri = urljoin(url, make_path(resource))
    return uri


def fake_api():
    return [
        {
            'uri': mock_uri('temperature_min'),
            'body': json.dumps({
                'temp_min':  [
                    {'date': '2020-01-01 00:13:00', 'temp': '12'},
                    {'date': '2020-01-01 00:14:00', 'temp': '23'},
                    {'date': '2020-01-01 00:15:00', 'temp': '20'},
                    {'date': '2020-01-02 00:16:00', 'temp': '19'},
                    {'date': '2020-01-02 00:17:00', 'temp': '18'},
                    {'date': '2020-01-02 00:17:00', 'temp': '12'},
                ]
            })
        },
        {
            'uri': mock_uri('temperature_max'),
            'body': json.dumps({
                'temp_min':  [
                    {'date': '2020-01-01 00:13:00', 'temp': '12'},
                    {'date': '2020-01-01 00:14:00', 'temp': '23'},
                    {'date': '2020-01-01 00:15:00', 'temp': '20'},
                    {'date': '2020-01-02 00:16:00', 'temp': '19'},
                    {'date': '2020-01-02 00:17:00', 'temp': '18'},
                    {'date': '2020-01-02 00:17:00', 'temp': '12'},
                ]
            })
        },
        {
            'uri': getattr(settings, 'API_URL'),
            'body': json.dumps({
                        "data": "10/04/2020 - 13:20",
                        "temperatura_ar": "20",
                        "temperatura_orvalho": "10",
                        "ur": "80",
                        "temperatura_min": "10",
                        "temperatura_max": "20",
                        "vento": "calmo",
                        "pressao": "129",
                        "visibilidade_min": "4",
                        "visibilidade_max": "10",
                        "nuvens_baixas": "Ac/As-10/10",
                        "nuvens_medias": "Am/As-20/20",
                        "nuvens_altas": "Am/As-20/20"
            })
        }
    ]
