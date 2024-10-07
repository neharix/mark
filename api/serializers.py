from django.contrib.auth.models import User
from rest_framework import serializers

from main.models import *


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["pk", "description", "agency", "full_name_of_manager"]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["pk", "id", "first_name", "last_name"]
