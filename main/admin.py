from django.contrib import admin
from django.contrib.admin.models import LogEntry

from .models import *

admin.site.register(LogEntry)


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ["pk", "date", "quene_json"]


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ["pk", "full_name_of_manager", "description"]


@admin.register(Direction)
class DirectionAdmin(admin.ModelAdmin):
    list_display = ["pk", "name"]


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["pk", "user", "password"]
    readonly_fields = ("user", "password")


@admin.register(Mark)
class MarkAdmin(admin.ModelAdmin):
    list_display = ["pk", "project", "mark", "jury", "date"]
    readonly_fields = (
        "pk",
        "project",
        "mark",
        "description",
        "jury",
        "date",
    )
