import json

from .models import Project, Schedule


def get_projects_schedule(project: Project):
    for schedule in Schedule.objects.all():
        if project.pk in json.loads(schedule.quene_json):
            return schedule
    return None
