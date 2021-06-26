import pytest
from translator.service import ClientRpc, ClientRpcError, ClientRpcHttpError
from django.conf import settings


def test_auth_check():
    rpc_client = ClientRpc()
    res = rpc_client.get(method="auth.check")
    rpc_client.close()
    print(res)
    assert res["result"]["_data"]["user"]["id"] == 7


def test_metod_error():
    rpc_client = ClientRpc()
    with pytest.raises(ClientRpcError) as exc:
        rpc_client.get(method="err")
    print(str(exc.value))
    assert exc.value.code == -32601
    assert exc.value.message == "Method not found"


def test_invalid_url():
    settings.RPC_URL = "https://slb.medv.ru/api/v2"
    with pytest.raises(ClientRpcHttpError) as exc:
        rpc_client = ClientRpc()
        rpc_client.get(method="auth.check")
    print(str(exc.value))


def test_config_err():
    settings.SSL_RPC = {}
    with pytest.raises(Exception) as exc:
        ClientRpc()
    print(exc.value.args)
