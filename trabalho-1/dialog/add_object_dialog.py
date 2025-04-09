import tkinter as tk
from tkinter import ttk
from typing import List, Tuple
from graphicObject import Point, Segment, Wireframe 
from graphicsSystem import GraphicsSystem

class AddObjectDialog:
    def __init__(self, master, graphics: GraphicsSystem):
        self.master = master
        self.graphics = graphics

        # Widgets principais
        self.dialog = None
        self.name_entry = None
        self.notebook = None

        # Campos da aba ponto
        self.point_frame = None
        self.x_entry = None
        self.y_entry = None

        # Campos da aba reta
        self.axis_frame = None
        self.x1_entry = None
        self.y1_entry = None
        self.x2_entry = None
        self.y2_entry = None

        # Campos da aba wireframe
        self.wireframe_frame = None
        self.wireframe_points: List[Tuple[float, float]] = []
        self.wf_x_entry = None
        self.wf_y_entry = None
        self.point_list_box = None

        self.build_ui()

    def build_ui(self):
        self.dialog = tk.Toplevel(self.master)
        self.dialog.title("Incluir Objeto")

        # ---------- Campo nome ----------
        tk.Label(self.dialog, text="Nome").pack(anchor="w", padx=10)
        self.name_entry = tk.Entry(self.dialog)
        self.name_entry.pack(fill="x", padx=10, pady=(0, 10))

        # ---------- Notebook ----------
        self.notebook = ttk.Notebook(self.dialog)
        self.notebook.pack(padx=10, pady=10)

        # ---------- Abas ----------
        self.build_point_tab()
        self.build_axis_tab()
        self.build_wireframe_tab()
        # ----------> Aba Curvas

        # ---------- Botões ----------
        button_frame = tk.Frame(self.dialog)
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="Cancelar",
            command=self.on_cancel).grid(row=0, column=0, padx=10)
        
        tk.Button(button_frame, text="OK",
            command=self.on_ok).grid(row=0, column=1, padx=10)
        
        

    def build_point_tab(self):
        self.point_frame = tk.Frame(self.notebook)
        self.notebook.add(self.point_frame, text="Ponto")

        tk.Label(self.point_frame, text="Coordenadas do Ponto").grid(row=0, column=0, columnspan=4, pady=(0, 5))
        
        # x:
        tk.Label(self.point_frame, text="x:").grid(row=1, column=0, sticky="w", padx=(0, 5))

        self.x_entry = tk.Entry(self.point_frame, width=5)
        self.x_entry.grid(row=1, column=1, sticky="w", padx=(0, 15))
        
        # y:
        tk.Label(self.point_frame, text="y:").grid(row=1, column=2, sticky="w", padx=(0, 5))
        self.y_entry = tk.Entry(self.point_frame, width=5)
        self.y_entry.grid(row=1, column=3, sticky="w")

    def build_axis_tab(self):
        self.axis_frame = tk.Frame(self.notebook)
        self.notebook.add(self.axis_frame, text="Reta")

        #Ponto inicial
        tk.Label(self.axis_frame, text="Coordenadas do Ponto Inicial").grid(row=0, column=0, columnspan=4, pady=(0, 5), sticky="w")

        #x1:
        tk.Label(self.axis_frame, text="x1:").grid(row=1, column=0, sticky="w", padx=(0, 5))
        self.x1_entry = tk.Entry(self.axis_frame, width=5)
        self.x1_entry.grid(row=1, column=1, sticky="w", padx=(0, 15))
        # y1:
        tk.Label(self.axis_frame, text="y1:").grid(row=1, column=2, sticky="w", padx=(0, 5))
        self.y1_entry = tk.Entry(self.axis_frame, width=5)
        self.y1_entry.grid(row=1, column=3, sticky="w")


        #Ponto final
        tk.Label(self.axis_frame, text="Coordenadas do Ponto Final").grid(row=2, column=0, columnspan=4, pady=(20, 5), sticky="w")

        #x2:
        tk.Label(self.axis_frame, text="x2:").grid(row=3, column=0, sticky="w", padx=(0, 5))
        self.x2_entry = tk.Entry(self.axis_frame, width=5)
        self.x2_entry.grid(row=3, column=1, sticky="w", padx=(0, 15))
        # y2:
        tk.Label(self.axis_frame, text="y2:").grid(row=3, column=2, sticky="w", padx=(0, 5))
        self.y2_entry = tk.Entry(self.axis_frame, width=5)
        self.y2_entry.grid(row=3, column=3, sticky="w")

    def build_wireframe_tab(self):
        self.wireframe_frame = tk.Frame(self.notebook)
        self.notebook.add(self.wireframe_frame, text="Wireframe")

        #Label 'Novo Ponto'
        tk.Label(self.wireframe_frame, text="Novo ponto:").grid(row=0, column=0, columnspan=4, padx=(2,0), pady=(0, 5), sticky="w")
        # x:
        tk.Label(self.wireframe_frame, text="x:").grid(row=1, column=0, sticky="w", padx=(0, 5))
        self.wf_x_entry = tk.Entry(self.wireframe_frame, width=5)
        self.wf_x_entry.grid(row=1, column=1, sticky="w", padx=(0, 15))
        # y:
        tk.Label(self.wireframe_frame, text="y:").grid(row=1, column=2, sticky="w", padx=(0, 5))
        self.wf_y_entry = tk.Entry(self.wireframe_frame, width=5)
        self.wf_y_entry.grid(row=1, column=3, sticky="w")

        
        #Botão de adicionar
        add_button = tk.Button(self.wireframe_frame, text="Adicionar", command=self.add_wireframe_point)
        add_button.grid(row=3, column=0,columnspan=4, pady=5)

        #Label de Pontos adicionados
        tk.Label(self.wireframe_frame, text="Pontos adicionados:").grid(row=4, column=0, columnspan=4, padx=(2,0), pady=(10,5), sticky="w")

        #Listbox de pontos
        self.point_list_box = tk.Listbox(self.wireframe_frame, height=5, width=30)
        self.point_list_box.grid(row=5, column=0, columnspan=4, sticky="w")

    def add_wireframe_point(self):
        try:
            x = float(self.wf_x_entry.get())
            y = float(self.wf_y_entry.get())

            self.wireframe_points.append((x, y))
            self.point_list_box.insert(tk.END, f"({x}, {y})")

            self.wf_x_entry.delete(0, tk.END)
            self.wf_y_entry.delete(0, tk.END)
        except ValueError:
            print("Coordenadas inválidas")

    def on_cancel(self):
        self.dialog.destroy()

    def on_ok(self):
        print("debug: AddObjectDialog.on_ok() - start")
        try:
            print("debug: entrando no try")
            name = self.name_entry.get().strip() or "Objeto"
            tab_index = self.notebook.index(self.notebook.select())

            if tab_index == 0 and self.x_entry and self.y_entry:
                print(f"debug: entrou na condicional do(a) {name} - tabIndex: {tab_index}, x: {self.x_entry.get()}, y: {self.y_entry.get()}")
                # Aba Ponto
                x = float(self.x_entry.get())
                y = float(self.y_entry.get())
                obj = Point(name, [(x, y)])

            elif tab_index == 1 and all([self.x1_entry, self.y1_entry, self.x2_entry, self.y2_entry]):
                print(f"debug: entrou na condicional do(a) {name} - tabIndex: {tab_index}")
                # Aba Reta
                x1 = float(self.x1_entry.get())
                y1 = float(self.y1_entry.get())
                x2 = float(self.x2_entry.get())
                y2 = float(self.y2_entry.get())
                obj = Segment(name, [(x1, y1), (x2, y2)])

            elif tab_index == 2 and self.wireframe_points is not None:
                print(f"debug: entrou na condicional do(a) {name} - tabIndex: {tab_index}")
                # Aba Wireframe
                if len(self.wireframe_points) < 3:
                    print("Wireframe precisa de pelo menos 3 pontos.")
                    return
                obj = Wireframe(name, self.wireframe_points.copy())

            else:
                print("Tipo de objeto ou parâmetros inválidos.")
                return

            # Adiciona e desenha
            print("debyg: Adiciona e desenha - start")
            self.graphics.display_file.add_object(obj)
            self.graphics.draw()
            self.dialog.destroy()
            print("debyg: Adiciona e desenha - end")

            print("debug: AddObjectDialog.on_ok() - end")

        except ValueError:
            print("Erro: valores inválidos nos campos")
