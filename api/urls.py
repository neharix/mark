from django.urls import include, path, re_path

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
    path("project-search/", search_project_api_view, name="search_project"),
    path("project-search-all/", search_all_project_api_view, name="search_all_project"),
    path("mark-client/", mark_client_api_view, name="mark_client_api_view"),
    path("is-admin/", check_status, name="is_admin"),
    path("jury-search/", search_juries_api_view, name="search_jury"),
    path("session-auth/", include("rest_framework.urls")),
    path("auth/", include("djoser.urls")),
    re_path(r"^auth/", include("djoser.urls.authtoken")),
]
