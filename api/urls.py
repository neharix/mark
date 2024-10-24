from django.urls import path

from .views import *

urlpatterns = [
    path(
        "update_project/<int:project_pk>/<int:arr_id>/",
        update_chart_data_api_view,
    ),
    path(
        "unrated_projects/", unrated_projects_api_view, name="unrated_projects_api_view"
    ),
    path(
        "unrated_status/",
        unrated_projects_status_api_view,
        name="unrated_projects_status_api_view",
    ),
    # path("otp/", otp_api_view, name="otp_api_view"),
    path("juries/", juries_api_view, name="juries_api_view"),
    path(
        "delete_project_from_schedule/",
        delete_project_from_schedule_api_view,
        name="delete_project_from_schedule",
    ),
    path(
        "delete_jury_from_schedule/",
        delete_jury_from_schedule_api_view,
        name="delete_jury_from_schedule",
    ),
    path(
        "add_schedule/",
        add_schedule_api_view,
        name="add_schedule_api_view",
    ),
    path(
        "edit_schedule/",
        edit_schedule_api_view,
        name="edit_schedule_api_view",
    ),
]
