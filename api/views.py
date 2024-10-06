import datetime
import json

from django.contrib.auth.models import Group
from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.request import HttpRequest
from rest_framework.response import Response

from main.models import *

from .serializers import *


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


@api_view(["GET"])
def juries_api_view(request: HttpRequest):
    users = User.objects.all()
    juries = []
    for user in users:
        if user.groups.contains(Group.objects.get(name="Jury")):
            juries.append(user)
    serializer = UserSerializer(juries, many=True)
    return Response(serializer.data)


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


# @api_view(["GET"])
# def devices_api_view(request: HttpRequest, slug: str):
#     devices = Device.objects.filter(device_type__short=slug)
#     devices_list = [DeviceContainer(device, slug) for device in devices]
#     serializer = DeviceSerializer(devices_list, many=True)
#     return Response(serializer.data)
