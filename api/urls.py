from django.urls import path

from .views import *

urlpatterns = [
    path(
        "unrated_projects/", unrated_projects_api_view, name="unrated_projects_api_view"
    ),
    path("juries/", juries_api_view, name="juries_api_view"),
    path(
        "add_schedule/",
        add_schedule_api_view,
        name="add_schedule_api_view",
    ),
]
