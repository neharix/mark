from django.urls import path

from .views import *

urlpatterns = [
    path("", main, name="home"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("add_project/", add_project, name="add_project"),
    path("add_schedule/", add_schedule, name="add_schedule"),
    path(
        "add_project_using_excel/",
        add_project_using_xlsx,
        name="add_project_using_excel",
    ),
]
