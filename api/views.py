import json

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


# @api_view(["GET"])
# def devices_api_view(request: HttpRequest, slug: str):
#     devices = Device.objects.filter(device_type__short=slug)
#     devices_list = [DeviceContainer(device, slug) for device in devices]
#     serializer = DeviceSerializer(devices_list, many=True)
#     return Response(serializer.data)
