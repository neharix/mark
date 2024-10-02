from django.contrib import admin

from .models import *


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["username", "email", "pk"]


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ["pk", "full_name_of_manager", "personality_type"]


@admin.register(Direction)
class DirectionAdmin(admin.ModelAdmin):
    list_display = ["pk", "name"]
