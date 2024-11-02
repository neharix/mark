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
        self.pk = project.pk
        self.name = project.description
        self.manager = project.full_name_of_manager
        self.direction = project.direction.name
        self.agency = project.agency
        self.marks_list = []
        self.mark_objects_list = []
        for jury in User.objects.filter(groups__name="Jury"):
            if Profile.objects.get(user=jury).active_jury:
                total = 0
                for mark in Mark.objects.filter(project=project, jury=jury):
                    total += mark.mark
                    self.mark_objects_list.append(mark)
                    self.mark_date = mark.date
                if Mark.objects.filter(project=project, jury=jury).count() != 0:
                    self.marks_list.append(total)

        try:
            self.percent = round(sum(self.marks_list) / len(self.marks_list), 3)
        except ZeroDivisionError:
            self.percent = 0


class MarkContainer:
    def __init__(self, mark: Mark) -> None:
        self.jury = mark.jury
        self.mark = mark.mark
        self.description = mark.description
        self.date = mark.date.astimezone(pytz.timezone("Asia/Ashgabat")).strftime(
            "%d.%m.%Y %H:%M:%S"
        )


class UnparticipatedJuryContainer:
    def __init__(self, jury: User):
        self.jury = jury

    is_ujc = True


class SecondaryMarkContainer:
    def __init__(self, mark: Mark) -> None:
        self.pk = mark.pk
        self.jury = mark.jury
        self.project = mark.project
        self.mark = mark.mark
        self.description = mark.description
        self.date = mark.date.astimezone(pytz.timezone("Asia/Ashgabat"))
