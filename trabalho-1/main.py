import tkinter as tk
from typing import List, Tuple
import math

INITIAL_STEP = 10
INITIAL_DEGREE = 45

# Trabalho 1.1 - Sistema básico com Window e Viewport

def set_example_data(self) -> List[Tuple[str, List[Tuple[float, float]]]]:
    objects = [
        Point("Ponto 1", [(0, 0)]),
        Segment("Segmento 1", [(10, 10), (50, 50)]),
        Wireframe("Polígono 1", [(20, 20), (30, 40), (40, 20)]),
    ]
    
    for obj in objects:
        self.graphics.display_file.add_object(obj)
    self.graphics.draw()
    return objects

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
        self.origin = [0, 0]
        self.scale = 1.0

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

# ---------- Aplicação principal ----------
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema Gráfico 2D")
        self.logs_data = []

        # Frame da Viewport
        viewport_frame = tk.Frame(root)
        viewport_frame.grid(column=1, row=0, columnspan=1, rowspan=12, sticky="nsew")

        tk.Label(viewport_frame, text="Viewport", bg="lightgray").grid(column=0, row=0, sticky="ew")

        canva_frame = tk.Frame(viewport_frame, bg="lightgray")
        canva_frame.grid(column=0, row=1, sticky="nsew")
        self.canvas = tk.Canvas(canva_frame, highlightthickness=1, highlightbackground="gray")
        self.canvas.pack(fill="both", expand=True)

        logs_frame = tk.LabelFrame(viewport_frame, text="Logs", highlightbackground="gray", highlightthickness=1, padx=4, pady=4)
        logs_frame.grid(column=0, row=2, sticky="nsew")
        self.logs = tk.Text(logs_frame, height=5, wrap="word", state="disabled", bg="white", fg="black")
        self.logs.grid(column=0, row=1, sticky="nsew")

        self.logs.config(state="normal")
        for log in self.logs_data:
            self.logs.insert("end", log , "\n")
        self.logs.config(state="disabled")

        self.graphics = GraphicsSystem(self.canvas)
        # -- REMOVE COMENT 
        # self.objects = self.graphics.display_file.objects
        self.objects = set_example_data(self)

        self.selected_object = None

        # Frame do Menu de Funções
        menu_frame = tk.Frame(self.root, highlightbackground="gray", highlightthickness=1, padx=4, pady=4)
        menu_frame.grid(row=0, column=0, rowspan=12, sticky="nsw")
        tk.Label(menu_frame, text="Menu de Funções:").grid(row=0, column=0, sticky="w")

        # Frame de Objetos
        objects_frame = tk.LabelFrame(menu_frame, text="Objetos", padx=4, pady=4)
        objects_frame.grid(row=1, column=0, sticky="ew")
        
        choices_var = tk.StringVar(value=[obj.name for obj in self.objects])
        self.listbox = tk.Listbox(objects_frame, listvariable=choices_var, height=5, exportselection=False, highlightbackground="gray", highlightthickness=1)
        self.listbox.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        self.listbox.bind("<<ListboxSelect>>", self.on_select)
        self.update_objects_list()

        # Frame da Window
        window_frame = tk.LabelFrame(menu_frame, text="Window", padx=4, pady=4, bg="lightgray")
        window_frame.grid(row=2, column=0, sticky="ew")

        tk.Label(window_frame, text="Passo:", bg="lightgray").grid(row=0, column=0, sticky="w")
        self.step = tk.Entry(window_frame, width=6)
        self.step.insert(0, INITIAL_STEP)
        self.step.grid(row=0, column=1, padx=2, pady=2, sticky="ew")
        tk.Label(window_frame, text="%", bg="lightgray").grid(row=0, column=2, sticky="w")

        # tk.Button(window_frame, text="In", command=lambda: self.graphics.zoom(0.9)).grid(row=1, column=2)
        # tk.Button(window_frame, text="Out", command=lambda: self.graphics.zoom(1.1)).grid(row=3, column=2)

        buttonUp_frame = tk.Frame(window_frame)
        buttonUp_frame.grid(row=1, column=0, columnspan=2)

        buttonDown_frame = tk.Frame(window_frame)
        buttonDown_frame.grid(row=3, column=0, columnspan=2)

        tk.Button(buttonUp_frame, text="Up", command=lambda: [self.graphics.pan(0, int(self.step.get() or 10)), self.update_logs(f"Move Up in {self.step.get()} steps")]).pack()
        tk.Button(window_frame, text="Left", command=lambda: [self.graphics.pan(-int(self.step.get() or 10), 0), self.update_logs(f"Move Left in {self.step.get()} steps")]).grid(row=2, column=0, sticky="e")
        tk.Button(window_frame, text="Right", command=lambda: [self.graphics.pan(int(self.step.get() or 10), 0), self.update_logs(f"Move Right in {self.step.get()} steps")]).grid(row=2, column=1, sticky="w")
        tk.Button(buttonDown_frame, text="Down", command=lambda: [self.graphics.pan(0, -int(self.step.get() or 10)), self.update_logs(f"Move Down in {self.step.get()} steps")]).pack()

        # Frame de Rotação
        rotation_frame = tk.LabelFrame(window_frame, text="Rotação", padx=4, pady=4, bg="lightgray")
        rotation_frame.grid(row=4, column=0, columnspan=3, pady=4, sticky="ew")

        tk.Label(rotation_frame, text="Graus:", bg="lightgray").grid(row=0, column=0, sticky="w")
        self.degree = tk.Entry(rotation_frame, width=8)
        self.degree.insert(0, INITIAL_DEGREE)
        self.degree.grid(row=0, column=1, padx=2, pady=2, sticky="ew")
        tk.Label(rotation_frame, text="°", bg="lightgray").grid(row=0, column=2, sticky="w")

        tk.Button(rotation_frame, text="X", command=lambda: [self.graphics.rotate("x", float(self.degree.get() or 0)), self.update_logs(f"Move {self.degree.get()}° in X")]).grid(row=1, column=0, padx=5, pady=3)
        tk.Button(rotation_frame, text="Y", command=lambda: [self.graphics.rotate("y", float(self.degree.get() or 0)), self.update_logs(f"Move {self.degree.get()}° in Y")]).grid(row=1, column=1, padx=5, pady=3)

        # Frame de Zoom
        zoom_frame = tk.Frame(window_frame, bg="lightgray")
        zoom_frame.grid(row=5, column=0, pady=4, columnspan=3, sticky="ew")
    
        tk.Label(zoom_frame, text="Zoom", bg="lightgray").grid(row=0, column=0, sticky="w")
        tk.Button(zoom_frame, text="+", command=lambda: [self.graphics.zoom(0.9), self.update_logs("Zoom In")]).grid(row=0, column=1, padx=5)
        tk.Button(zoom_frame, text="-", command=lambda: [self.graphics.zoom(1.1), self.update_logs("Zoom Out")]).grid(row=0, column=2, padx=5)

        tk.Button(window_frame, text="Reset Window", command=lambda: [self.graphics.reset(), self.update_logs("Window Reset")]).grid(row=6, column=0, columnspan=3, pady=5, sticky="ew")

        tk.Button(window_frame, text="Adicionar", command=lambda: self.open_add_object_dialog()).grid(row=7, column=0, columnspan=3, sticky="ew")

        self.bind_keys()

    def bind_keys(self):
        self.root.bind("<Left>", lambda e: self.graphics.pan(-10, 0))
        self.root.bind("<Right>", lambda e: self.graphics.pan(10, 0))
        self.root.bind("<Up>", lambda e: self.graphics.pan(0, 10))
        self.root.bind("<Down>", lambda e: self.graphics.pan(0, -10))
        self.root.bind("<plus>", lambda e: self.graphics.zoom(0.9))
        self.root.bind("<minus>", lambda e: self.graphics.zoom(1.1))
        self.root.bind("<ButtonPress-1>", self.start_pan)
        self.root.bind("<B1-Motion>", self.do_pan)
        self.root.bind("<MouseWheel>", self.zoom)  # Windows/Mac
        self.root.bind("<Button-4>", self.zoom)    # Linux scroll up
        self.root.bind("<Button-5>", self.zoom)

    def open_add_object_dialog(self):
        self.add_object_window = tk.Toplevel(self.root)
        self.add_object_window.title("Adicionar Objeto")

        tk.Label(self.add_object_window, text="Tipo de Objeto:").grid(row=0, column=0, sticky="w")
        self.type_var = tk.StringVar(value="Point")
        self.type_menu = tk.OptionMenu(self.add_object_window, self.type_var, "Point", "Segment", "Wireframe")
        self.type_menu.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.add_object_window, text="Coordenadas:").grid(row=1, column=0, sticky="w")
        self.entry = tk.Entry(self.add_object_window)
        self.entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Button(self.add_object_window, text="Adicionar", command=self.add_object).grid(row=2, columnspan=2, pady=5)


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
            self.update_logs(f"Coordenadas inválidas para o tipo: {obj_type}")
            return

        self.graphics.display_file.add_object(obj)
        self.graphics.draw()

    def update_objects_list(self):
        choices_var = tk.StringVar(value=[obj.name for obj in self.objects])
        self.listbox.config(listvariable=choices_var)
        self.root.after(500, self.update_objects_list)  # Update every 500ms

    def on_select(self, event: tk.Event):
        widget: tk.Listbox = event.widget
        index = widget.curselection()
        if index:
            selected_item = widget.get(index)
            self.selected_object = next((obj for obj in self.objects if obj.name == selected_item), None)
            self.logs_data.append(selected_item)
            self.update_logs(f"Objeto selecionado: {selected_item}")

    def update_logs(self, message):
        self.logs.config(state="normal")
        self.logs.insert("end", message + "\n")
        self.logs.config(state="disabled")
        self.logs.yview(tk.END)

    def start_pan(self, event: tk.Event):
        self.canvas.scan_mark(event.x, event.y)

    def do_pan(self, event: tk.Event):
        self.canvas.scan_dragto(event.x, event.y, gain=1)

    def zoom(self, event: tk.Event):
        factor = 1.1 if (event.delta > 0 or event.num == 4) else 0.9
        self.scale *= factor
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
        self.scale_all(x, y, factor)

    def scale_all(self, x, y, scale):
        self.canvas.scale("all", x, y, scale, scale)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

# ---------- Rodar ----------
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
