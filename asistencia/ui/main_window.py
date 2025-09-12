import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime, date
from modelos.asistencia import Asistencia
import csv

class MainWindow:
    def __init__(self, root, estudiantes, asistencias, db_manager, generador_reportes):
        self.root = root
        self.estudiantes = estudiantes
        self.asistencias = asistencias
        self.db_manager = db_manager
        self.generador_reportes = generador_reportes
        
        
        self.fecha_var = tk.StringVar(value=date.today().strftime("%Y-%m-%d"))
        self.filtro_fecha_var = tk.StringVar(value=date.today().strftime("%Y-%m-%d"))
        self.filtro_estudiante_var = tk.StringVar()
        self.estado_var = tk.StringVar(value="Presente")

        self.crear_interfaz()
        self.actualizar_lista_estudiantes()
        self.actualizar_combobox_estudiantes()
    
    def crear_interfaz(self):
        self.root.title("Sistema de Registro de Asistencia Estudiantil")
        self.root.geometry("900x600")
        
        
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        
        frame_registro = ttk.Frame(notebook)
        notebook.add(frame_registro, text="Registrar Asistencia")
        
        
        frame_consulta = ttk.Frame(notebook)
        notebook.add(frame_consulta, text="Consultar Asistencia")
        
        
        frame_reportes = ttk.Frame(notebook)
        notebook.add(frame_reportes, text="Reportes")
        
        
        self.crear_pestaña_registro(frame_registro)
        self.crear_pestaña_consulta(frame_consulta)
        self.crear_pestaña_reportes(frame_reportes)
        
        
        self.crear_menu()
    
    def crear_pestaña_registro(self, parent):
        
        frame_fecha = ttk.LabelFrame(parent, text="Fecha")
        frame_fecha.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(frame_fecha, text="Fecha:").grid(row=0, column=0, padx=5, pady=5)
        ttk.Entry(frame_fecha, textvariable=self.fecha_var).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(frame_fecha, text="Hoy", command=self.establecer_fecha_hoy).grid(row=0, column=2, padx=5, pady=5)
        
        
        frame_estudiantes = ttk.LabelFrame(parent, text="Estudiantes")
        frame_estudiantes.pack(fill='both', expand=True, padx=10, pady=5)
        
        
        columns = ('id', 'nombre', 'apellido', 'estado')
        self.tree_estudiantes = ttk.Treeview(frame_estudiantes, columns=columns, show='headings')
        
        self.tree_estudiantes.heading('id', text='ID')
        self.tree_estudiantes.heading('nombre', text='Nombre')
        self.tree_estudiantes.heading('apellido', text='Apellido')
        self.tree_estudiantes.heading('estado', text='Estado')
        
        self.tree_estudiantes.column('id', width=80)
        self.tree_estudiantes.column('nombre', width=150)
        self.tree_estudiantes.column('apellido', width=150)
        self.tree_estudiantes.column('estado', width=100)
        
        
        scrollbar = ttk.Scrollbar(frame_estudiantes, orient=tk.VERTICAL, command=self.tree_estudiantes.yview)
        self.tree_estudiantes.configure(yscrollcommand=scrollbar.set)
        
        self.tree_estudiantes.pack(side=tk.LEFT, fill='both', expand=True)
        scrollbar.pack(side=tk.RIGHT, fill='y')
        
        
        frame_controles = ttk.Frame(parent)
        frame_controles.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(frame_controles, text="Estado:").pack(side=tk.LEFT, padx=5)
        ttk.Combobox(frame_controles, textvariable=self.estado_var, 
                    values=["Presente", "Ausente", "Tarde"], state="readonly").pack(side=tk.LEFT, padx=5)
        
        ttk.Button(frame_controles, text="Aplicar a seleccionados", 
                command=self.aplicar_estado_seleccionados).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(frame_controles, text="Guardar cambios", 
                command=self.guardar_asistencias).pack(side=tk.RIGHT, padx=5)
        
        
        self.tree_estudiantes.bind('<<TreeviewSelect>>', self.on_estudiante_seleccionado)
    
    def crear_pestaña_consulta(self, parent):
        
        frame_filtros = ttk.LabelFrame(parent, text="Filtros de Consulta")
        frame_filtros.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(frame_filtros, text="Fecha:").grid(row=0, column=0, padx=5, pady=5)
        ttk.Entry(frame_filtros, textvariable=self.filtro_fecha_var).grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(frame_filtros, text="Estudiante:").grid(row=0, column=2, padx=5, pady=5)
        self.combo_estudiantes = ttk.Combobox(frame_filtros, textvariable=self.filtro_estudiante_var, state="readonly")
        self.combo_estudiantes.grid(row=0, column=3, padx=5, pady=5)
        
        ttk.Button(frame_filtros, text="Buscar por Fecha", 
                command=self.buscar_por_fecha).grid(row=0, column=4, padx=5, pady=5)
        
        ttk.Button(frame_filtros, text="Buscar por Estudiante", 
                command=self.buscar_por_estudiante).grid(row=0, column=5, padx=5, pady=5)
        
        
        frame_resultados = ttk.Frame(parent)
        frame_resultados.pack(fill='both', expand=True, padx=10, pady=5)
        
        columns = ('fecha', 'id_estudiante', 'nombre', 'apellido', 'estado')
        self.tree_consulta = ttk.Treeview(frame_resultados, columns=columns, show='headings')
        
        self.tree_consulta.heading('fecha', text='Fecha')
        self.tree_consulta.heading('id_estudiante', text='ID')
        self.tree_consulta.heading('nombre', text='Nombre')
        self.tree_consulta.heading('apellido', text='Apellido')
        self.tree_consulta.heading('estado', text='Estado')
        
        self.tree_consulta.column('fecha', width=100)
        self.tree_consulta.column('id_estudiante', width=80)
        self.tree_consulta.column('nombre', width=150)
        self.tree_consulta.column('apellido', width=150)
        self.tree_consulta.column('estado', width=100)
        
        scrollbar = ttk.Scrollbar(frame_resultados, orient=tk.VERTICAL, command=self.tree_consulta.yview)
        self.tree_consulta.configure(yscrollcommand=scrollbar.set)
        
        self.tree_consulta.pack(side=tk.LEFT, fill='both', expand=True)
        scrollbar.pack(side=tk.RIGHT, fill='y')
    
#---------------------- Pestaña Reportes ---------------------#