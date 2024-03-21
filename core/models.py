from enum import Enum
import requests


class GroupType(Enum):
    DEFAULT = "GENERAL"
    FILTERS = "Filters options"
    INPUT = "Input options"


class PluginType(Enum):
    PARSER = 0
    FILTER = 1


class HTTPMethod(Enum):
    GET = 'GET'
    POST = 'POST'


class SessionBaseModel(object):
    _headers: dict = dict()
    _payload: str = None
    _url: str = None
    _response: requests.Response = None
    _verbose: bool = False
    _prefix_val: str = None

    def __init__(self, url: str, variable: str, verbose: bool = False):
        self._prefix_val = variable
        self._url = url.replace("FUZZ", variable) if "FUZZ" in url else url + variable
        self._verbose = verbose

    @property
    def get_headers(self):
        return self._headers

    def parser_fuzz_replace(self, data: str) -> str:
        return data.replace("FUZZ", self._prefix_val if "FUZZ" in data else data)

    def add_headers(self, key, value):
        value = self.parser_fuzz_replace(value)
        self._headers[key] = value

    @property
    def get_payload(self):
        return self._payload

    def set_payload(self, data: str):
        self._payload = self.parser_fuzz_replace(data)

    @property
    def get_url(self):
        return self._url
    
    def set_url(self, url):
        self._url = url

    @property
    def get_response(self):
        return self._response 

    def set_response(self, r: requests.Response):
        self._response = r
