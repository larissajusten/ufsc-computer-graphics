from graphicObject import GraphicObject, Point, Segment, Wireframe
from displayFile import DisplayFile
import tkinter as tk
import math
from typing import Tuple

# ---------- Sistema Gráfico ----------
class GraphicsSystem:
    def __init__(self, canvas: tk.Canvas):
        self.canvas = canvas
        self.display_file = DisplayFile()
        self.origin = [0, 0]

        # Window (coordenadas do mundo)
        self.window_min = [-100.0, -100.0]
        self.window_max = [100.0, 100.0]

        # Viewport (coordenadas da tela)
        self.viewport = [0, 0, int(canvas["width"]), int(canvas["height"])]

    def draw(self):
        self.canvas.delete("all")
        for obj in self.display_file.objects:
            self.draw_object(obj)

    def reset(self):
        self.window_min = [-100.0, -100.0]
        self.window_max = [100.0, 100.0]
        self.draw()

    def window_to_viewport(self, xw, yw) -> Tuple[int, int]:
        wx_min, wy_min = self.window_min
        wx_max, wy_max = self.window_max
        vx_min, vy_min, vx_max, vy_max = self.viewport

        # Normalização
        x_norm = (xw - wx_min) / (wx_max - wx_min)
        y_norm = (yw - wy_min) / (wy_max - wy_min)

        # Escala uniforme (sem distorção)
        scale = min(
            (vx_max - vx_min) / (wx_max - wx_min),
            (vy_max - vy_min) / (wy_max - wy_min)
        )

        # Centro da viewport
        cx = (vx_max + vx_min) / 2
        cy = (vy_max + vy_min) / 2

        # Viewport coordenadas
        xv = cx + (x_norm - 0.5) * scale * (wx_max - wx_min)
        yv = cy - (y_norm - 0.5) * scale * (wy_max - wy_min)  # Inverter y

        return int(xv), int(yv)

    def draw_object(self, obj: GraphicObject):
        coords = [self.window_to_viewport(x, y) for x, y in obj.coordinates]

        if isinstance(obj, Point):
            x, y = coords[0]
            self.canvas.create_oval(x-2, y-2, x+2, y+2, fill="black")
        elif isinstance(obj, Segment):
            self.canvas.create_line(*coords[0], *coords[1], fill="blue")
        elif isinstance(obj, Wireframe):
            for i in range(len(coords)):
                x1, y1 = coords[i]
                x2, y2 = coords[(i + 1) % len(coords)]
                self.canvas.create_line(x1, y1, x2, y2, fill="green")

    def pan(self, dx, dy):
        self.window_min[0] += dx
        self.window_max[0] += dx
        self.window_min[1] += dy
        self.window_max[1] += dy
        self.draw()

    def zoom(self, factor):
        cx = (self.window_min[0] + self.window_max[0]) / 2
        cy = (self.window_min[1] + self.window_max[1]) / 2
        w = (self.window_max[0] - self.window_min[0]) * factor
        h = (self.window_max[1] - self.window_min[1]) * factor
        self.window_min = [cx - w / 2, cy - h / 2]
        self.window_max = [cx + w / 2, cy + h / 2]
        self.draw()

    def rotate(self, axis, angle):
        # Convert angle to radians
        angle_rad = math.radians(angle)

        # Rotation around the x-axis
        if axis == "x":
            for obj in self.display_file.objects:
                for i, (x, y) in enumerate(obj.coordinates):
                    new_x = x
                    new_y = y * math.cos(angle_rad) - x * math.sin(angle_rad)
                    obj.coordinates[i] = (new_x, new_y)

        # Rotation around the y-axis
        elif axis == "y":
            for obj in self.display_file.objects:
                for i, (x, y) in enumerate(obj.coordinates):
                    new_x = x * math.cos(angle_rad) - y * math.sin(angle_rad)
                    new_y = x * math.sin(angle_rad) + y * math.cos(angle_rad)
                    obj.coordinates[i] = (new_x, new_y)

        self.draw()
        pass