from django.urls import path

from .views import *

urlpatterns = [
    path("", main, name="home"),
    path("schedules/", schedules, name="schedules"),
    path("users/", users, name="users"),
    path("projects_list/", projects_list, name="projects_list"),
    path("project_result/<int:project_pk>/", project_result),
    path("mark_form/", mark_form, name="mark_form"),
    path("schedules/edit/<int:schedule_pk>/", edit_schedule),
    path("schedules/delete/<int:schedule_pk>/", delete_schedule),
    path("users/delete/<int:user_pk>/", delete_user),
    path("export_to_pdf/", export_to_pdf, name="export_to_pdf"),
    path("export_to_xlsx/", export_to_xlsx, name="export_to_xlsx"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("add_project/", add_project, name="add_project"),
    path("add_user/", add_user, name="add_user"),
    path("add_schedule/", add_schedule, name="add_schedule"),
    path(
        "add_project_using_excel/",
        add_project_using_xlsx,
        name="add_project_using_excel",
    ),
]
