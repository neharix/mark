import json

from .models import *


class ScheduleContainer:
    def __init__(self, schedule: Schedule) -> None:
        self.pk = schedule.pk
        self.projects_count = f"{len(json.loads(schedule.quene_json))} taslama"
        self.date = schedule.date.strftime("%d.%m.%Y")
        self.juries_count = f"{schedule.juries.count()} emin agza"
