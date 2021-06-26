from django.shortcuts import render
from translator.service import ClientRpc, ClientRpcError, ClientRpcHttpError

# Create your views here.
def metods(request):
    return render(request, "metods.html")


def auth_check(request):
    try:
        rpc_client = ClientRpc()
        res = rpc_client.get(method="auth.check")
        rpc_client.close()
    except ClientRpcError as e:
        context = {"error": {"code": e.code, "message": e.message, "data": e.data}}
    except ClientRpcHttpError as e:
        context = {"error": {"status": e.status, "reason": e.reason}}
    else:
        context = {"data": res}
    return render(request, "metods.html", context)


def test_metod(request):
    pass
