from django.urls import path

from .views import *

urlpatterns = [
    path(
        "unrated_projects/", unrated_projects_api_view, name="unrated_projects_api_view"
    ),
]
