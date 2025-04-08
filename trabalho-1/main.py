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

        self.viewportLabel = tk.Label(root, text="Viewport")
        self.viewportLabel.grid(column=1, row=0, rowspan=1, columnspan=1, sticky="w")

        self.canvas = tk.Canvas(root, highlightthickness=1, highlightbackground="gray")
        self.canvas.grid(column=1, row=1, columnspan=1, rowspan=5)

        self.graphics = GraphicsSystem(self.canvas)

        # Frame Menu de funções (/menu_frame)
        menu_frame = tk.Frame(self.root, highlightbackground="gray", highlightthickness=1, padx=4, pady=4)
        menu_frame.grid(row=0, column=0, columnspan=1, rowspan=6, sticky="nsw")
        tk.Label(menu_frame, text="Menu de Funções:").grid(row=0, column=0, sticky="w")

        # Frame Menu de objetos (/menu_frame/objects_frame)
        objects_frame = tk.Frame(menu_frame, padx=4, pady=4)
        objects_frame.grid(row=1, column=0)
        tk.Label(objects_frame, text="Objetos:").grid(row=1, column=0, sticky="w")

        choices_var = tk.StringVar(value= [obj.name for obj in self.objects])

        self.listbox = tk.Listbox(objects_frame, listvariable=choices_var, height=3, exportselection=False, highlightbackground="gray", highlightthickness=1)
        self.listbox.grid(row=2, column=0, rowspan=2, padx=5, pady=5)

        self.listbox.bind("<<ListboxSelect>>", self.on_select)

        # Frame Window (/menu_frame/window_frame)
        window_frame = tk.Frame(menu_frame, highlightbackground="gray", highlightthickness=1, padx=4, pady=4)
        window_frame.grid(row=2, column=0)
        tk.Label(window_frame, text="Window:").grid(row=0, column=0, sticky="w")
        
        tk.Label(window_frame, text="Passo:").grid(row=1, column=0, columnspan=1, sticky="w")
        self.step = tk.Entry(window_frame, width=6).grid(row=1, column=1, padx=2, pady=2, sticky="ew")
        tk.Label(window_frame, text="%").grid(row=1, column=2, columnspan=1, sticky="w")

        tk.Button(window_frame, text="In", command=lambda: None).grid(row=2, column=2)
        tk.Button(window_frame, text="Out", command=lambda: None).grid(row=4, column=2)

        buttonUp_frame = tk.Frame(window_frame)
        buttonUp_frame.grid(row=2, column=0, columnspan=2)

        buttonDown_frame = tk.Frame(window_frame)
        buttonDown_frame.grid(row=4, column=0, columnspan=2)

        tk.Button(buttonUp_frame, text="Up", command=lambda e: self.graphics.pan(0, self.step)).pack()
        tk.Button(window_frame, text="Left", command=lambda e: self.graphics.pan(-self.step, 0)).grid(row=3, column=0, sticky="e")
        tk.Button(window_frame, text="Right", command=lambda e: self.graphics.pan(self.step, 0)).grid(row=3, column=1, sticky="w")
        tk.Button(buttonDown_frame, text="Down", command=lambda e: self.graphics.pan(0, -self.step)).pack()
        
        # Frame Rotação (/menu_frame/window_frame/rotation_frame)
        rotation_frame = tk.Frame(window_frame, highlightbackground="gray", highlightthickness=1, padx=4, pady=4)
        rotation_frame.grid(row=5, column=0, pady=4, columnspan=3, sticky="ew")
        tk.Label(rotation_frame, text="Rotação:").grid(row=0, column=0, columnspan=3, sticky="w")

        tk.Label(rotation_frame, text="Graus:").grid(row=1, column=0, sticky="w")
        self.degree = tk.Entry(rotation_frame, width=8).grid(row=1, column=1, columnspan=1)
        tk.Label(rotation_frame, text="°").grid(row=1, column=2, sticky="w")

        buttons_frame = tk.Frame(rotation_frame)
        buttons_frame.grid(row=2, column=0, columnspan=12)

        tk.Button(buttons_frame, text="X", command=lambda: None).pack(side=tk.LEFT, padx=5, pady=3)
        tk.Button(buttons_frame, text="Y", command=lambda: None).pack(side=tk.LEFT, padx=5, pady=3)
        tk.Button(buttons_frame, text="Z", command=lambda: None).pack(side=tk.LEFT, padx=5, pady=3)

        # Zoom (/menu_frame/window_frame)
        zoom_frame = tk.Frame(window_frame)
        zoom_frame.grid(row=6, column=0, pady=4, columnspan=3, sticky="ew")
        tk.Label(zoom_frame, text="Zoom").grid(row=0, column=0, sticky="w")
        tk.Button(zoom_frame, text="+", command=lambda: None).grid(row=0, column=1, padx=5)
        tk.Button(zoom_frame, text="-", command=lambda: None).grid(row=0, column=2, padx=5)
        
        tk.Button(window_frame, text="Set window", command=lambda: None).grid(row=7, column=0, columnspan=3, pady=5, sticky="ew")

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

# ---------- Rodar ----------
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
