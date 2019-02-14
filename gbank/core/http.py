import requests
import pickle
from bs4 import BeautifulSoup
from json.decoder import JSONDecodeError
from fake_useragent import UserAgent

from ..helper import DictToObj


class Http(object):

    def __init__(self):
        self._req_session = requests.Session()

        self._req_session.headers.update({
            'User-agent': UserAgent(verify_ssl=False).random
        })

    def set_requests_session(self, session: requests.Session):
        self._req_session = session

    def get_requests_session(self):

        return self._req_session

    def save_cookies(self, path: str):
        with open(path, 'wb+') as wrt:
            pickle.dump(self._req_session.cookies, wrt)

    def load_cookies(self, path: str):
        with open(path, 'rb') as rd:
            cookies = pickle.load(rd)

        # apply to current session now.
        self._req_session.cookies = cookies

    def _source(self, url: str, _type: str = "get", **data):
        req = getattr(self._req_session, _type)(url, **data)

        # get status code
        code = req.status_code
        # is status ok
        is_ok = req.ok
        # plain text response
        raw_response = req.text
        # bs response
        response = self._convert_to_bs(req.text)
        # json
        try:
            json = req.json()
        except (JSONDecodeError):
            json = None

        return {
            'status_code': code,
            'ok': is_ok,
            'raw_response': raw_response,
            'response': response,
            'json': json,
            'requests_response': req
        }

    @staticmethod
    def _convert_to_bs(raw_response: str, _to_convert: str = "html.parser"):

        return BeautifulSoup(raw_response, _to_convert)

    def __getattr__(self, name):
        if 'source' in name:
            method = name.replace('_source', '')

            def wrapper(*names, **kwarg):
                kwarg.update(_type=method)
                return DictToObj(self._source(*names, **kwarg))

            return wrapper
        else:
            if hasattr(super(), '__getattr__'):
                return super().__getattr__(name)
            else:
                raise AttributeError("No Such Attribute")
