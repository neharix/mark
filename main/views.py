import datetime
import os
import random
import zipfile
from io import BytesIO

import numpy as np
import pandas as pd
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.core.files.base import ContentFile
from django.http import HttpRequest
from django.shortcuts import redirect, render

from .containers import *
from .models import *


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")

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


def register_view(request):
    if request.method == "POST":
        fname = request.POST["firstname"]
        lname = request.POST["lastname"]
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensuring password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(
                request, "flight/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.first_name = fname
            user.last_name = lname
            user.save()
        except:
            return render(
                request, "flight/register.html", {"message": "Username already taken."}
            )
        login(request, user)
        return redirect("home")
    else:
        return render(request, "flight/register.html")


@login_required(login_url="/login/")
def logout_view(request):
    logout(request)
    return redirect("home")


@login_required(login_url="/login/")
def main(request: HttpRequest):
    if request.user.groups.contains(Group.objects.get(name="Moderator")):
        projects_count = Project.objects.all().count()
        rated_projects_count = Project.rated_objects.all().count()
        unrated_projects_count = Project.unrated_objects.all().count()
        schedules = [
            ScheduleContainer(schedule)
            for schedule in Schedule.objects.all().order_by("-date")[:5]
        ]
        return render(
            request,
            "views/main/moderator.html",
            {
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


@login_required(login_url="/login/")
def schedules(request: HttpRequest):
    if request.user.groups.contains(Group.objects.get(name="Moderator")):
        schedules = [
            ScheduleContainer(schedule)
            for schedule in Schedule.objects.all().order_by("-date")
        ]
        return render(
            request,
            "views/schedules.html",
            {
                "schedules": schedules,
            },
        )
    return redirect("home")


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

                if not type(dataframe["Ikinji agzanyň F.A.A"][index]) == np.float64:
                    project.full_name_of_second_participant = dataframe[
                        "Ikinji agzanyň F.A.A"
                    ][index]

                if not type(dataframe["Üçünji agzanyň F.A.A"][index]) == np.float64:
                    project.full_name_of_third_participant = dataframe[
                        "Üçünji agzanyň F.A.A"
                    ][index]
                project.save()

        return render(request, "views/add_project_using_xlsx.html")
    return redirect("home")


def add_schedule(request: HttpRequest):
    if request.user.groups.contains(Group.objects.get(name="Moderator")):
        return render(request, "views/add_schedule.html")
    return redirect("home")


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


def delete_schedule(request: HttpRequest, schedule_pk: int):
    if request.user.groups.contains(Group.objects.get(name="Moderator")):
        Schedule.objects.get(pk=schedule_pk).delete()
        return redirect("schedules")
    return redirect("home")


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
