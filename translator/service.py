from typing import Optional
import http.client
from urllib.parse import urlparse
import json
import ssl

from django.conf import settings

URL = "slb.medv.ru"


class ClientRpcError(Exception):
    def __init__(self, code, message, data):
        super().__init__()
        self.code = code
        self.message = message
        self.data = data

    def __str__(self):
        return f'ClientRpcError: code = {self.code}, message = "{self.message}", data = "{self.data}"'


class ClientRpcHttpError(Exception):
    def __init__(self, status, reason):
        super().__init__()
        self.status = status
        self.reason = reason

    def __str__(self):
        return f'ClientRpcHttpError: http status = {self.status}, http reason = "{self.reason}"'


class ClientRpc:
    def __init__(self):
        try:
            self.url = urlparse(settings.RPC_URL)
        except KeyError as err:
            print("KeyError: {0}".format(err))
            raise Exception("Проверьте настроки Django settings.py")
        self.certfile = settings.SSL_RPC["certfile"]
        if not self.certfile.exists():
            raise Exception(
                "Проверьте настроки Django settings.py: Отсутствует файл certfile"
            )
        self.keyfile = settings.SSL_RPC["keyfile"]
        if not self.keyfile.exists():
            raise Exception(
                "Проверьте настроки Django settings.py: Отсутствует файл keyfile"
            )
        self.hostname = self.url.hostname
        self.path = self.url.path
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.load_cert_chain(certfile=self.certfile, keyfile=self.keyfile)
        self.conn = http.client.HTTPSConnection(self.hostname, context=context)
        self.headers = {"Content-type": "application/json"}
        self.request = {
            "jsonrpc": "2.0",
        }

    def get(self, method: str, params: Optional[dict] = None, _id: int = 1) -> dict:
        self.request["method"] = method
        self.request["id"] = _id
        if params:
            self.request["params"] = params
        body = json.dumps(self.request)
        self.conn.request("POST", self.path, body, self.headers)
        response = self.conn.getresponse()
        if response.status != 200:
            self.close()
            raise ClientRpcHttpError(response.status, response.reason)
        res = json.loads(response.read())
        if res.get("error"):
            err = res["error"]
            self.close()
            raise ClientRpcError(err["code"], err["message"], err.get("data"))
        return res

    def close(self):
        return self.conn.close()
