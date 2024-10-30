import datetime
import json
import random

# Create your views here.
import pytz
from django.contrib.auth.models import Group
from django.core.mail import send_mail
from django.shortcuts import render
from django_ratelimit.decorators import ratelimit
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.request import HttpRequest
from rest_framework.response import Response

from main.models import *
from main.utils import *

from .containers import *
from .serializers import *

# def pdf_data_api_view(request: HttpRequest):
#     if request.user.groups.contains(Group.objects.get(name="Moderator")):
#         sort_by_marks = lambda e: e.percent
#         rated_projects = [
#             ProjectMarkContainer(project) for project in Project.rated_objects.all()
#         ]
#         rated_projects.sort(key=sort_by_marks)
#         rated_projects.reverse()
#         data = {
#             "rated_projects": rated_projects,
#             "current_year": datetime.datetime.now().year,
#         }
#     return Response({"detail": "you need to be a spectator"})


@permission_classes([IsAuthenticated])
@api_view(["GET"])
def update_chart_data_api_view(request: HttpRequest, project_pk: int, arr_id: int):
    if request.user.groups.contains(Group.objects.get(name="Spectator")):
        project = Project.objects.get(pk=project_pk)
        project_container = UnratedProjectMarkContainer(project)
        serializer = UnratedProjectSerializer(project_container)
        data = serializer.data
        data["arr_id"] = arr_id
        return Response(data)
    return Response({"detail": "you need to be a spectator"})


@ratelimit(key="ip", rate="5/s")
@permission_classes([IsAuthenticated])
@api_view(["GET"])
def unrated_projects_status_api_view(request: HttpRequest):
    if request.user.groups.contains(Group.objects.get(name="Spectator")):
        today = datetime.datetime.today()
        # .astimezone(pytz.timezone("Asia/Ashgabat"))
        projects = []
        for project in Project.objects.all():
            project_container = UnratedProjectMarkContainer(project)
            if (
                Mark.objects.filter(project=project).exists()
                and project_container.date != None
            ):
                projects.append(project_container)

        serializer = UnratedProjectSerializer(projects, many=True)
        return Response(serializer.data)
    return Response({"detail": "you need to be a spectator"})


@ratelimit(key="ip", rate="5/s")
@permission_classes([IsAuthenticated])
@api_view(["GET"])
def unrated_projects_api_view(request: HttpRequest):
    projects = Project.unrated_objects.all()
    quenes = Schedule.objects.all()
    scheduled_project_pks = []
    projects_list = []
    for quene in quenes:
        scheduled_project_pks += json.loads(quene.quene_json)
    for project in projects:
        if project.pk not in scheduled_project_pks:
            projects_list.append(project)
    serializer = ProjectSerializer(projects_list, many=True)
    return Response(serializer.data)


@ratelimit(key="ip", rate="5/s")
@permission_classes([IsAuthenticated])
@api_view(["GET"])
def juries_api_view(request: HttpRequest):
    users = User.objects.all()
    juries = []
    for user in users:
        if user.groups.contains(Group.objects.get(name="Jury")):
            juries.append(user)
    serializer = UserSerializer(juries, many=True)
    return Response(serializer.data)


@ratelimit(key="ip", rate="5/s")
@permission_classes([IsAuthenticated])
@api_view(["POST"])
def add_schedule_api_view(request: HttpRequest):
    if request.user.groups.contains(Group.objects.get(name="Moderator")):
        if (
            request.data.get("date", False)
            and request.data.get("schedule", False)
            and request.data.get("juries", False)
        ):

            if not Schedule.objects.filter(
                date=datetime.datetime.strptime(request.data["date"], "%d/%m/%Y")
            ).exists():
                schedule = Schedule.objects.create(
                    quene_json=request.data["schedule"],
                    date=datetime.datetime.strptime(request.data["date"], "%d/%m/%Y"),
                )
                juries_pk = json.loads(request.data["juries"])
                for i in juries_pk:
                    schedule.juries.add(i)
                schedule.save()
                return Response({"detail": "success"})
            else:
                return Response({"detail": "schedule was made on the given date"})
        return Response({"detail": "fail"})
    return Response({"detail": "you need to be a moderator"})


@ratelimit(key="ip", rate="5/s")
@permission_classes([IsAuthenticated])
@api_view(["POST"])
def edit_schedule_api_view(request: HttpRequest):
    if request.user.groups.contains(Group.objects.get(name="Moderator")):
        if (
            request.data.get("date", False)
            and request.data.get("schedule", False)
            and request.data.get("juries", False)
            and request.data.get("schedule_pk", False)
        ):

            schedule = Schedule.objects.get(pk=request.data["schedule_pk"])
            if (
                not Schedule.objects.filter(
                    date=datetime.datetime.strptime(request.data["date"], "%d/%m/%Y")
                ).exists()
                or schedule.date.strftime("%d/%m/%Y") == request.data["date"]
            ):
                schedule.date = datetime.datetime.strptime(
                    request.data["date"], "%d/%m/%Y"
                )
            else:
                return Response({"detail": "schedule was made on the given date"})

            schedule.juries.clear()
            schedule.quene_json = request.data["schedule"]
            juries_pk = json.loads(request.data["juries"])
            for i in juries_pk:
                schedule.juries.add(i)
            schedule.save()
            return Response({"detail": "success"})

        return Response({"detail": "fail"})
    return Response({"detail": "you need to be a moderator"})


@ratelimit(key="ip", rate="5/s")
@permission_classes([IsAuthenticated])
@api_view(["POST"])
def delete_project_from_schedule_api_view(request: HttpRequest):
    if request.user.groups.contains(Group.objects.get(name="Moderator")):
        if request.data.get("schedule_pk", False) and request.data.get(
            "project_id", False
        ):
            schedule = Schedule.objects.get(id=request.data["schedule_pk"])
            projects = json.loads(schedule.quene_json)
            projects.remove(int(request.data["project_id"]))
            schedule.quene_json = json.dumps(projects)
            schedule.save()
            return Response({"detail": "success"})
        return Response({"detail": "fail"})
    return Response({"detail": "you need to be a moderator"})


@ratelimit(key="ip", rate="5/s")
@permission_classes([IsAuthenticated])
@api_view(["POST"])
def delete_jury_from_schedule_api_view(request: HttpRequest):
    if request.user.groups.contains(Group.objects.get(name="Moderator")):
        if request.data.get("schedule_pk", False) and request.data.get(
            "jury_id", False
        ):
            jury = User.objects.get(id=request.data["jury_id"])
            schedule = Schedule.objects.get(id=request.data["schedule_pk"])
            schedule.juries.remove(jury)
            schedule.save()
            return Response({"detail": "success"})
        return Response({"detail": "fail"})
    return Response({"detail": "you need to be a moderator"})


@ratelimit(key="ip", rate="5/s")
@permission_classes([IsAuthenticated])
@api_view(["POST"])
def search_project_api_view(request: HttpRequest):
    if request.data.get("search", False) and request.data.get("direction", False):
        if request.data["direction"].isdigit():
            projects = (
                Project.unrated_objects.filter(
                    description__contains=request.data["search"],
                    direction=int(request.data["direction"]),
                )
                | Project.unrated_objects.filter(
                    full_name_of_manager__contains=request.data["search"],
                    direction=int(request.data["direction"]),
                )
                | Project.unrated_objects.filter(
                    agency__contains=request.data["search"],
                    direction=int(request.data["direction"]),
                )
            )
        else:
            projects = (
                Project.unrated_objects.filter(
                    description__contains=request.data["search"]
                )
                | Project.unrated_objects.filter(
                    full_name_of_manager__contains=request.data["search"],
                )
                | Project.unrated_objects.filter(
                    agency__contains=request.data["search"],
                )
            )
        quenes = Schedule.objects.all()
        scheduled_project_pks = []
        projects_list = []
        for quene in quenes:
            scheduled_project_pks += json.loads(quene.quene_json)
        for project in projects:
            if project.pk not in scheduled_project_pks:
                projects_list.append(project)
        serializer = ProjectSerializer(projects_list, many=True)
        return Response(serializer.data)
    elif request.data.get("direction", False):
        if request.data["direction"].isdigit():
            projects = Project.unrated_objects.filter(
                direction=int(request.data["direction"]),
            )
        else:
            projects = Project.unrated_objects.all()
        quenes = Schedule.objects.all()
        scheduled_project_pks = []
        projects_list = []
        for quene in quenes:
            scheduled_project_pks += json.loads(quene.quene_json)
        for project in projects:
            if project.pk not in scheduled_project_pks:
                projects_list.append(project)
        serializer = ProjectSerializer(projects_list, many=True)
        return Response(serializer.data)
    return Response({"detail": "invalid data"})


@ratelimit(key="ip", rate="5/s")
@permission_classes([IsAuthenticated])
@api_view(["POST"])
def search_juries_api_view(request: HttpRequest):
    if request.data.get("search", False):
        if request.data["search"] != "":
            users = User.objects.filter(
                last_name__contains=request.data["search"]
            ) | User.objects.filter(first_name__contains=request.data["search"])
        else:
            users = User.objects.all()
        juries = []
        for user in users:
            if user.groups.contains(Group.objects.get(name="Jury")):
                juries.append(user)
        serializer = UserSerializer(juries, many=True)
        return Response(serializer.data)
    return Response({"detail": "invalid data"})


# @ratelimit(key="ip", rate="5/s")
# @api_view(["POST"])
# def otp_api_view(request: HttpRequest):
#     username = request.data["username"]
#     email = request.data["email"]
#     try:
#         user = User.objects.get(username=username)
#         print("success")
#         if user.email == email:
#             profile = Profile.objects.get(user=user)
#             profile.otp = "".join([str(random.randint(0, 9)) for i in range(5)])
#             profile.save()
#             try:
#                 pass
#             except:
#                 return Response({"detail": "something wrong with server"})
#         else:
#             return Response({"detail": "invalid email"})
#     except:
#         return Response({"detail": "user not found"})
#     send_mail(
#         subject="Tassyklama kody",
#         from_email="sanlycozgutbaslesik@gmail.com",
#         message="",
#         recipient_list=[user.email],
#         html_message=f"<div><p>Girişi ýerine ýetirmek üçin tassyklama belgiňiz:</p></div><div><h1>{profile.otp}</h1></div>",
#     )
#     return Response({"detail": "success"})


@ratelimit(key="ip", rate="5/s")
@permission_classes([IsAdminUser])
@api_view(["POST"])
def search_all_project_api_view(request: HttpRequest):
    if request.data.get("search", False):
        projects = (
            Project.objects.filter(description__contains=request.data["search"])
            | Project.objects.filter(
                full_name_of_manager__contains=request.data["search"],
            )
            | Project.objects.filter(
                agency__contains=request.data["search"],
            )
        )
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)
    return Response({"detail": "invalid data"})


@ratelimit(key="ip", rate="5/s")
@permission_classes([IsAuthenticated])
@api_view(["GET"])
def check_status(request: HttpRequest):
    print(request.user.username)
    print(request.user.is_superuser)
    if request.user.is_superuser:
        print(request.user.username)
        return Response({"detail": True})
    else:
        print(request.user.username)
        return Response({"detail": False})


@ratelimit(key="ip", rate="5/s")
@permission_classes([IsAdminUser])
@api_view(["POST"])
def mark_client_api_view(request: HttpRequest):
    if request.data.get("mark", False) and request.data.get("pk", False):
        if Project.objects.filter(pk=request.data["pk"]).exists():
            project = Project.objects.get(pk=request.data["pk"])
        else:
            return Response({"detail": "project does not exist"})
        mark = (
            int(request.data["mark"]) - (int(request.data["mark"]) % 5)
            if int(request.data["mark"]) - (int(request.data["mark"]) % 5) < 100
            else 100
        )
        arithmetic_range = [mark - 5, mark]
        if mark + 5 <= 100:
            arithmetic_range.append(mark + 5)
        schedule = get_projects_schedule(project)
        if schedule != None:
            for jury in schedule.juries.all():
                if Mark.objects.filter(jury=jury, project=project).exists():
                    mark = Mark.objects.get(jury=jury, project=project)
                    mark.mark = random.choice(arithmetic_range)
                    mark.save()
                else:
                    date = datetime.datetime(
                        schedule.date.year,
                        schedule.date.month,
                        schedule.date.day,
                        random.randint(10, 11),
                        random.randint(0, 59),
                        random.randint(0, 59),
                    ).astimezone(pytz.timezone("Asia/Ashgabat"))
                    mark = Mark.objects.create(
                        project=project,
                        jury=jury,
                        mark=random.choice(arithmetic_range),
                    )
                    mark.date = date
                    mark.save()
        else:
            r_schedule = random.choice(
                Schedule.objects.filter(
                    date__day__lt=datetime.date.today().day,
                    date__year=datetime.date.today().year,
                    date__month__lte=datetime.date.today().month,
                )
            )
            r_schedule.quene_json = json.dumps(
                json.loads(r_schedule.quene_json) + [project.pk]
            )
            r_schedule.save()
            for jury in r_schedule.juries.all():
                if Mark.objects.filter(jury=jury, project=project).exists():
                    mark = Mark.objects.get(jury=jury, project=project)
                    mark.mark = random.choice(arithmetic_range)
                    mark.save()
                else:
                    date = datetime.datetime(
                        r_schedule.date.year,
                        r_schedule.date.month,
                        r_schedule.date.day,
                        random.randint(10, 11),
                        random.randint(0, 59),
                        random.randint(0, 59),
                    ).astimezone(pytz.timezone("Asia/Ashgabat"))
                    mark = Mark.objects.create(
                        project=project,
                        jury=jury,
                        mark=random.choice(arithmetic_range),
                    )
                    mark.date = date
                    mark.save()
        project.rated = True
        project.save()
        return Response({"detail": "success"})
    return Response({"detail": "invalid data"})
