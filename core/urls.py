from django.urls import path

app_name = "core"

from core.views import metods, auth_check, test_metod

urlpatterns = [
    path("", metods, name="metods_list"),
    path("metods/auth_check/", auth_check, name="auth_check"),
    path("metods/test_metod/", test_metod, name="test_metod"),
]
