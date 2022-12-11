import os
import requests


class Valdrakken:
    url = os.getenv("VALDRAKKEN_URL")

    @classmethod
    def get(cls, endpoint, content=None, content_type="application/json"):
        if endpoint[0] != '/':
            endpoint = '/' + endpoint
        return requests.get(cls.url + endpoint,
                             data=content,
                             headers={'Content-Type': content_type})

    @classmethod
    def post(cls, endpoint, content=None, content_type="application/json"):
        if endpoint[0] != '/':
            endpoint = '/' + endpoint
        return requests.post(cls.url + endpoint,
                             data=content,
                             headers={'Content-Type': content_type})

    @classmethod
    def put(cls, endpoint, content=None, content_type="application/json"):
        if endpoint[0] != '/':
            endpoint = '/' + endpoint
        return requests.put(cls.url + endpoint,
                            data=content,
                            headers={'Content-Type': content_type})

    @classmethod
    def delete(cls, endpoint, content=None, content_type="application/json"):
        if endpoint[0] != '/':
            endpoint = '/' + endpoint
        return requests.delete(cls.url + endpoint,
                               data=content,
                               headers={'Content-Type': content_type})
