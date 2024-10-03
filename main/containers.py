import json

from .models import *


class ScheduleContainer:
    def __init__(self, quene: Schedule) -> None:
        self.projects_count = f"{len(json.loads(quene.quene_json))} taslama"
        self.date = quene.date.strftime("%d.%m.%Y")
        self.juries_count = f"{quene.juries.count()} emin agza"
