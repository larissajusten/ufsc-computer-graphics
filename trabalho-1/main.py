import tkinter as tk
from typing import List, Tuple

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
        self.objects = []

        self.root = root
        self.root.title("Sistema Gráfico 2D")

        self.viewportLabel = tk.Label(root, text="Viewport", fg="black", anchor="w")
        self.viewportLabel.grid(column=1, row=0, rowspan=1, columnspan=1, sticky="w")

        self.canvas = tk.Canvas(root, highlightthickness=1, highlightbackground="gray")
        self.canvas.grid(column=1, row=1, columnspan=1, rowspan=5)

        self.graphics = GraphicsSystem(self.canvas)

        # Menu de funções
        menu_frame = tk.Frame(self.root, bg="gray", highlightbackground="gray", highlightthickness=1, padx=4, pady=4)
        menu_frame.grid(row=0, column=0, columnspan=1, rowspan=6, sticky="nsw")
        tk.Label(menu_frame, text="Menu de Funções:").grid(row=0, column=0, sticky="w")

        # Menu de objetos
        objects_frame = tk.Frame(menu_frame, padx=4, pady=4)
        objects_frame.grid(row=1, column=0, sticky="nsw")
        tk.Label(objects_frame, text="Objetos:").grid(row=1, column=0, sticky="w")

        choices_var = tk.StringVar(value= [obj.name for obj in self.objects])

        self.listbox = tk.Listbox(objects_frame, listvariable=choices_var, height=3, exportselection=False, highlightbackground="gray", highlightthickness=1)
        self.listbox.grid(row=2, column=0, rowspan=2, padx=5, pady=5)

        self.listbox.bind("<<ListboxSelect>>", self.on_select)

        # Window
        window_frame = tk.Frame(menu_frame, highlightbackground="gray", highlightthickness=1, padx=4, pady=4)
        window_frame.grid(row=2, column=0, sticky="nsw")
        tk.Label(window_frame, text="Window:").grid(row=0, column=0, sticky="w")
        
        tk.Label(window_frame, text="Passo:").grid(row=1, column=0, sticky="w")
        self.passo = tk.Entry(window_frame).grid(row=1, column=1, padx=5, pady=5)
        
        #tk.Button(menu_frame, text="Adicionar", command=lambda: self.add_object()).grid(row=7, column=0, padx=5, pady=5)

        self.bind_keys()

    def bind_keys(self):
        self.root.bind("<Left>", lambda e: self.graphics.pan(-10, 0))
        self.root.bind("<Right>", lambda e: self.graphics.pan(10, 0))
        self.root.bind("<Up>", lambda e: self.graphics.pan(0, 10))
        self.root.bind("<Down>", lambda e: self.graphics.pan(0, -10))
        self.root.bind("<plus>", lambda e: self.graphics.zoom(0.9))
        self.root.bind("<minus>", lambda e: self.graphics.zoom(1.1))

    def on_select(event):
        widget = event.widget
        index = widget.curselection()
        if index:
            selected_item = widget.get(index)
            print("Selecionado:", selected_item)

    # def add_object(self, obj_type):
    #     if obj_type == "Point" and len(coords) == 1:
    #         obj = Point("Ponto", coords)
    #     elif obj_type == "Segment" and len(coords) == 2:
    #         obj = Segment("Segmento", coords)
    #     elif obj_type == "Wireframe" and len(coords) >= 3:
    #         obj = Wireframe("Wireframe", coords)
    #     else:
    #         print("Coordenadas inválidas para o tipo:", obj_type)
    #         return

    #     self.graphics.display_file.add_object(obj)
    #     self.graphics.draw()

# ---------- Rodar ----------
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
