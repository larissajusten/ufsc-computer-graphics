from typing import List, Tuple
from dataclasses import dataclass

@dataclass
class GraphicObject:
    name: str
    type: str
    coordinates: List[Tuple[float, float]]
