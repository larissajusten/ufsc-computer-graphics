import tkinter as tk
from tkinter import ttk

from typing import List, Tuple, Union
import math

# Trabalho 1.1 - Sistema básico com Window e Viewport

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

# ---------- Display File ----------
class DisplayFile:
    def __init__(self):
        self.objects: List[GraphicObject] = []

    def add_object(self, obj: GraphicObject):
        self.objects.append(obj)

# ---------- Sistema Gráfico ----------
class GraphicsSystem:
    def __init__(self, canvas: tk.Canvas):
        self.canvas = canvas
        self.display_file = DisplayFile()

        # Window (coordenadas do mundo)
        self.window_min = [-100.0, -100.0]
        self.window_max = [100.0, 100.0]

        # Viewport (coordenadas da tela)
        self.viewport = [0, 0, int(canvas["width"]), int(canvas["height"])]

    def draw(self):
        self.canvas.delete("all")
        for obj in self.display_file.objects:
            self.draw_object(obj)

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

# ---------- Aplicação principal ----------
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema Gráfico 2D")
        self.canvas = tk.Canvas(root, width=600, height=600, bg="white")
        self.canvas.pack()

        self.graphics = GraphicsSystem(self.canvas)

        tk.Label(root, text="Teste").pack(anchor="w", padx=10)
        self.entry = tk.Entry(root)
        self.entry.pack(fill="x")

        self.type_var = tk.StringVar(value="Point")
        tk.OptionMenu(root, self.type_var, "Point", "Segment", "Wireframe").pack()

        tk.Button(root, text="Adicionar", command=self.add_object).pack()

        tk.Button(root, text="Incluir Objeto", command=self.show_add_object_dialog).pack()


        self.bind_keys()

    def bind_keys(self):
        self.root.bind("<Left>", lambda e: self.graphics.pan(-10, 0))
        self.root.bind("<Right>", lambda e: self.graphics.pan(10, 0))
        self.root.bind("<Up>", lambda e: self.graphics.pan(0, 10))
        self.root.bind("<Down>", lambda e: self.graphics.pan(0, -10))
        self.root.bind("<plus>", lambda e: self.graphics.zoom(0.9))
        self.root.bind("<minus>", lambda e: self.graphics.zoom(1.1))

    def add_object(self):
        coords = list(eval(self.entry.get()))
        obj_type = self.type_var.get()

        if obj_type == "Point" and len(coords) == 1:
            obj = Point("Ponto", coords)
        elif obj_type == "Segment" and len(coords) == 2:
            obj = Segment("Segmento", coords)
        elif obj_type == "Wireframe" and len(coords) >= 3:
            obj = Wireframe("Wireframe", coords)
        else:
            print("Coordenadas inválidas para o tipo:", obj_type)
            return

        self.graphics.display_file.add_object(obj)
        self.graphics.draw()

    def show_point_input(self, point_frame):
        tk.Label(point_frame, text="Coordenadas do Ponto").grid(row=0, column=0, columnspan=4, pady=(0, 5))
        # x:
        tk.Label(point_frame, text="x:").grid(row=1, column=0, sticky="w", padx=(0, 5))
        x_entry = tk.Entry(point_frame, width=5)
        x_entry.grid(row=1, column=1, sticky="w", padx=(0, 15))
        # y:
        tk.Label(point_frame, text="y:").grid(row=1, column=2, sticky="w", padx=(0, 5))
        y_entry = tk.Entry(point_frame, width=5)
        y_entry.grid(row=1, column=3, sticky="w")

    def show_axis_input(self, axis_frame):
        #Ponto inicial
        initial_point = tk.Frame(axis_frame)

        tk.Label(axis_frame, text="Coordenadas do Ponto Inicial").grid(row=0, column=0, columnspan=4, pady=(0, 5), sticky="w")
        #x1:
        tk.Label(axis_frame, text="x1:").grid(row=1, column=0, sticky="w", padx=(0, 5))
        x1_entry = tk.Entry(axis_frame, width=5)
        x1_entry.grid(row=1, column=1, sticky="w", padx=(0, 15))
        # y1:
        tk.Label(axis_frame, text="y1:").grid(row=1, column=2, sticky="w", padx=(0, 5))
        y1_entry = tk.Entry(axis_frame, width=5)
        y1_entry.grid(row=1, column=3, sticky="w")

        #Ponto final
        end_point = tk.Frame(axis_frame)

        tk.Label(axis_frame, text="Coordenadas do Ponto Final").grid(row=2, column=0, columnspan=4, pady=(20, 5), sticky="w")
        #x2:
        tk.Label(axis_frame, text="x2:").grid(row=3, column=0, sticky="w", padx=(0, 5))
        x2_entry = tk.Entry(axis_frame, width=5)
        x2_entry.grid(row=3, column=1, sticky="w", padx=(0, 15))
        # y2:
        tk.Label(axis_frame, text="y2:").grid(row=3, column=2, sticky="w", padx=(0, 5))
        y2_entry = tk.Entry(axis_frame, width=5)
        y2_entry.grid(row=3, column=3, sticky="w")

    def show_add_object_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Incluir Objeto")

        # ---------- Campo nome ----------
        tk.Label(dialog, text="Nome").pack(anchor="w", padx=10)
        name_entry = tk.Entry(dialog)
        name_entry.pack(fill="x", padx=10, pady=(0, 10))

        # ---------- Notebook ----------
        notebook = ttk.Notebook(dialog)
        notebook.pack(padx=10, pady=10)

        # ---------- Abas ----------
        point_frame = tk.Frame(notebook)
        axis_frame = tk.Frame(notebook)
        wireframe_frame = tk.Frame(notebook)

        notebook.add(point_frame, text="Ponto")
        notebook.add(axis_frame, text="Reta")
        notebook.add(wireframe_frame, text="Wireframe")

        # ---------- Aba Ponto ----------
        self.show_point_input(point_frame)

        # ---------- Aba Reta ----------
        self.show_axis_input(axis_frame)

        # ---------- Aba Wireframe ----------
        tk.Label(wireframe_frame, text="Novo pontooooo").grid(row=0, column=0, columnspan=4, pady=(0, 5))
        # x:
        tk.Label(wireframe_frame, text="x:").grid(row=1, column=0, sticky="w", padx=(0, 5))
        x_entry = tk.Entry(wireframe_frame, width=5)
        x_entry.grid(row=1, column=1, sticky="w", padx=(0, 15))
        # y:
        tk.Label(wireframe_frame, text="y:").grid(row=1, column=2, sticky="w", padx=(0, 5))
        y_entry = tk.Entry(wireframe_frame, width=5)
        y_entry.grid(row=1, column=3, sticky="w")
        # ---------- Aba Curvas ----------

        # ---------- Notebook ----------
        # ---------- Notebook ----------
        # ---------- Notebook ----------

# ---------- Rodar ----------
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
