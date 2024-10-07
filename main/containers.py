import json

import pytz
from django.contrib.auth.models import User

from .models import *


class ScheduleContainer:
    def __init__(self, schedule: Schedule) -> None:
        self.pk = schedule.pk
        self.projects_count = f"{len(json.loads(schedule.quene_json))} taslama"
        self.date = schedule.date.strftime("%d.%m.%Y")
        self.juries_count = f"{schedule.juries.count()} emin agza"


class DirectionContainer:
    def __init__(self, direction: Direction) -> None:
        self.name = direction.name
        self.projects_count = Project.objects.filter(direction=direction).count()


class ProjectMarkContainer:
    def __init__(self, project: Project) -> None:
        self.name = project.description
        marks_list = []
        for jury in User.objects.filter(groups__name="Jury"):
            total = 0
            for mark in Mark.objects.filter(project=project, jury=jury):
                total += mark.mark
            if total != 0:
                marks_list.append(total)
        self.percent = int(sum(marks_list) / len(marks_list))


class MarkContainer:
    def __init__(self, mark: Mark) -> None:
        self.criteria = mark.criteria
        self.jury = mark.jury
        self.mark = mark.mark
        self.description = mark.description
        self.date = mark.date.astimezone(pytz.timezone("Asia/Ashgabat")).strftime(
            "%d.%m.%Y %H:%M:%S"
        )
