from rest_framework import serializers

from main.models import *


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["pk", "description", "agency", "full_name_of_manager"]
