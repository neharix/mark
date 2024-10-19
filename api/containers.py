from django.contrib.auth.models import User

from main.models import Mark, Project


class UnratedProjectMarkContainer:
    def __init__(self, project: Project) -> None:
        self.name = project.description
        self.manager = project.full_name_of_manager
        self.direction = project.direction.name
        self.agency = project.agency
        marks_list = []
        for jury in User.objects.filter(groups__name="Jury"):
            total = 0
            for mark in Mark.objects.filter(project=project, jury=jury):
                total += mark.mark
            if total != 0:
                marks_list.append(total)
        self.percent = int(sum(marks_list) / len(marks_list))
