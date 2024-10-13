import datetime
import os
import random
import zipfile
from io import BytesIO

import numpy as np
import pandas as pd
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.core.files.base import ContentFile
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django_ratelimit.decorators import ratelimit
from encrypted_files.base import EncryptedFile

from .containers import *
from .models import *
from .utils import *


@ratelimit(key="ip", rate="5/s")
def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        otp = request.POST["otp"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if Profile.objects.get(user=user).otp == otp:
                login(request, user)
                return redirect("home")
            else:
                return render(
                    request,
                    "views/login.html",
                    {"message": "Tassyklama belgisi nädogry"},
                )
        else:
            return render(
                request,
                "views/login.html",
                {"message": "Ulanyjy adyňyz ýa-da/we açar sözüňiz nädogry"},
            )
    else:
        if request.user.is_authenticated:
            return redirect("home")
        else:
            return render(
                request,
                "views/login.html",
            )


@ratelimit(key="ip", rate="5/s")
@login_required(login_url="/login/")
def logout_view(request):
    logout(request)
    return redirect("home")


@ratelimit(key="ip", rate="5/s")
@login_required(login_url="/login/")
def main(request: HttpRequest):
    if request.user.groups.contains(Group.objects.get(name="Moderator")):
        moderators_count = User.objects.filter(groups__name="Moderator").count()
        juries_count = User.objects.filter(groups__name="Jury").count()
        spectators_count = User.objects.filter(groups__name="Spectator").count()
        projects_count = Project.objects.all().count()
        rated_projects_count = Project.rated_objects.all().count()
        unrated_projects_count = Project.unrated_objects.all().count()
        schedules = [
            ScheduleContainer(schedule)
            for schedule in Schedule.objects.filter(
                date__gte=datetime.date.today()
            ).order_by("-date")[:5]
        ]
        return render(
            request,
            "views/main/moderator.html",
            {
                "moderators_count": moderators_count,
                "juries_count": juries_count,
                "spectators_count": spectators_count,
                "projects_count": projects_count,
                "rated_projects_count": rated_projects_count,
                "unrated_projects_count": unrated_projects_count,
                "schedules": schedules,
            },
        )
    elif request.user.groups.contains(Group.objects.get(name="Jury")):
        today = datetime.datetime.today()
        context = {"projects_count": 0, "juries_count": 0}
        try:
            schedule = Schedule.objects.get(
                date__year=today.year, date__month=today.month, date__day=today.day
            )
            projects = []
            for pk in json.loads(schedule.quene_json):
                projects.append(Project.objects.get(pk=pk))
            context["projects_count"] = len(json.loads(schedule.quene_json))
            context["juries_count"] = schedule.juries.all().count()
            context["projects"] = projects
            context["juries"] = schedule.juries.all()
        except:
            pass
        return render(
            request,
            "views/main/jury.html",
            context,
        )
    elif request.user.groups.contains(Group.objects.get(name="Spectator")):
        rated_projects_count = Project.rated_objects.all().count()
        rated_projects = [
            ProjectMarkContainer(project) for project in Project.rated_objects.all()
        ]
        unrated_projects_count = Project.unrated_objects.all().count()
        directions = [
            DirectionContainer(direction) for direction in Direction.objects.all()
        ]
        return render(
            request,
            "views/main/spectator.html",
            {
                "rated_projects_count": rated_projects_count,
                "rated_projects": rated_projects,
                "unrated_projects_count": unrated_projects_count,
                "directions": directions,
                "spectate_btn": True,
                "exporter": True,
            },
        )
    return render(request, "views/main/default.html")


@ratelimit(key="ip", rate="5/s")
@login_required(login_url="/login/")
def schedules(request: HttpRequest):
    if request.user.groups.contains(Group.objects.get(name="Moderator")):
        today = datetime.date.today()
        schedules = [
            ScheduleContainer(schedule)
            for schedule in Schedule.objects.filter(date__gte=today).order_by("-date")
        ]
        return render(
            request,
            "views/schedules.html",
            {
                "schedules": schedules,
            },
        )
    return redirect("home")


@ratelimit(key="ip", rate="5/s")
@login_required(login_url="/login/")
def add_project(request: HttpRequest):
    if request.user.groups.contains(Group.objects.get(name="Moderator")):
        directions = Direction.objects.all()
        if request.method == "POST":
            if request.POST["personality_type"] == "1":
                personality_type = Project.PersonalityType.INDIVIDUAL
            elif request.POST["personality_type"] == "2":
                personality_type = Project.PersonalityType.LEGAL
            else:
                return render(
                    request,
                    "views/add_project.html",
                    {
                        "directions": directions,
                        "message": "Şahsyýet görnüşini dogry giriziň!",
                    },
                )
            try:
                direction = Direction.objects.get(pk=int(request.POST["direction"]))
            except:
                return render(
                    request,
                    "views/add_project.html",
                    {
                        "directions": directions,
                        "message": "Ugry dogry giriziň!",
                    },
                )
            try:
                project = Project.objects.create(
                    personality_type=personality_type,
                    agency=request.POST["agency"],
                    direction=direction,
                    place_of_residence=request.POST["place_of_residence"],
                    full_name_of_manager=request.POST["manager_full_name"],
                    phone_number=request.POST["phone_number"],
                    additional_phone_number=request.POST["additional_phone_number"],
                    email=request.POST["email"],
                    description=request.POST["description"],
                    p_copy_page1=request.FILES["page1"],
                    p_copy_page2_3=request.FILES["page2_3"],
                    p_copy_page5_6=request.FILES["page5_6"],
                    p_copy_page32=request.FILES["page32"],
                )
                if request.POST.get("second_member_full_name", False):
                    if request.POST["second_member_full_name"] != "ýok":
                        project.full_name_of_second_participant = request.POST[
                            "second_member_full_name"
                        ]
                if request.POST.get("third_member_full_name", False):
                    if request.POST["third_member_full_name"] != "ýok":
                        project.full_name_of_third_participant = request.POST[
                            "third_member_full_name"
                        ]
                project.save()
            except:
                return render(
                    request,
                    "views/add_project.html",
                    {"message": "Ýalňyşlyk döredi!", "directions": directions},
                )

            print(request.POST)
            print(request.FILES)
        return render(request, "views/add_project.html", {"directions": directions})
    return redirect("home")


@ratelimit(key="ip", rate="5/s")
@login_required(login_url="/login/")
def add_project_using_xlsx(request: HttpRequest):
    if request.user.groups.contains(Group.objects.get(name="Moderator")):
        if request.method == "POST":
            zip_file_memory = request.FILES.get("zipfile", None)
            if zip_file_memory is not None:
                zip_file = BytesIO(zip_file_memory.read())
                with zipfile.ZipFile(zip_file, "r") as file:
                    images = file.namelist()
                print(images)
            else:
                return render(
                    request,
                    "views/add_project_using_xlsx.html",
                    {"message": "ZIP arhiw tapylmady"},
                )

            dataframe = pd.read_excel(request.FILES.get("xlsx"))
            for index in range(len(dataframe["Ýolbaşçynyň F.A.A"])):
                if f'page1/{dataframe["Pasportyň 1-nji sahypasy"][index]}' in images:
                    filename = f'page1/{dataframe["Pasportyň 1-nji sahypasy"][index]}'
                    try:
                        os.mkdir(f"temp/page1/")
                    except:
                        pass
                    with zipfile.ZipFile(zip_file, "r") as file:
                        file.extract(filename, "temp")
                    with open(f"temp/{filename}", "rb") as file:
                        image1 = ContentFile(file.read(), filename.split("/")[1])
                    os.remove(f"temp/{filename}")
                    os.rmdir(f"temp/{filename.split('/')[0]}/")

                if (
                    f'page2_3/{dataframe["Pasportyň 2-3-nji sahypalary"][index]}'
                    in images
                ):
                    filename = (
                        f'page2_3/{dataframe["Pasportyň 2-3-nji sahypalary"][index]}'
                    )
                    try:
                        os.mkdir(f"temp/page2_3/")
                    except:
                        pass
                    with zipfile.ZipFile(zip_file, "r") as file:
                        file.extract(filename, "temp")
                    with open(f"temp/{filename}", "rb") as file:
                        image2_3 = ContentFile(file.read(), filename.split("/")[1])
                    os.remove(f"temp/{filename}")
                    os.rmdir(f"temp/{filename.split('/')[0]}/")

                if (
                    f'page5_6/{dataframe["Pasportyň 5-6-njy sahypalary"][index]}'
                    in images
                ):
                    filename = (
                        f'page5_6/{dataframe["Pasportyň 5-6-njy sahypalary"][index]}'
                    )
                    try:
                        os.mkdir(f"temp/page5_6/")
                    except:
                        pass
                    with zipfile.ZipFile(zip_file, "r") as file:
                        file.extract(filename, "temp")
                    with open(f"temp/{filename}", "rb") as file:
                        image5_6 = ContentFile(file.read(), filename.split("/")[1])
                    os.remove(f"temp/{filename}")
                    os.rmdir(f"temp/{filename.split('/')[0]}/")

                if f'page32/{dataframe["Pasportyň 32-nji sahypasy"][index]}' in images:
                    filename = f'page32/{dataframe["Pasportyň 32-nji sahypasy"][index]}'
                    try:
                        os.mkdir(f"temp/page32/")
                    except:
                        pass
                    with zipfile.ZipFile(zip_file, "r") as file:
                        file.extract(filename, "temp")
                    with open(f"temp/{filename}", "rb") as file:
                        image32 = ContentFile(file.read(), filename.split("/")[1])
                    os.remove(f"temp/{filename}")
                    os.rmdir(f"temp/{filename.split('/')[0]}/")

                if dataframe["Şahs"][index].lower() == "fiziki":
                    personality_type = Project.PersonalityType.INDIVIDUAL
                elif dataframe["Şahs"][index].lower() == "ýuridiki":
                    personality_type = Project.PersonalityType.LEGAL
                try:
                    direction = Direction.objects.get(name=dataframe["Ugry"][index])
                except:
                    direction = Direction.objects.create(name=dataframe["Ugry"][index])

                project = Project.objects.create(
                    personality_type=personality_type,
                    agency=dataframe["Edaranyň ady"][index],
                    direction=direction,
                    place_of_residence=dataframe["Ýaşaýan ýeri"][index],
                    full_name_of_manager=dataframe["Ýolbaşçynyň F.A.A"][index],
                    phone_number=dataframe["Ýolbaşçynyň telefon belgisi"][index],
                    additional_phone_number=dataframe["Goşmaça telefon belgisi"][index],
                    email=dataframe["Email"][index],
                    description=dataframe["Taslamanyň beýany"][index],
                    p_copy_page1=image1,
                    p_copy_page2_3=image2_3,
                    p_copy_page5_6=image5_6,
                    p_copy_page32=image32,
                )

                if (
                    not type(dataframe["Ikinji agzanyň F.A.A"][index]) == np.float64
                    or not type(dataframe["Üçünji agzanyň F.A.A"][index]) == np.nan
                ):
                    project.full_name_of_second_participant = dataframe[
                        "Ikinji agzanyň F.A.A"
                    ][index]

                if (
                    not type(dataframe["Üçünji agzanyň F.A.A"][index]) == np.float64
                    or not type(dataframe["Üçünji agzanyň F.A.A"][index]) == np.nan
                ):
                    project.full_name_of_third_participant = dataframe[
                        "Üçünji agzanyň F.A.A"
                    ][index]
                project.save()

        return render(request, "views/add_project_using_xlsx.html")
    return redirect("home")


@ratelimit(key="ip", rate="5/s")
@login_required(login_url="/login/")
def add_schedule(request: HttpRequest):
    if request.user.groups.contains(Group.objects.get(name="Moderator")):
        return render(request, "views/add_schedule.html")
    return redirect("home")


@ratelimit(key="ip", rate="5/s")
@login_required(login_url="/login/")
def edit_schedule(request: HttpRequest, schedule_pk: int):
    if request.user.groups.contains(Group.objects.get(name="Moderator")):
        schedule = Schedule.objects.get(pk=schedule_pk)
        juries = schedule.juries.all()
        project_pks = json.loads(schedule.quene_json)
        projects = []
        for project_pk in project_pks:
            projects.append(Project.objects.get(pk=project_pk))
        return render(
            request,
            "views/edit_schedule.html",
            {"schedule": schedule, "projects": projects, "juries": juries},
        )
    return redirect("home")


@ratelimit(key="ip", rate="5/s")
@login_required(login_url="/login/")
def delete_schedule(request: HttpRequest, schedule_pk: int):
    if request.user.groups.contains(Group.objects.get(name="Moderator")):
        Schedule.objects.get(pk=schedule_pk).delete()
        return redirect("schedules")
    return redirect("home")


@ratelimit(key="ip", rate="5/s")
@login_required(login_url="/login/")
def mark_form(request: HttpRequest):
    context = {"criteries": Criteria.objects.all()}
    if request.user.groups.contains(Group.objects.get(name="Jury")):
        if request.method == "POST":
            rated_project = Project.objects.get(pk=int(request.POST["project-pk"]))
            if Mark.objects.filter(jury=request.user, project=rated_project).exists():
                return redirect("mark_form")
            for criteria in context["criteries"]:
                mark = Mark.objects.create(
                    jury=request.user,
                    mark=int(request.POST[f"mark-{criteria.pk}"]),
                    project=rated_project,
                    criteria=criteria,
                )
                if request.POST[f"description-{criteria.pk}"] != "":
                    mark.description = request.POST[f"description-{criteria.pk}"]
                mark.save()

                today = datetime.datetime.today()
                schedule = Schedule.objects.get(
                    date__year=today.year, date__month=today.month, date__day=today.day
                )

                juries = schedule.juries.all()
                rate_count = 0
                for jury in juries:
                    print(jury.first_name + "init")
                    mark_count = 0
                    for criteria in context["criteries"]:
                        if Mark.objects.filter(
                            jury=jury, criteria=criteria, project=rated_project
                        ).exists():
                            print(f"{ jury.first_name } +1")
                            mark_count += 1
                    if mark_count == context["criteries"].count():
                        rate_count += 1
                if rate_count == juries.count():
                    print(rate_count)
                    rated_project.rated = True
                    rated_project.save()
        today = datetime.datetime.today()
        try:
            schedule = Schedule.objects.get(
                date__year=today.year, date__month=today.month, date__day=today.day
            )
        except:
            return redirect("home")
        if not schedule.juries.filter(pk=request.user.pk):
            return redirect("home")

        for project_pk in json.loads(schedule.quene_json):
            project = Project.objects.get(pk=project_pk)
            if (
                not Mark.objects.filter(
                    project=project,
                    jury=request.user,
                ).exists()
                and not project.rated
            ):
                context["project"] = project
                break
        else:
            return redirect("home")
        return render(request, "views/mark_form.html", context)
    return redirect("home")


@ratelimit(key="ip", rate="5/s")
@login_required(login_url="/login/")
def export_to_pdf(request: HttpRequest):
    if request.user.groups.contains(Group.objects.get(name="Spectator")):
        sort_by_marks = lambda e: e.percent
        rated_projects = [
            ProjectMarkContainer(project) for project in Project.rated_objects.all()
        ]
        rated_projects.sort(key=sort_by_marks)
        rated_projects.reverse()
        data = {
            "rated_projects": rated_projects,
            "current_year": datetime.datetime.now().year,
        }
        pdf = render_to_pdf("results_pdf.html", data)
        return HttpResponse(pdf, content_type="application/pdf")
    return redirect("home")


@ratelimit(key="ip", rate="5/s")
@login_required(login_url="/login/")
def export_to_xlsx(request: HttpRequest):
    if request.user.groups.contains(Group.objects.get(name="Spectator")):
        rated_projects = [
            ProjectMarkContainer(project) for project in Project.rated_objects.all()
        ]
        dataframe_dict = {"Taslama": [], "Bal": []}

        for project in rated_projects:
            dataframe_dict["Taslama"].append(project.name)
            dataframe_dict["Bal"].append(f"{project.percent}%")

        dataframe = pd.DataFrame(dataframe_dict)
        response = HttpResponse(
            content_type="application/xlsx",
        )
        response["Content-Disposition"] = f'attachment; filename="results.xlsx"'
        with pd.ExcelWriter(response) as writer:
            dataframe.to_excel(writer, sheet_name="sheet1")
        return response
    return redirect("home")


@ratelimit(key="ip", rate="5/s")
@login_required(login_url="/login/")
def projects_list(request: HttpRequest):
    if request.user.groups.contains(Group.objects.get(name="Spectator")):
        rated_projects = Project.rated_objects.all()
        return render(request, "views/projects_list.html", {"projects": rated_projects})
    return redirect("home")


@ratelimit(key="ip", rate="5/s")
@login_required(login_url="/login/")
def project_result(request: HttpRequest, project_pk: int):
    if request.user.groups.contains(Group.objects.get(name="Spectator")):
        project = Project.objects.get(pk=project_pk)
        marks = [
            MarkContainer(mark)
            for mark in Mark.objects.filter(project=project).order_by("-date")
        ]
        project_mark_container = ProjectMarkContainer(project)
        return render(
            request,
            "views/project_result.html",
            {
                "project": project,
                "marks": marks,
                "project_mark_container": project_mark_container,
            },
        )


@ratelimit(key="ip", rate="5/s")
@login_required(login_url="/login/")
def add_user(request: HttpRequest):
    if request.user.groups.contains(Group.objects.get(name="Moderator")):
        groups = Group.objects.all()
        if request.method == "POST":
            if request.POST["password_1"] == request.POST["password_2"]:
                try:
                    group = Group.objects.get(pk=int(request.POST["role"]))
                    user = User.objects.create(
                        last_name=request.POST["last_name"],
                        first_name=request.POST["first_name"],
                        username=request.POST["username"],
                    )
                    user.set_password(request.POST["password_1"])
                    Profile.objects.create(
                        user=user, password=request.POST["password_1"]
                    )
                    user.groups.add(group)
                    user.save()
                    return redirect("users")
                except:
                    return render(
                        request,
                        "views/add_user.html",
                        {
                            "groups": groups,
                            "message": "Näsazlyk ýüze çykdy",
                        },
                    )
            else:
                return render(
                    request,
                    "views/add_user.html",
                    {
                        "groups": groups,
                        "message": "Girizen açar sözleriňiz bir-birine deň däl",
                    },
                )
        return render(request, "views/add_user.html", {"groups": groups})
    return redirect("home")


@ratelimit(key="ip", rate="5/s")
@login_required(login_url="/login/")
def users(request: HttpRequest):
    if request.user.groups.contains(Group.objects.get(name="Moderator")):
        juries = User.objects.filter(groups__name="Jury")
        spectators = User.objects.filter(groups__name="Spectator")
        moderators = User.objects.filter(groups__name="Moderator")
        return render(
            request,
            "views/users.html",
            {
                "juries": juries,
                "spectators": spectators,
                "moderators": moderators,
            },
        )
    return redirect("home")


@ratelimit(key="ip", rate="5/s")
@login_required(login_url="/login/")
def delete_user(request: HttpRequest, user_pk: int):
    if request.user.groups.contains(Group.objects.get(name="Moderator")):
        User.objects.get(pk=user_pk).delete()
        return redirect("users")
    return redirect("home")


@ratelimit(key="ip", rate="5/s")
@login_required(login_url="/login/")
def decrypted_copy_1(request: HttpRequest, project_pk: int):
    if (
        request.user.groups.contains(Group.objects.get(name="Moderator"))
        or request.user.is_superuser
    ):
        file = Project.objects.get(pk=project_pk).p_copy_page1
        encrypted_file = EncryptedFile(file)
        return HttpResponse(
            encrypted_file.read(),
            content_type="image/jpg, image/png",
        )
    return redirect("home")


@ratelimit(key="ip", rate="5/s")
@login_required(login_url="/login/")
def decrypted_copy_2_3(request: HttpRequest, project_pk: int):
    if (
        request.user.groups.contains(Group.objects.get(name="Moderator"))
        or request.user.is_superuser
    ):
        file = Project.objects.get(pk=project_pk).p_copy_page2_3
        encrypted_file = EncryptedFile(file)
        return HttpResponse(
            encrypted_file.read(),
            content_type="image/jpg, image/png",
        )
    return redirect("home")


@ratelimit(key="ip", rate="5/s")
@login_required(login_url="/login/")
def decrypted_copy_5_6(request: HttpRequest, project_pk: int):
    if (
        request.user.groups.contains(Group.objects.get(name="Moderator"))
        or request.user.is_superuser
    ):
        file = Project.objects.get(pk=project_pk).p_copy_page5_6
        encrypted_file = EncryptedFile(file)
        return HttpResponse(
            encrypted_file.read(),
            content_type="image/jpg, image/png",
        )
    return redirect("home")


@ratelimit(key="ip", rate="5/s")
@login_required(login_url="/login/")
def decrypted_copy_32(request: HttpRequest, project_pk: int):
    if (
        request.user.groups.contains(Group.objects.get(name="Moderator"))
        or request.user.is_superuser
    ):
        file = Project.objects.get(pk=project_pk).p_copy_page32
        encrypted_file = EncryptedFile(file)
        return HttpResponse(
            encrypted_file.read(),
            content_type="image/jpg, image/png",
        )
    return redirect("home")
