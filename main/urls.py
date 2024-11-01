from django.urls import path

from .views import *

urlpatterns = [
    path("", main, name="home"),
    path("schedules/", schedules, name="schedules"),
    path("users/", users, name="users"),
    path("projects_list/", projects_list, name="projects_list"),
    path("projects_list/by_direction/<str:direction>/", projects_list),
    path("projects_list/export_to_docx/", export_to_docx, name="export_to_docx"),
    path("projects_list/export_to_xlsx/", export_to_xlsx, name="export_to_xlsx"),
    path(
        "projects_list/export_jury_marks_to_xlsx/",
        export_jury_marks_to_xlsx,
        name="export_jury_marks_to_xlsx",
    ),
    path(
        "projects_list/by_direction/<str:direction>/export_jury_marks_to_xlsx/",
        export_jury_marks_to_xlsx,
        name="export_jury_marks_to_xlsx",
    ),
    path("projects_list/by_direction/<str:direction>/export_to_docx/", export_to_docx),
    path("projects_list/by_direction/<str:direction>/export_to_xlsx/", export_to_xlsx),
    path("project_result/<int:project_pk>/", project_result),
    path("project_result/<int:project_pk>/export_to_xlsx/", project_result_to_xlsx),
    path("mark_form/", mark_form, name="mark_form"),
    path("schedules/edit/<int:schedule_pk>/", edit_schedule),
    path("mark/edit/<int:mark_pk>/", edit_mark),
    path("schedules/delete/<int:schedule_pk>/", delete_schedule),
    # path("users/delete/<int:user_pk>/", delete_user),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout_view"),
    path("add_project/", add_project, name="add_project"),
    # path("add_user/", add_user, name="add_user"),
    path("add_schedule/", add_schedule, name="add_schedule"),
    path(
        "add_project_using_excel/",
        add_project_using_xlsx,
        name="add_project_using_excel",
    ),
]
