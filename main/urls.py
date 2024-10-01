from django.urls import path

from .views import *

urlpatterns = [
    path("", main, name="home"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("", logout_view, name="register"),
]
