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
    path("export_to_docx/", export_to_docx, name="export_to_docx"),
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
    path("decrypt_p1/<int:project_pk>/", decrypted_copy_1),
    path("decrypt_p2_3/<int:project_pk>/", decrypted_copy_2_3),
    path("decrypt_p5_6/<int:project_pk>/", decrypted_copy_5_6),
    path("decrypt_p32/<int:project_pk>/", decrypted_copy_32),
]
