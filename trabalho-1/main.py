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

        return x_entry, y_entry

    def show_axis_input(self, axis_frame):
        #Ponto inicial
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

        return x1_entry, y1_entry, x2_entry, y2_entry

    def show_wireframe_input(self, wireframe_frame):
        #Label Novo Ponto
        tk.Label(wireframe_frame, text="Novo ponto:").grid(row=0, column=0, columnspan=4, padx=(2,0), pady=(0, 5), sticky="w")
        # x:
        tk.Label(wireframe_frame, text="x:").grid(row=1, column=0, sticky="w", padx=(0, 5))
        x_entry = tk.Entry(wireframe_frame, width=5)
        x_entry.grid(row=1, column=1, sticky="w", padx=(0, 15))
        # y:
        tk.Label(wireframe_frame, text="y:").grid(row=1, column=2, sticky="w", padx=(0, 5))
        y_entry = tk.Entry(wireframe_frame, width=5)
        y_entry.grid(row=1, column=3, sticky="w")

        wireframe_points: List[Tuple[float, float]] = []

        #Botão de adicionar
        add_button = tk.Button(wireframe_frame, text="Adicionar", command=lambda: self.add_wireframe_points(wireframe_points, x_entry, y_entry, point_list_box))
        add_button.grid(row=3, column=0,columnspan=4, pady=5)

        #Label de Pontos adicionados
        tk.Label(wireframe_frame, text="Pontos adicionados:").grid(row=4, column=0, columnspan=4, padx=(2,0), pady=(10,5), sticky="w")

        #Listbox de pontos
        point_list_box = point_listbox = tk.Listbox(wireframe_frame, height=5, width=30)
        point_listbox.grid(row=5, column=0, columnspan=4, sticky="w")

        return wireframe_points, point_list_box


    def add_wireframe_points(self, points_list: List, x_entry: tk.Entry, y_entry: tk.Entry, list_box: tk.Listbox):
        try:
            x = float(x_entry.get())
            y = float(y_entry.get())

            points_list.append((x, y))
            list_box.insert(tk.END, f"({x}, {y})")

            x_entry.delete(0, tk.END)
            y_entry.delete(0, tk.END)

            return points_list
        except ValueError:
            print("Coordenadas inválidas")
    
    def on_ok(self, dialog, name_entry, tab_index,
          x_entry=None, y_entry=None,
          x1_entry=None, y1_entry=None, x2_entry=None, y2_entry=None,
          wireframe_points=None):
        try:
            name = name_entry.get().strip() or "Objeto"

            if tab_index == 0 and x_entry and y_entry:
                # Aba Ponto
                x = float(x_entry.get())
                y = float(y_entry.get())
                obj = Point(name, [(x, y)])

            elif tab_index == 1 and all([x1_entry, y1_entry, x2_entry, y2_entry]):
                # Aba Reta
                x1 = float(x1_entry.get())
                y1 = float(y1_entry.get())
                x2 = float(x2_entry.get())
                y2 = float(y2_entry.get())
                obj = Segment(name, [(x1, y1), (x2, y2)])

            elif tab_index == 2 and wireframe_points is not None:
                # Aba Wireframe
                if len(wireframe_points) < 3:
                    print("Wireframe precisa de pelo menos 3 pontos.")
                    return
                obj = Wireframe(name, wireframe_points.copy())

            else:
                print("Tipo de objeto ou parâmetros inválidos.")
                return

            # Adiciona e desenha
            self.graphics.display_file.add_object(obj)
            self.graphics.draw()
            dialog.destroy()

        except ValueError:
            print("Erro: valores inválidos nos campos")

    def on_cancel(self, dialog):
        dialog.destroy()
   

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
        x_entry, y_entry = self.show_point_input(point_frame)

        # ---------- Aba Reta ----------
        x1_entry, y1_entry, x2_entry, y2_entry = self.show_axis_input(axis_frame)

        # ---------- Aba Wireframe ----------
        wireframe_points, point_list_box = self.show_wireframe_input(wireframe_frame)

        # ---------- Aba Curvas ----------

        # ---------- Botões ----------
        button_frame = tk.Frame(dialog)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Cancelar",
            command=lambda: self.on_cancel(dialog)).grid(row=0, column=0, padx=10)

        tk.Button(button_frame, text="OK",
            command=lambda: self.on_ok(
                dialog,
                name_entry,
                notebook.index(notebook.select()),
                x_entry, y_entry,
                x1_entry, y1_entry, x2_entry, y2_entry,
                wireframe_points
            )).grid(row=0, column=1, padx=10)


# ---------- Rodar ----------
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
