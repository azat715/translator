from django.shortcuts import render
from core.forms import TestForm
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
    return render(request, "result.html", context)


def test_metod(request):
    if request.method == "POST":
        form = TestForm(request.POST)
        if form.is_valid():
            param1 = form.cleaned_data["text_param"]
            param2 = form.cleaned_data["numeric_param"]
            try:
                rpc_client = ClientRpc()
                res = rpc_client.get(
                    method="test.error",
                    params={
                        "param1": param1,
                        "param2": param2,
                    },
                )
                rpc_client.close()
            except ClientRpcError as e:
                context = {
                    "error": {"code": e.code, "message": e.message, "data": e.data}
                }
            except ClientRpcHttpError as e:
                context = {"error": {"status": e.status, "reason": e.reason}}
            else:
                context = {"data": res}
            print(context)
            return render(request, "result.html", context)
    else:
        form = TestForm()
    return render(request, "form.html", {"form": form})
