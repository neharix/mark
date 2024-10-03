import json

from .models import *


class QueneContainer:
    def __init__(self, quene: Quene) -> None:
        self.projects_count = f"{len(json.loads(quene.quene_json))} taslama"
        self.date = quene.date.strftime("%d.%m.%Y")
        self.juries_count = f"{quene.juries.count()} emin agza"
