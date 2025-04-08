from typing import List, Tuple

# ---------- Classes base ----------
class GraphicObject:
    def __init__(self, name: str, coordinates: List[Tuple[float, float]]):
        self.name = name
        self.coordinates = coordinates

    def get_type(self):
        return self.__class__.__name__

class Point(GraphicObject):
    pass

class Segment(GraphicObject):
    pass

class Wireframe(GraphicObject):  # Polígono (lista de pontos interligados)
    pass