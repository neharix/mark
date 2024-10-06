from django.contrib import admin

from .models import *


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["username", "email", "pk"]


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ["pk", "date", "quene_json"]


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ["pk", "full_name_of_manager", "personality_type", "description"]


@admin.register(Criteria)
class CriteriaAdmin(admin.ModelAdmin):
    list_display = ["pk", "expression", "max_value"]


@admin.register(Direction)
class DirectionAdmin(admin.ModelAdmin):
    list_display = ["pk", "name"]


@admin.register(Mark)
class MarkAdmin(admin.ModelAdmin):
    list_display = ["pk", "criteria", "project", "mark", "jury", "date"]
