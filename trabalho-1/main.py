import tkinter as tk
from typing import List, Tuple
from graphicObject import GraphicObject, Point, Segment, Wireframe
from graphicsSystem import GraphicsSystem
from dialog import AddObjectDialog

INITIAL_STEP = 10
INITIAL_DEGREE = 45

# Trabalho 1.1 - Sistema básico com Window e Viewport

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
        
        self.objects: List[GraphicObject] = []
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
        AddObjectDialog(self.root, self.graphics, self.add_new_object)

    def add_new_object(self, obj):
        self.objects.append(obj)
        self.update_objects_list()
        self.update_logs(f"Objeto criado: {obj.name}")


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
