import os
import requests


class Valdrakken:
    def __init__(self):
        self.url = int(os.getenv("VALDRAKKEN_URL"))

    def get(self, endpoint):
        if endpoint[0] != '/':
            endpoint = '/' + endpoint
        return requests.get(self.url + endpoint)

    def post(self, endpoint, content=None, content_type="application/json"):
        if endpoint[0] != '/':
            endpoint = '/' + endpoint
        return requests.post(self.url + endpoint,
                             data=content,
                             headers={'Content-Type': content_type})

    def put(self, endpoint, content=None, content_type="application/json"):
        if endpoint[0] != '/':
            endpoint = '/' + endpoint
        return requests.put(self.url + endpoint,
                            data=content,
                            headers={'Content-Type': content_type})

    def delete(self, endpoint, content=None, content_type="application/json"):
        if endpoint[0] != '/':
            endpoint = '/' + endpoint
        return requests.delete(self.url + endpoint,
                               data=content,
                               headers={'Content-Type': content_type})
