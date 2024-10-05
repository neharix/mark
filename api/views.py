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
    if (
        request.data.get("date", False)
        and request.data.get("schedule", False)
        and request.data.get("juries", False)
    ):

        if not Schedule.objects.filter(
            date=datetime.datetime.strptime(request.data["date"], "%d/%m/%Y")
        ).exists():
            schedule = Schedule.objects.create(
                quene_json=json.dumps(request.data["schedule"]),
                date=datetime.datetime.strptime(request.data["date"], "%d/%m/%Y"),
            )
            juries_pk = json.loads(request.data["juries"])
            for i in juries_pk:
                schedule.juries.add(i)
            schedule.save()
            return Response({"detail": "success"})
        else:
            return Response({"detail": "berlen senede tertip bellenildi"})
    return Response({"detail": "fail"})


# @api_view(["GET"])
# def devices_api_view(request: HttpRequest, slug: str):
#     devices = Device.objects.filter(device_type__short=slug)
#     devices_list = [DeviceContainer(device, slug) for device in devices]
#     serializer = DeviceSerializer(devices_list, many=True)
#     return Response(serializer.data)
