from typing import List
from graphicObject import GraphicObject

# ---------- Display File ----------
class DisplayFile:
    def __init__(self):
        self.objects: List[GraphicObject] = []

    def add_object(self, obj: GraphicObject):
        self.objects.append(obj)