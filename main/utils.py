import json

from .models import Mark, Project, Schedule


def get_projects_schedule(project: Project):
    for schedule in Schedule.objects.all():
        if project.pk in json.loads(schedule.quene_json):
            return schedule
    return None


def get_unparticipated_juries(project: Project, schedule: Schedule):
    juries = []
    for jury in schedule.juries.all():
        if not Mark.objects.filter(jury=jury, project=project).exists():
            juries.append(jury)
    return juries


def numerate_containers(list_of_objects):
    temp_list = []
    index = 1
    for obj in list_of_objects:
        obj.number = index
        temp_list.append(obj)
        index += 1
    return temp_list
