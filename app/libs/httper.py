# -*- coding: utf-8 -*-

import requests
from requests import RequestException


class Http(object):
    @staticmethod
    def get(url, return_json=True):
        try:
            resp = requests.get(url)
            if resp.status_code != 200:
                return {} if return_json else ''
            return resp.json() if return_json else resp.text
        except RequestException :
            return {} if return_json else ''
        except Exception:
            return {} if return_json else ''
