import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime, date
from modelos.asistencia import Asistencia
from modelos.estudiante import Estudiante
import csv
import os
from tkcalendar import DateEntry
import shutil


class MainWindow:
    def __init__(self, root, estudiantes, asistencias, db_manager, generador_reportes):
        self.root = root
        self.estudiantes = estudiantes
        self.asistencias = asistencias
        self.db_manager = db_manager
        self.generador_reportes = generador_reportes

        # Configuración de colores y estilos
        self.color_primario = "#2c3e50"  # Azul oscuro
        self.color_secundario = "#3498db"  # Azul
        self.color_terciario = "#2980b9"  # Azul más oscuro
        self.color_exito = "#27ae60"  # Verde
        self.color_alerta = "#e74c3c"  # Rojo
        self.color_fondo = "#ecf0f1"  # Gris claro
        self.color_texto = "#2c3e50"  # Azul oscuro

        self.fecha_var = tk.StringVar(value=date.today().strftime("%Y-%m-%d"))
        self.filtro_fecha_var = tk.StringVar(value=date.today().strftime("%Y-%m-%d"))
        self.filtro_estudiante_var = tk.StringVar()
        self.estado_var = tk.StringVar(value="Presente")

        self.configurar_estilos()
        self.crear_interfaz()
        self.actualizar_lista_estudiantes()
        self.actualizar_combobox_estudiantes()

    def configurar_estilos(self):
        """Configura estilos personalizados para los widgets"""
        style = ttk.Style()
        style.theme_use('clam')  # Usar un tema más moderno

        # Configurar estilo para los frames con etiqueta
        style.configure("TLabelframe", background=self.color_fondo, bordercolor=self.color_primario)
        style.configure("TLabelframe.Label", background=self.color_fondo, foreground=self.color_primario,
                        font=('Arial', 10, 'bold'))

        # Configurar estilo para los botones
        style.configure("TButton",
                        background=self.color_secundario,
                        foreground="white",
                        focuscolor=style.configure(".")["background"],
                        font=('Arial', 9),
                        borderwidth=1,
                        relief="raised")
        style.map("TButton",
                  background=[('active', self.color_terciario),
                              ('pressed', self.color_primario)])

        # Configurar estilo para los botones de éxito
        style.configure("Exito.TButton",
                        background=self.color_exito,
                        foreground="white")
        style.map("Exito.TButton",
                  background=[('active', "#219653"),
                              ('pressed', "#1e7e4c")])

        # Configurar estilo para las pestañas
        style.configure("TNotebook", background=self.color_fondo)
        style.configure("TNotebook.Tab",
                        background="#bdc3c7",
                        foreground=self.color_texto,
                        padding=[10, 5],
                        font=('Arial', 9, 'bold'))
        style.map("TNotebook.Tab",
                  background=[('selected', self.color_secundario),
                              ('active', self.color_terciario)],
                  foreground=[('selected', 'white'),
                              ('active', 'white')])

        # Configurar estilo para los treeviews
        style.configure("Treeview",
                        background="white",
                        foreground=self.color_texto,
                        fieldbackground="white",
                        rowheight=25)
        style.configure("Treeview.Heading",
                        background=self.color_primario,
                        foreground="white",
                        font=('Arial', 9, 'bold'),
                        relief="flat")
        style.map("Treeview.Heading",
                  background=[('active', self.color_secundario)])

        # Configurar estilo para las etiquetas
        style.configure("TLabel", background=self.color_fondo, foreground=self.color_texto, font=('Arial', 9))

        # Configurar estilo para los combobox
        style.configure("TCombobox", selectbackground=self.color_secundario)

    def crear_interfaz(self):
        self.root.title("Sistema de Registro de Asistencia Estudiantil")
        self.root.geometry("1000x700")
        self.root.configure(bg=self.color_fondo)

        # Frame principal con saludo
        frame_principal = tk.Frame(self.root, bg=self.color_primario)
        frame_principal.pack(fill='x')

        saludo = tk.Label(frame_principal,
                          text="Sistema de Gestión de Asistencia Estudiantil",
                          font=('Arial', 16, 'bold'),
                          bg=self.color_primario,
                          fg='white',
                          pady=10)
        saludo.pack()

        # Frame para la fecha actual
        frame_fecha_actual = tk.Frame(self.root, bg=self.color_fondo)
        frame_fecha_actual.pack(fill='x', padx=10, pady=5)

        fecha_hoy = date.today().strftime("%d/%m/%Y")
        label_fecha = tk.Label(frame_fecha_actual,text=f"Fecha actual: {fecha_hoy}",font=('Arial', 10, 'italic'),bg=self.color_fondo,fg=self.color_texto)
        label_fecha.pack(side=tk.LEFT)

        self.label_info_estudiantes = tk.Label(frame_fecha_actual,text=f"Estudiantes cargados: {len(self.estudiantes)}",font=('Arial', 10, 'italic'),bg=self.color_fondo,fg=self.color_texto)
        self.label_info_estudiantes.pack(side=tk.RIGHT)

        label_fecha = tk.Label(frame_fecha_actual,
                               text=f"Fecha actual: {fecha_hoy}",
                               font=('Arial', 10, 'italic'),
                               bg=self.color_fondo,
                               fg=self.color_texto)
        label_fecha.pack(side=tk.LEFT)

        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)

        frame_registro = ttk.Frame(notebook)
        notebook.add(frame_registro, text="Registrar Asistencia")

        frame_consulta = ttk.Frame(notebook)
        notebook.add(frame_consulta, text=" Consultar Asistencia")

        frame_reportes = ttk.Frame(notebook)
        notebook.add(frame_reportes, text="Reportes y Estadísticas")

        frame_carga = ttk.Frame(notebook)
        notebook.add(frame_carga, text="Cargar Estudiantes")

        self.crear_pestana_registro(frame_registro)
        self.crear_pestana_consulta(frame_consulta)
        self.crear_pestana_reportes(frame_reportes)
        self.crear_pestana_carga_datos(frame_carga)

        self.crear_menu()

    def crear_pestana_registro(self, parent):
        parent.configure(style="TFrame")

        frame_fecha = ttk.LabelFrame(parent, text="Fecha de Registro")
        frame_fecha.pack(fill='x', padx=10, pady=5)

        ttk.Label(frame_fecha, text="Fecha:").grid(row=0, column=0, padx=5, pady=5)
        
        self.calendario_registro = DateEntry(
            frame_fecha,
            date_pattern='yyyy-mm-dd',
            mindate=date(2024, 1, 1),
            maxdate=date(2029, 12, 31),
            background='gray',
            foreground='white',
            borderwidth=3
        )
        self.calendario_registro.set_date(self.fecha_actual)
        self.calendario_registro.grid(row=0, column=1, padx=5, pady=5)
        
        self.calendario_registro.bind('<<DateEntrySelected>>', self.on_fecha_cambiada_registro)
        notebook.add(frame_registro, text="📝 Registrar Asistencia")

        frame_consulta = ttk.Frame(notebook)
        notebook.add(frame_consulta, text="🔍 Consultar Asistencia")

        frame_reportes = ttk.Frame(notebook)
        notebook.add(frame_reportes, text="📊 Reportes y Estadísticas")

        self.crear_pestaña_registro(frame_registro)
        self.crear_pestaña_consulta(frame_consulta)
        self.crear_pestaña_reportes(frame_reportes)

        self.crear_menu()

    def crear_pestaña_carga_datos(self, parent):
        """Crea la pestaña para cargar archivos CSV con estudiantes"""
        parent.configure(style="TFrame")

        # Frame de información
        frame_info = ttk.LabelFrame(parent, text="ℹ️ Información sobre el Formato CSV")
        frame_info.pack(fill='x', padx=10, pady=5)

        info_text = """
        El archivo CSV debe contener las siguientes columnas:
        • id_estudiante: Identificador único del estudiante
        • nombre: Nombre del estudiante
        • apellido: Apellido del estudiante

        Ejemplo de formato:
        id_estudiante,nombre,apellido
        E001,Juan,Pérez
        E002,María,García
        E003,Carlos,López
        """

        label_info = tk.Label(frame_info,
                              text=info_text,
                              font=('Arial', 9),
                              bg=self.color_fondo,
                              fg=self.color_texto,
                              justify=tk.LEFT)
        label_info.pack(padx=10, pady=10)

        # Frame para selección de archivo
        frame_seleccion = ttk.LabelFrame(parent, text="📁 Seleccionar Archivo CSV")
        frame_seleccion.pack(fill='x', padx=10, pady=5)

        # Controles de selección de archivo
        frame_controles = ttk.Frame(frame_seleccion)
        frame_controles.pack(fill='x', padx=10, pady=10)

        ttk.Button(frame_controles,
                   text="Examinar...",
                   command=self.seleccionar_archivo_csv).pack(side=tk.LEFT, padx=5)

        label_archivo = ttk.Label(frame_controles,
                                  textvariable=self.archivo_csv_var,
                                  font=('Arial', 9, 'italic'),
                                  foreground="#7f8c8d")
        label_archivo.pack(side=tk.LEFT, padx=10, fill='x', expand=True)

        # Frame para vista previa
        frame_vista_previa = ttk.LabelFrame(parent, text="👀 Vista Previa del Archivo")
        frame_vista_previa.pack(fill='both', expand=True, padx=10, pady=5)

        # Treeview para vista previa
        columns = ('id_estudiante', 'nombre', 'apellido')
        self.tree_vista_previa = ttk.Treeview(frame_vista_previa, columns=columns, show='headings', height=8)

        self.tree_vista_previa.heading('id_estudiante', text='ID Estudiante')
        self.tree_vista_previa.heading('nombre', text='Nombre')
        self.tree_vista_previa.heading('apellido', text='Apellido')

        self.tree_vista_previa.column('id_estudiante', width=120, anchor='center')
        self.tree_vista_previa.column('nombre', width=150, anchor='center')
        self.tree_vista_previa.column('apellido', width=150, anchor='center')

        scrollbar = ttk.Scrollbar(frame_vista_previa, orient=tk.VERTICAL, command=self.tree_vista_previa.yview)
        self.tree_vista_previa.configure(yscrollcommand=scrollbar.set)

        self.tree_vista_previa.pack(side=tk.LEFT, fill='both', expand=True, padx=5, pady=5)
        scrollbar.pack(side=tk.RIGHT, fill='y', pady=5)

        # Frame para botones de acción
        frame_acciones = ttk.Frame(parent)
        frame_acciones.pack(fill='x', padx=10, pady=10)

        ttk.Button(frame_acciones,
                   text="🔄 Cargar Estudiantes a la Base de Datos",
                   command=self.cargar_estudiantes_desde_csv,
                   style="Exito.TButton").pack(side=tk.RIGHT, padx=5)

        ttk.Button(frame_acciones,
                   text="📋 Generar Plantilla CSV",
                   command=self.generar_plantilla_csv).pack(side=tk.LEFT, padx=5)

    def seleccionar_archivo_csv(self):
        """Permite al usuario seleccionar un archivo CSV"""
        archivo = filedialog.askopenfilename(
            title="Seleccionar archivo CSV de estudiantes",
            filetypes=[
                ("Archivos CSV", "*.csv"),
                ("Todos los archivos", "*.*")
            ]
        )

        if archivo:
            self.archivo_csv_var.set(archivo)
            self.mostrar_vista_previa_csv(archivo)

    def mostrar_vista_previa_csv(self, archivo):
        """Muestra una vista previa del archivo CSV seleccionado"""
        # Limpiar vista previa anterior
        for item in self.tree_vista_previa.get_children():
            self.tree_vista_previa.delete(item)

        try:
            with open(archivo, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)

                # Verificar que el archivo tenga las columnas necesarias
                columnas_requeridas = ['id_estudiante', 'nombre', 'apellido']
                if not all(col in reader.fieldnames for col in columnas_requeridas):
                    messagebox.showerror(
                        "Error de formato",
                        f"El archivo CSV debe contener las columnas: {', '.join(columnas_requeridas)}"
                    )
                    return

                # Mostrar las primeras 10 filas como vista previa
                contador = 0
                for fila in reader:
                    if contador >= 10:  # Limitar a 10 filas para la vista previa
                        break

                    self.tree_vista_previa.insert('', 'end', values=(
                        fila['id_estudiante'],
                        fila['nombre'],
                        fila['apellido']
                    ))
                    contador += 1

                if contador == 0:
                    messagebox.showwarning("Archivo vacío", "El archivo CSV seleccionado está vacío")

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo leer el archivo CSV: {str(e)}")

    def cargar_estudiantes_desde_csv(self):
        """Carga los estudiantes desde el archivo CSV a la base de datos"""
        archivo = self.archivo_csv_var.get()

        if not archivo or archivo == "No se ha seleccionado archivo":
            messagebox.showwarning("Advertencia", "Por favor seleccione un archivo CSV primero")
            return

        try:
            # Leer el archivo CSV
            nuevos_estudiantes = []
            with open(archivo, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)

                for num_fila, row in enumerate(reader, start=2):  # start=2 porque la fila 1 es el encabezado
                    try:
                        # Validar campos requeridos
                        if not all([row.get('id_estudiante'), row.get('nombre'), row.get('apellido')]):
                            messagebox.showwarning(
                                "Advertencia",
                                f"Fila {num_fila}: Campos incompletos, se omitirá"
                            )
                            continue

                        from modelos.estudiante import Estudiante
                        estudiante = Estudiante(
                            row['id_estudiante'].strip(),
                            row['nombre'].strip(),
                            row['apellido'].strip()
                        )
                        nuevos_estudiantes.append(estudiante)

                    except Exception as e:
                        messagebox.showwarning(
                            "Advertencia",
                            f"Error en fila {num_fila}: {str(e)}"
                        )
                        continue

            if not nuevos_estudiantes:
                messagebox.showwarning("Advertencia", "No se encontraron estudiantes válidos en el archivo")
                return

            # Confirmar con el usuario
            confirmacion = messagebox.askyesno(
                "Confirmar carga",
                f"¿Está seguro de que desea cargar {len(nuevos_estudiantes)} estudiantes a la base de datos?\n\n"
                "Esta acción reemplazará la lista actual de estudiantes."
            )

            if not confirmacion:
                return

            # Limpiar estudiantes existentes y cargar nuevos
            self.db_manager.limpiar_estudiantes()  # Necesitarás implementar este método

            for est in nuevos_estudiantes:
                resultado, mensaje = self.db_manager.insertar_estudiante(est)
                if not resultado:
                    messagebox.showerror("Error", f"No se pudo insertar estudiante {est.nombre}: {mensaje}")
                    return

            # Actualizar la lista de estudiantes en memoria
            self.estudiantes, _ = self.db_manager.obtener_estudiantes()
            self.generador_reportes.estudiantes = self.estudiantes

            # Actualizar la interfaz
            self.actualizar_lista_estudiantes()
            self.actualizar_combobox_estudiantes()
            self.actualizar_contador_estudiantes()

            messagebox.showinfo(
                "Éxito",
                f"✅ Se cargaron {len(nuevos_estudiantes)} estudiantes correctamente\n"
                f"Total de estudiantes en el sistema: {len(self.estudiantes)}"
            )

            # Limpiar la selección después de cargar
            self.archivo_csv_var.set("No se ha seleccionado archivo")
            for item in self.tree_vista_previa.get_children():
                self.tree_vista_previa.delete(item)

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar el archivo: {str(e)}")

    def generar_plantilla_csv(self):
        """Genera un archivo CSV de plantilla para que el usuario lo llene"""
        archivo = filedialog.asksaveasfilename(
            title="Guardar plantilla CSV",
            defaultextension=".csv",
            filetypes=[("Archivos CSV", "*.csv")]
        )

        if archivo:
            try:
                with open(archivo, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    # Escribir encabezados
                    writer.writerow(['id_estudiante', 'nombre', 'apellido'])
                    # Escribir algunos ejemplos
                    writer.writerow(['E001', 'Juan', 'Pérez'])
                    writer.writerow(['E002', 'María', 'García'])
                    writer.writerow(['E003', 'Carlos', 'López'])
                    writer.writerow(['# Complete con los datos de sus estudiantes...', '', ''])

                messagebox.showinfo(
                    "Plantilla generada",
                    f"✅ Plantilla CSV generada correctamente en:\n{archivo}\n\n"
                    "Por favor complete con los datos de sus estudiantes."
                )
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo generar la plantilla: {str(e)}")

    def actualizar_contador_estudiantes(self):
        """Actualiza el contador de estudiantes en la interfaz"""
        self.label_info_estudiantes.config(text=f"👥 Estudiantes cargados: {len(self.estudiantes)}")

    # Los métodos restantes se mantienen igual, solo agregando la actualización del contador
    # donde sea necesario...

    def actualizar_lista_estudiantes(self):
        for item in self.tree_estudiantes.get_children():
            self.tree_estudiantes.delete(item)

        fecha_actual = self.fecha_var.get()
        asistencias_fecha, _ = self.db_manager.obtener_asistencias_por_fecha(fecha_actual)

        asistencias_dict = {a.id_estudiante: a.estado for a in asistencias_fecha}

        for est in self.estudiantes:
            estado = asistencias_dict.get(est.id_estudiante, "No registrado")
            self.tree_estudiantes.insert('', 'end', values=(
                est.id_estudiante, est.nombre, est.apellido, estado
            ))

        self.actualizar_contador_estudiantes()

    def actualizar_combobox_estudiantes(self):
        opciones_estudiantes = [f"{est.id_estudiante} - {est.nombre} {est.apellido}"
                                for est in self.estudiantes]
        self.combo_estudiantes['values'] = opciones_estudiantes
        if opciones_estudiantes:
            self.filtro_estudiante_var.set(opciones_estudiantes[0])

    def crear_pestaña_registro(self, parent):
        parent.configure(style="TFrame")

        frame_fecha = ttk.LabelFrame(parent, text="📅 Fecha de Registro")
        frame_fecha.pack(fill='x', padx=10, pady=5)

        ttk.Label(frame_fecha, text="Fecha:").grid(row=0, column=0, padx=5, pady=5)
        entry_fecha = ttk.Entry(frame_fecha, textvariable=self.fecha_var, width=12)
        entry_fecha.grid(row=0, column=1, padx=5, pady=5)

        btn_hoy = ttk.Button(frame_fecha, text="Hoy", command=self.establecer_fecha_hoy, width=8)
        btn_hoy.grid(row=0, column=2, padx=5, pady=5)

        frame_estudiantes = ttk.LabelFrame(parent, text="Lista de Estudiantes")
        frame_estudiantes = ttk.LabelFrame(parent, text="👥 Lista de Estudiantes")
        frame_estudiantes.pack(fill='both', expand=True, padx=10, pady=5)

        columns = ('id', 'nombre', 'apellido', 'estado')
        self.tree_estudiantes = ttk.Treeview(frame_estudiantes, columns=columns, show='headings', height=15)

        self.tree_estudiantes.heading('id', text='ID')
        self.tree_estudiantes.heading('nombre', text='Nombre')
        self.tree_estudiantes.heading('apellido', text='Apellido')
        self.tree_estudiantes.heading('estado', text='Estado')

        self.tree_estudiantes.column('id', width=80, anchor='center')
        self.tree_estudiantes.column('nombre', width=150)
        self.tree_estudiantes.column('apellido', width=150)
        self.tree_estudiantes.column('estado', width=100, anchor='center')

        scrollbar = ttk.Scrollbar(frame_estudiantes, orient=tk.VERTICAL, command=self.tree_estudiantes.yview)
        self.tree_estudiantes.configure(yscrollcommand=scrollbar.set)

        self.tree_estudiantes.pack(side=tk.LEFT, fill='both', expand=True, padx=5, pady=5)
        scrollbar.pack(side=tk.RIGHT, fill='y', pady=5)

        frame_controles = ttk.Frame(parent)
        frame_controles.pack(fill='x', padx=10, pady=10)

        ttk.Label(frame_controles, text="Estado:").pack(side=tk.LEFT, padx=5)
        combo_estado = ttk.Combobox(frame_controles, textvariable=self.estado_var,values=["Presente", "Ausente", "Tarde"],state="readonly", width=12)
        combo_estado.pack(side=tk.LEFT, padx=5)

        btn_aplicar = ttk.Button(frame_controles, text="Aplicar a Seleccionados",command=self.aplicar_estado_seleccionados)
        btn_aplicar.pack(side=tk.LEFT, padx=10)

        btn_eliminar = ttk.Button(frame_controles, text="Eliminar Seleccionados",command=self.eliminar_estudiantes_seleccionados,style="Peligro.TButton")
        btn_eliminar.pack(side=tk.LEFT, padx=10)

        btn_guardar = ttk.Button(frame_controles, text="Guardar Cambios",command=self.guardar_asistencias, style="Exito.TButton")
        combo_estado = ttk.Combobox(frame_controles, textvariable=self.estado_var,
                                    values=["Presente", "Ausente", "Tarde"],
                                    state="readonly", width=12)
        combo_estado.pack(side=tk.LEFT, padx=5)

        btn_aplicar = ttk.Button(frame_controles, text="Aplicar a Seleccionados",
                                 command=self.aplicar_estado_seleccionados)
        btn_aplicar.pack(side=tk.LEFT, padx=10)

        btn_guardar = ttk.Button(frame_controles, text="💾 Guardar Cambios",
                                 command=self.guardar_asistencias, style="Exito.TButton")
        btn_guardar.pack(side=tk.RIGHT, padx=5)

        self.tree_estudiantes.bind('<<TreeviewSelect>>', self.on_estudiante_seleccionado)

    def crear_pestana_consulta(self, parent):
        parent.configure(style="TFrame")

        frame_filtros = ttk.LabelFrame(parent, text="Filtros de Consulta")
        frame_filtros.pack(fill='x', padx=10, pady=5)

        ttk.Label(frame_filtros, text="Fecha:").grid(row=0, column=0, padx=5, pady=5)
        
        self.calendario_consulta = DateEntry(
            frame_filtros,
            date_pattern='yyyy-mm-dd',
            mindate=date(2020, 1, 1),
            maxdate=date(2030, 12, 31),
            background='gray',
            foreground='white',
            borderwidth=3
        )
        self.calendario_consulta.set_date(self.filtro_fecha_actual)
        self.calendario_consulta.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame_filtros, text="Estudiante:").grid(row=0, column=2, padx=5, pady=5)
        self.combo_estudiantes = ttk.Combobox(frame_filtros, textvariable=self.filtro_estudiante_var,state="readonly", width=25)
        self.combo_estudiantes.grid(row=0, column=3, padx=5, pady=5)

        btn_fecha = ttk.Button(frame_filtros, text="Buscar por Fecha",command=self.buscar_por_fecha)
        btn_fecha.grid(row=0, column=4, padx=5, pady=5)

        btn_estudiante = ttk.Button(frame_filtros, text="Buscar por Estudiante",command=self.buscar_por_estudiante)
    def crear_pestaña_consulta(self, parent):
        parent.configure(style="TFrame")

        frame_filtros = ttk.LabelFrame(parent, text="🔍 Filtros de Consulta")
        frame_filtros.pack(fill='x', padx=10, pady=5)

        ttk.Label(frame_filtros, text="Fecha:").grid(row=0, column=0, padx=5, pady=5)
        entry_filtro_fecha = ttk.Entry(frame_filtros, textvariable=self.filtro_fecha_var, width=12)
        entry_filtro_fecha.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame_filtros, text="Estudiante:").grid(row=0, column=2, padx=5, pady=5)
        self.combo_estudiantes = ttk.Combobox(frame_filtros, textvariable=self.filtro_estudiante_var,
                                              state="readonly", width=25)
        self.combo_estudiantes.grid(row=0, column=3, padx=5, pady=5)

        btn_fecha = ttk.Button(frame_filtros, text="Buscar por Fecha",
                               command=self.buscar_por_fecha)
        btn_fecha.grid(row=0, column=4, padx=5, pady=5)

        btn_estudiante = ttk.Button(frame_filtros, text="Buscar por Estudiante",
                                    command=self.buscar_por_estudiante)
        btn_estudiante.grid(row=0, column=5, padx=5, pady=5)

        frame_resultados = ttk.Frame(parent)
        frame_resultados.pack(fill='both', expand=True, padx=10, pady=5)

        columns = ('fecha', 'id_estudiante', 'nombre', 'apellido', 'estado')
        self.tree_consulta = ttk.Treeview(frame_resultados, columns=columns, show='headings', height=15)

        self.tree_consulta.heading('fecha', text='Fecha')
        self.tree_consulta.heading('id_estudiante', text='ID')
        self.tree_consulta.heading('nombre', text='Nombre')
        self.tree_consulta.heading('apellido', text='Apellido')
        self.tree_consulta.heading('estado', text='Estado')

        self.tree_consulta.column('fecha', width=100, anchor='center')
        self.tree_consulta.column('id_estudiante', width=80, anchor='center')
        self.tree_consulta.column('nombre', width=150)
        self.tree_consulta.column('apellido', width=150)
        self.tree_consulta.column('estado', width=100, anchor='center')

        scrollbar = ttk.Scrollbar(frame_resultados, orient=tk.VERTICAL, command=self.tree_consulta.yview)
        self.tree_consulta.configure(yscrollcommand=scrollbar.set)

        self.tree_consulta.pack(side=tk.LEFT, fill='both', expand=True, padx=5, pady=5)
        scrollbar.pack(side=tk.RIGHT, fill='y', pady=5)

    def crear_pestana_reportes(self, parent):
        parent.configure(style="TFrame")

        frame_controles = ttk.LabelFrame(parent, text="Acciones de Reportes")
        frame_controles.pack(fill='x', padx=10, pady=5)

        btn_reporte = ttk.Button(frame_controles, text="Generar Reporte de Asistencia",command=self.generar_reporte_asistencia)
        btn_reporte.pack(side=tk.LEFT, padx=5, pady=5)

        btn_alertas = ttk.Button(frame_controles, text="Ver Alertas de Baja Asistencia",command=self.mostrar_alertas)
        btn_alertas.pack(side=tk.LEFT, padx=5, pady=5)

        btn_exportar_csv = ttk.Button(frame_controles, text="Exportar a CSV",command=self.exportar_reporte_csv, style="Exito.TButton")
        btn_exportar_csv.pack(side=tk.RIGHT, padx=5, pady=5)

        btn_exportar_pdf = ttk.Button(frame_controles, text="Exportar a PDF",command=self.exportar_reporte_pdf, style="Exito.TButton")
        btn_exportar_pdf.pack(side=tk.RIGHT, padx=5, pady=5)
    def crear_pestaña_reportes(self, parent):
        parent.configure(style="TFrame")

        frame_controles = ttk.LabelFrame(parent, text="📈 Acciones de Reportes")
        frame_controles.pack(fill='x', padx=10, pady=5)

        btn_reporte = ttk.Button(frame_controles, text="Generar Reporte de Asistencia",
                                 command=self.generar_reporte_asistencia)
        btn_reporte.pack(side=tk.LEFT, padx=5, pady=5)

        btn_alertas = ttk.Button(frame_controles, text="Ver Alertas de Baja Asistencia",
                                 command=self.mostrar_alertas)
        btn_alertas.pack(side=tk.LEFT, padx=5, pady=5)

        btn_exportar = ttk.Button(frame_controles, text="📤 Exportar a CSV",
                                  command=self.exportar_reporte_csv, style="Exito.TButton")
        btn_exportar.pack(side=tk.RIGHT, padx=5, pady=5)

        frame_reportes = ttk.Frame(parent)
        frame_reportes.pack(fill='both', expand=True, padx=10, pady=5)

        columns = ('id_estudiante', 'nombre', 'apellido', 'porcentaje', 'estado')
        self.tree_reportes = ttk.Treeview(frame_reportes, columns=columns, show='headings', height=15)

        self.tree_reportes.heading('id_estudiante', text='ID')
        self.tree_reportes.heading('nombre', text='Nombre')
        self.tree_reportes.heading('apellido', text='Apellido')
        self.tree_reportes.heading('porcentaje', text='Porcentaje (%)')
        self.tree_reportes.heading('estado', text='Estado')

        self.tree_reportes.column('id_estudiante', width=80, anchor='center')
        self.tree_reportes.column('nombre', width=150)
        self.tree_reportes.column('apellido', width=150)
        self.tree_reportes.column('porcentaje', width=100, anchor='center')
        self.tree_reportes.column('estado', width=100, anchor='center')

        scrollbar = ttk.Scrollbar(frame_reportes, orient=tk.VERTICAL, command=self.tree_reportes.yview)
        self.tree_reportes.configure(yscrollcommand=scrollbar.set)

        self.tree_reportes.pack(side=tk.LEFT, fill='both', expand=True, padx=5, pady=5)
        scrollbar.pack(side=tk.RIGHT, fill='y', pady=5)

    def crear_pestana_carga_datos(self, parent):
        parent.configure(style="TFrame")

        frame_info = ttk.LabelFrame(parent, text="Información sobre el Formato CSV")
        frame_info.pack(fill='both', expand=True, padx=10, pady=10)

        info_text = """
    El archivo CSV debe contener las siguientes columnas:
    • id_estudiante: Identificador único del estudiante (NUMÉRICO, obligatorio)
    • nombre: Nombre del estudiante (TEXTO sin números, obligatorio)
    • apellido: Apellido del estudiante (TEXTO sin números, obligatorio)

    Ejemplo de formato:
    id_estudiante,nombre,apellido
    001,Juan,Pérez
    002,María,García
    003,Carlos,López

    Nota: Para cargar estudiantes, utilice la opción de carga de archivos 
    desde el menú principal del sistema (Archivo → Cargar Estudiantes CSV).
    """

        label_info = tk.Label(frame_info, text=info_text, font=('Arial', 10), bg=self.color_fondo,fg=self.color_texto,justify=tk.LEFT)
        label_info.pack(padx=20, pady=20)

    def crear_menu(self):
        menubar = tk.Menu(self.root, bg=self.color_fondo, fg=self.color_texto, activebackground=self.color_secundario)
        self.root.config(menu=menubar)

        menu_archivo = tk.Menu(menubar, tearoff=0, bg=self.color_fondo, fg=self.color_texto,activebackground=self.color_secundario, activeforeground="white")
        menubar.add_cascade(label="Archivo", menu=menu_archivo)
        menu_archivo.add_command(label="Agregar Estudiante", command=self.mostrar_dialogo_agregar_estudiante)
        menu_archivo.add_command(label="Eliminar Estudiante", command=self.mostrar_dialogo_eliminar_estudiante)
        menu_archivo.add_command(label="Cargar Estudiantes CSV", command=self.cargar_estudiantes_dialogo)

        menu_archivo.add_command(label="Cargar Base de Datos CSV",command=self.cargar_base_datos_completa)
        
        menu_archivo.add_command(label="Exportar Reporte CSV", command=self.exportar_reporte_csv)
        menu_archivo.add_command(label="Exportar Reporte PDF", command=self.exportar_reporte_pdf)
        menu_archivo.add_separator()
        menu_archivo.add_command(label="Salir", command=self.on_salir)

        menu_db = tk.Menu(menubar, tearoff=0, bg=self.color_fondo, fg=self.color_texto,activebackground=self.color_secundario, activeforeground="white")
        menubar.add_cascade(label="Base de Datos", menu=menu_db)
        menu_db.add_command(label="Respaldar BD", command=self.respaldar_base_datos)
        menu_db.add_command(label="Estadísticas BD", command=self.mostrar_estadisticas)

    def es_texto_valido(self, texto):
        if not texto or texto.strip() == "":
            return False, "El campo no puede estar vacío"

        if any(caracter.isdigit() for caracter in texto):
            return False, "No puede contener números"
        
        return True, ""

    def es_id_valido(self, id_estudiante):
        if not id_estudiante or id_estudiante.strip() == "":
            return False, "El ID no puede estar vacío"

        if not id_estudiante.strip().isdigit():
            return False, "El ID debe ser un número"
        
        return True, ""

    def cargar_base_datos_completa(self):
        try:
            confirmacion = messagebox.askyesno(
                "Cargar Nueva Base de Datos",
                "Esta acción eliminará TODOS los datos actuales y cargará una nueva base de datos.\n\n"
                "¿Está seguro de que desea continuar?",
                icon='warning'
            )
            
            if not confirmacion:
                return

            archivo_estudiantes = filedialog.askopenfilename(
                title="Seleccionar archivo CSV de estudiantes",
                filetypes=[("Archivos CSV", "*.csv"), ("Todos los archivos", "*.*")]
            )
            
            if not archivo_estudiantes:
                return

            cargar_asistencias = messagebox.askyesno(
                "Cargar Asistencias",
                "¿Desea también cargar un archivo de asistencias?\n\n"
                "Si selecciona 'No', solo se cargarán los estudiantes."
            )

            archivo_asistencias = None
            if cargar_asistencias:
                archivo_asistencias = filedialog.askopenfilename(
                    title="Seleccionar archivo CSV de asistencias",filetypes=[("Archivos CSV", "*.csv"), ("Todos los archivos", "*.*")]
                )
                
                if not archivo_asistencias:
                    cargar_asistencias = False

            resultado, mensaje = self.db_manager.limpiar_estudiantes()
            if not resultado:
                messagebox.showerror("Error", f"No se pudo limpiar la base de datos: {mensaje}")
                return

            estudiantes_cargados = 0
            estudiantes_omitidos = 0
            errores_estudiantes = []
            
            try:
                with open(archivo_estudiantes, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    
                    for num_fila, row in enumerate(reader, start=2): 
                        try:
                            id_estudiante = row.get('id_estudiante', '').strip()
                            nombre = row.get('nombre', '').strip()
                            apellido = row.get('apellido', '').strip()

                            id_valido, mensaje_id = self.es_id_valido(id_estudiante)
                            if not id_valido:
                                errores_estudiantes.append(f"Fila {num_fila}: ID '{id_estudiante}' - {mensaje_id}")
                                estudiantes_omitidos += 1
                                continue

                            nombre_valido, mensaje_nombre = self.es_texto_valido(nombre)
                            if not nombre_valido:
                                errores_estudiantes.append(f"Fila {num_fila}: Nombre '{nombre}' - {mensaje_nombre}")
                                estudiantes_omitidos += 1
                                continue

                            apellido_valido, mensaje_apellido = self.es_texto_valido(apellido)
                            if not apellido_valido:
                                errores_estudiantes.append(f"Fila {num_fila}: Apellido '{apellido}' - {mensaje_apellido}")
                                estudiantes_omitidos += 1
                                continue

                            estudiante = Estudiante(id_estudiante, nombre, apellido)
                            
                            resultado, mensaje = self.db_manager.insertar_estudiante(estudiante)
                            if resultado:
                                estudiantes_cargados += 1
                            else:
                                errores_estudiantes.append(f"Fila {num_fila}: {mensaje}")
                                estudiantes_omitidos += 1
                                
                        except Exception as e:
                            errores_estudiantes.append(f"Fila {num_fila}: Error inesperado - {str(e)}")
                            estudiantes_omitidos += 1
                            continue
                            
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo leer el archivo de estudiantes: {str(e)}")
                return

            asistencias_cargadas = 0
            asistencias_omitidas = 0
            errores_asistencias = []
            
            if cargar_asistencias and archivo_asistencias:
                try:
                    with open(archivo_asistencias, 'r', encoding='utf-8') as f:
                        reader = csv.DictReader(f)
                        
                        for num_fila, row in enumerate(reader, start=2):
                            try:
                                if not all([row.get('id_estudiante'), row.get('fecha'), row.get('estado')]):
                                    asistencias_omitidas += 1
                                    continue
                                
                                asistencia = Asistencia(
                                    row['id_estudiante'].strip(),
                                    row['fecha'].strip(),
                                    row['estado'].strip()
                                )
                                
                                resultado, mensaje = self.db_manager.insertar_asistencia(asistencia)
                                if resultado:
                                    asistencias_cargadas += 1
                                else:
                                    errores_asistencias.append(f"Fila {num_fila}: {mensaje}")
                                    asistencias_omitidas += 1
                                    
                            except Exception as e:
                                errores_asistencias.append(f"Fila {num_fila}: Error inesperado - {str(e)}")
                                asistencias_omitidas += 1
                                continue
                                
                except Exception as e:
                    messagebox.showwarning(
                        "Advertencia", 
                        f"Se cargaron los estudiantes pero hubo un error con las asistencias: {str(e)}"
                    )

            self.estudiantes, _ = self.db_manager.obtener_estudiantes()
            self.asistencias, _ = self.db_manager.obtener_asistencias()
            self.generador_reportes.estudiantes = self.estudiantes

            self.actualizar_lista_estudiantes()
            self.actualizar_combobox_estudiantes()
            self.actualizar_contador_estudiantes()

            mensaje_resumen = f" Base de datos cargada correctamente:\n\n"
            mensaje_resumen += f" Estudiantes cargados: {estudiantes_cargados}\n"
            mensaje_resumen += f" Estudiantes omitidos: {estudiantes_omitidos}\n"
            
            if cargar_asistencias:
                mensaje_resumen += f"\n Asistencias cargadas: {asistencias_cargadas}\n"
                mensaje_resumen += f" Asistencias omitidas: {asistencias_omitidas}\n"
            else:
                mensaje_resumen += f"\n Asistencias: No se cargaron\n"
            
            mensaje_resumen += f"\n Archivo de estudiantes: {os.path.basename(archivo_estudiantes)}"
            
            if cargar_asistencias:
                mensaje_resumen += f"\n Archivo de asistencias: {os.path.basename(archivo_asistencias)}"

            if errores_estudiantes:
                mensaje_resumen += f"\n\n Errores en estudiantes (primeros 5):\n"
                for error in errores_estudiantes[:5]:
                    mensaje_resumen += f"• {error}\n"
                if len(errores_estudiantes) > 5:
                    mensaje_resumen += f"• ... y {len(errores_estudiantes) - 5} errores más\n"
            
            if errores_asistencias:
                mensaje_resumen += f"\n Errores en asistencias (primeros 5):\n"
                for error in errores_asistencias[:5]:
                    mensaje_resumen += f"• {error}\n"
                if len(errores_asistencias) > 5:
                    mensaje_resumen += f"• ... y {len(errores_asistencias) - 5} errores más\n"

            messagebox.showinfo("Carga Completada", mensaje_resumen)

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar la base de datos: {str(e)}")

    def cargar_estudiantes_dialogo(self):
        archivo = filedialog.askopenfilename(
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )

        if archivo:
            try:
                nuevos_estudiantes = []
                estudiantes_omitidos = 0
                errores = []
                
                with open(archivo, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for num_fila, row in enumerate(reader, start=2):
                        try:
                            id_estudiante = row['id_estudiante'].strip()
                            nombre = row['nombre'].strip()
                            apellido = row['apellido'].strip()

                            id_valido, mensaje_id = self.es_id_valido(id_estudiante)
                            if not id_valido:
                                errores.append(f"Fila {num_fila}: {mensaje_id}")
                                estudiantes_omitidos += 1
                                continue

                            nombre_valido, mensaje_nombre = self.es_texto_valido(nombre)
                            if not nombre_valido:
                                errores.append(f"Fila {num_fila}: {mensaje_nombre}")
                                estudiantes_omitidos += 1
                                continue

                            apellido_valido, mensaje_apellido = self.es_texto_valido(apellido)
                            if not apellido_valido:
                                errores.append(f"Fila {num_fila}: {mensaje_apellido}")
                                estudiantes_omitidos += 1
                                continue

                            estudiante = Estudiante(id_estudiante, nombre, apellido)
                            nuevos_estudiantes.append(estudiante)
                            
                        except Exception as e:
                            errores.append(f"Fila {num_fila}: Error inesperado - {str(e)}")
                            estudiantes_omitidos += 1
                            continue

                for est in nuevos_estudiantes:
                    self.db_manager.insertar_estudiante(est)

                self.estudiantes, _ = self.db_manager.obtener_estudiantes()
                self.generador_reportes.estudiantes = self.estudiantes
                self.actualizar_lista_estudiantes()
                self.actualizar_combobox_estudiantes()
                self.actualizar_contador_estudiantes()

                mensaje = f"{len(nuevos_estudiantes)} estudiantes cargados correctamente"
                if estudiantes_omitidos > 0:
                    mensaje += f"\n{estudiantes_omitidos} estudiantes omitidos por errores"
                    if errores:
                        mensaje += f"\n\nErrores (primeros 5):\n"
                        for error in errores[:5]:
                            mensaje += f"• {error}\n"
                        if len(errores) > 5:
                            mensaje += f"• ... y {len(errores) - 5} errores más"

                messagebox.showinfo("Carga Completada", mensaje)
                
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo cargar el archivo: {str(e)}")

    def mostrar_dialogo_agregar_estudiante(self):
        dialogo = tk.Toplevel(self.root)
        dialogo.title("Agregar Estudiante")
        dialogo.geometry("400x250")
        dialogo.configure(bg=self.color_fondo)
        dialogo.resizable(False, False)

        dialogo.transient(self.root)
        dialogo.grab_set()

        frame_principal = ttk.Frame(dialogo, style="TFrame")
        frame_principal.pack(fill='both', expand=True, padx=20, pady=20)

        ttk.Label(frame_principal,text="Ingrese los datos del estudiante",font=('Arial', 12, 'bold')).pack(pady=(0, 15))

        frame_campos = ttk.Frame(frame_principal)
        frame_campos.pack(fill='x', pady=10)

        ttk.Label(frame_campos, text="ID Estudiante:").grid(row=0, column=0, sticky='w', padx=5, pady=8)
        entry_id = ttk.Entry(frame_campos, width=30, font=('Arial', 10))
        entry_id.grid(row=0, column=1, padx=5, pady=8, sticky='ew')
        entry_id.focus_set()

        ttk.Label(frame_campos, text="Nombre:").grid(row=1, column=0, sticky='w', padx=5, pady=8)
        entry_nombre = ttk.Entry(frame_campos, width=30, font=('Arial', 10))
        entry_nombre.grid(row=1, column=1, padx=5, pady=8, sticky='ew')

        ttk.Label(frame_campos, text="Apellido:").grid(row=2, column=0, sticky='w', padx=5, pady=8)
        entry_apellido = ttk.Entry(frame_campos, width=30, font=('Arial', 10))
        entry_apellido.grid(row=2, column=1, padx=5, pady=8, sticky='ew')

        frame_campos.columnconfigure(1, weight=1)

        frame_botones = ttk.Frame(frame_principal)
        frame_botones.pack(fill='x', pady=(20, 0))

        def guardar_estudiante():
            id_estudiante = entry_id.get().strip()
            nombre = entry_nombre.get().strip()
            apellido = entry_apellido.get().strip()

            if not id_estudiante:
                messagebox.showerror("Error", "El ID del estudiante es obligatorio", parent=dialogo)
                return

            if not id_estudiante.isdigit():
                messagebox.showerror("Error", "El ID debe ser un número", parent=dialogo)
                return

            if not nombre:
                messagebox.showerror("Error", "El nombre es obligatorio", parent=dialogo)
                return

            if any(caracter.isdigit() for caracter in nombre):
                messagebox.showerror("Error", "El nombre no puede contener números", parent=dialogo)
                return

            if not apellido:
                messagebox.showerror("Error", "El apellido es obligatorio", parent=dialogo)
                return

            if any(caracter.isdigit() for caracter in apellido):
                messagebox.showerror("Error", "El apellido no puede contener números", parent=dialogo)
                return

            if any(est.id_estudiante == id_estudiante for est in self.estudiantes):
                messagebox.showerror("Error", f"Ya existe un estudiante con el ID: {id_estudiante}",parent=dialogo)
                return

            try:
                estudiante = Estudiante(id_estudiante, nombre, apellido)
                resultado, mensaje = self.db_manager.insertar_estudiante(estudiante)

                if resultado:
                    self.estudiantes, _ = self.db_manager.obtener_estudiantes()
                    self.generador_reportes.estudiantes = self.estudiantes

                    self.actualizar_lista_estudiantes()
                    self.actualizar_combobox_estudiantes()
                    self.actualizar_contador_estudiantes()

                    messagebox.showinfo("Éxito",f"Estudiante agregado correctamente:\n"f"ID: {id_estudiante}\n"f"Nombre: {nombre} {apellido}",parent=dialogo)
                    dialogo.destroy()
                else:
                    messagebox.showerror("Error",f"No se pudo guardar el estudiante: {mensaje}", parent=dialogo)

            except Exception as e:
                messagebox.showerror("Error",f"Error al guardar el estudiante: {str(e)}",parent=dialogo)

        def limpiar_campos():
            entry_id.delete(0, tk.END)
            entry_nombre.delete(0, tk.END)
            entry_apellido.delete(0, tk.END)
            entry_id.focus_set()

        ttk.Button(frame_botones,text="Guardar",command=guardar_estudiante,style="Exito.TButton").pack(side=tk.RIGHT, padx=5)
        ttk.Button(frame_botones,text="Limpiar",command=limpiar_campos).pack(side=tk.RIGHT, padx=5)
        ttk.Button(frame_botones,text="Cancelar",command=dialogo.destroy).pack(side=tk.LEFT, padx=5)

        def on_enter(event):
            guardar_estudiante()

        dialogo.bind('<Return>', on_enter)

    def eliminar_estudiantes_seleccionados(self):
        seleccionados = self.tree_estudiantes.selection()
        if not seleccionados:
            messagebox.showwarning("Advertencia", "Seleccione al menos un estudiante para eliminar")
            return

        estudiantes_a_eliminar = []
        for item in seleccionados:
            valores = self.tree_estudiantes.item(item, 'values')
            id_estudiante = valores[0]
            nombre = valores[1]
            apellido = valores[2]
            estudiantes_a_eliminar.append((id_estudiante, nombre, apellido))

        lista_estudiantes = "\n".join([f"• {id_est} - {nombre} {apellido}" for id_est, nombre, apellido in estudiantes_a_eliminar])
        
        confirmacion = messagebox.askyesno(
            "Confirmar Eliminación",
            f"¿Está seguro de que desea eliminar los siguientes estudiantes?\n\n"
            f"{lista_estudiantes}\n\n"
            f"Esta acción también eliminará todos sus registros de asistencia y no se puede deshacer.",icon='warning'
        )

        if not confirmacion:
            return

        try:
            for id_estudiante, nombre, apellido in estudiantes_a_eliminar:
                resultado, mensaje = self.db_manager.eliminar_estudiante(id_estudiante)
                if not resultado:
                    messagebox.showerror("Error", f"No se pudo eliminar {nombre} {apellido}: {mensaje}")
                    return

            self.estudiantes, _ = self.db_manager.obtener_estudiantes()
            self.generador_reportes.estudiantes = self.estudiantes
            self.asistencias, _ = self.db_manager.obtener_asistencias()

            self.actualizar_lista_estudiantes()
            self.actualizar_combobox_estudiantes()
            self.actualizar_contador_estudiantes()

            messagebox.showinfo(
                "Éxito",f"Se eliminaron {len(estudiantes_a_eliminar)} estudiantes correctamente"
            )

        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron eliminar los estudiantes: {str(e)}")

    def mostrar_dialogo_eliminar_estudiante(self):
        if not self.estudiantes:
            messagebox.showinfo("Información", "No hay estudiantes registrados para eliminar")
            return

        dialogo = tk.Toplevel(self.root)
        dialogo.title("Eliminar Estudiante")
        dialogo.geometry("500x400")
        dialogo.configure(bg=self.color_fondo)
        dialogo.resizable(False, False)

        dialogo.transient(self.root)
        dialogo.grab_set()

        frame_principal = ttk.Frame(dialogo, style="TFrame")
        frame_principal.pack(fill='both', expand=True, padx=20, pady=20)

        ttk.Label(frame_principal,text="Seleccione el estudiante a eliminar",font=('Arial', 12, 'bold')).pack(pady=(0, 15))

        frame_tree = ttk.Frame(frame_principal)
        frame_tree.pack(fill='both', expand=True, pady=10)

        columns = ('id', 'nombre', 'apellido')
        tree_seleccion = ttk.Treeview(frame_tree, columns=columns, show='headings', height=10)
        
        tree_seleccion.heading('id', text='ID')
        tree_seleccion.heading('nombre', text='Nombre')
        tree_seleccion.heading('apellido', text='Apellido')

        tree_seleccion.column('id', width=80, anchor='center')
        tree_seleccion.column('nombre', width=150, anchor='center')
        tree_seleccion.column('apellido', width=150, anchor='center')

        for est in self.estudiantes:
            tree_seleccion.insert('', 'end', values=(est.id_estudiante, est.nombre, est.apellido))

        scrollbar = ttk.Scrollbar(frame_tree, orient=tk.VERTICAL, command=tree_seleccion.yview)
        tree_seleccion.configure(yscrollcommand=scrollbar.set)

        tree_seleccion.pack(side=tk.LEFT, fill='both', expand=True)
        scrollbar.pack(side=tk.RIGHT, fill='y')

        frame_botones = ttk.Frame(frame_principal)
        frame_botones.pack(fill='x', pady=(20, 0))

        def eliminar_seleccionado():
            seleccion = tree_seleccion.selection()
            if not seleccion:
                messagebox.showwarning("Advertencia", "Seleccione un estudiante para eliminar", parent=dialogo)
                return

            valores = tree_seleccion.item(seleccion[0], 'values')
            id_estudiante = valores[0]
            nombre = valores[1]
            apellido = valores[2]

            confirmacion = messagebox.askyesno(
                "Confirmar Eliminación",
                f"¿Está seguro de que desea eliminar al estudiante?\n\n"
                f"ID: {id_estudiante}\n"
                f"Nombre: {nombre} {apellido}\n\n"
                f"Esta acción también eliminará todos sus registros de asistencia y no se puede deshacer.",
                parent=dialogo,
                icon='warning'
            )

            if not confirmacion:
                return

            try:
                resultado, mensaje = self.db_manager.eliminar_estudiante(id_estudiante)
                if resultado:
                    self.estudiantes, _ = self.db_manager.obtener_estudiantes()
                    self.generador_reportes.estudiantes = self.estudiantes
                    self.asistencias, _ = self.db_manager.obtener_asistencias()

                    self.actualizar_lista_estudiantes()
                    self.actualizar_combobox_estudiantes()
                    self.actualizar_contador_estudiantes()

                    messagebox.showinfo("Éxito", f"Estudiante eliminado correctamente", parent=dialogo)
                    dialogo.destroy()
                else:
                    messagebox.showerror("Error", f"No se pudo eliminar el estudiante: {mensaje}", parent=dialogo)

            except Exception as e:
                messagebox.showerror("Error", f"Error al eliminar el estudiante: {str(e)}", parent=dialogo)

        ttk.Button(frame_botones, 
                text="Eliminar Seleccionado",command=eliminar_seleccionado,style="Peligro.TButton").pack(side=tk.RIGHT, padx=5)

        ttk.Button(frame_botones,text="Cancelar",command=dialogo.destroy).pack(side=tk.LEFT, padx=5)

    def respaldar_base_datos(self):
        try:
            directorio = filedialog.askdirectory(
                title="Seleccionar carpeta para guardar el respaldo"
            )
            
            if not directorio:
                return  
            
            fecha_actual = datetime.now().strftime("%Y%m%d_%H%M%S")

            archivo_estudiantes = os.path.join(directorio, f"respaldo_estudiantes_{fecha_actual}.csv")
            estudiantes, mensaje = self.db_manager.obtener_estudiantes()
            
            with open(archivo_estudiantes, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['id_estudiante', 'nombre', 'apellido'])
                for estudiante in estudiantes:
                    writer.writerow([estudiante.id_estudiante, estudiante.nombre, estudiante.apellido])

            archivo_asistencias = os.path.join(directorio, f"respaldo_asistencias_{fecha_actual}.csv")
            asistencias, mensaje = self.db_manager.obtener_asistencias()
            
            with open(archivo_asistencias, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['id_estudiante', 'fecha', 'estado'])
                for asistencia in asistencias:
                    writer.writerow([asistencia.id_estudiante, asistencia.fecha, asistencia.estado])

            archivo_info = os.path.join(directorio, f"info_respaldo_{fecha_actual}.txt")
            with open(archivo_info, 'w', encoding='utf-8') as f:
                f.write(f"RESPALDO DEL SISTEMA DE ASISTENCIA\n")
                f.write(f"Fecha del respaldo: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Total de estudiantes: {len(estudiantes)}\n")
                f.write(f"Total de registros de asistencia: {len(asistencias)}\n")
                f.write(f"\nArchivos generados:\n")
                f.write(f"- {os.path.basename(archivo_estudiantes)}\n")
                f.write(f"- {os.path.basename(archivo_asistencias)}\n")
                f.write(f"- {os.path.basename(archivo_info)}\n")
            
            messagebox.showinfo(
                "Respaldo Completado",
                f"Respaldo generado correctamente en:\n{directorio}\n\n"
                f"Estudiantes respaldados: {len(estudiantes)}\n"
                f"Asistencias respaldadas: {len(asistencias)}\n\n"
                f"Archivos creados:\n"
                f"respaldo_estudiantes_{fecha_actual}.csv\n"
                f"respaldo_asistencias_{fecha_actual}.csv\n"
                f"info_respaldo_{fecha_actual}.txt"
            )
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo generar el respaldo: {str(e)}")

    def on_fecha_cambiada_registro(self, event=None):
        self.actualizar_lista_estudiantes()

    def establecer_fecha_hoy(self):
        fecha_hoy = date.today()
        self.calendario_registro.set_date(fecha_hoy)
        self.calendario_consulta.set_date(fecha_hoy)
        menu_archivo = tk.Menu(menubar, tearoff=0, bg=self.color_fondo, fg=self.color_texto,
                               activebackground=self.color_secundario, activeforeground="white")
        menubar.add_cascade(label="📁 Archivo", menu=menu_archivo)
        menu_archivo.add_command(label="📂 Cargar Estudiantes CSV", command=self.cargar_estudiantes_dialogo)
        menu_archivo.add_command(label="📊 Exportar Reporte CSV", command=self.exportar_reporte_csv)
        menu_archivo.add_separator()
        menu_archivo.add_command(label="🚪 Salir", command=self.on_salir)

        menu_db = tk.Menu(menubar, tearoff=0, bg=self.color_fondo, fg=self.color_texto,
                          activebackground=self.color_secundario, activeforeground="white")
        menubar.add_cascade(label="🗃️ Base de Datos", menu=menu_db)
        menu_db.add_command(label="💾 Respaldar BD", command=self.respaldar_base_datos)
        menu_db.add_command(label="📈 Estadísticas BD", command=self.mostrar_estadisticas)

        menu_ayuda = tk.Menu(menubar, tearoff=0, bg=self.color_fondo, fg=self.color_texto,
                             activebackground=self.color_secundario, activeforeground="white")
        menubar.add_cascade(label="❓ Ayuda", menu=menu_ayuda)
        menu_ayuda.add_command(label="ℹ️ Acerca de", command=self.mostrar_acerca_de)

    def mostrar_acerca_de(self):
        acerca_de = """
        Sistema de Gestión de Asistencia Estudiantil

        Versión: 2.0
        Desarrollado para instituciones educativas

        Funcionalidades:
        • Registro de asistencia diaria
        • Consulta de historial de asistencia
        • Generación de reportes y estadísticas
        • Alertas de baja asistencia
        • Exportación de datos

        ¡Gracias por utilizar nuestro sistema!
        """
        messagebox.showinfo("Acerca del Sistema", acerca_de)

    # Los métodos restantes se mantienen exactamente igual que en tu código original
    # (establecer_fecha_hoy, actualizar_lista_estudiantes, etc.)
    # Solo se han mejorado visualmente los elementos de la interfaz

    def establecer_fecha_hoy(self):
        self.fecha_var.set(date.today().strftime("%Y-%m-%d"))
        self.actualizar_lista_estudiantes()

    def actualizar_lista_estudiantes(self):
        for item in self.tree_estudiantes.get_children():
            self.tree_estudiantes.delete(item)

        fecha_seleccionada = self.calendario_registro.get_date()
        fecha_str = fecha_seleccionada.strftime("%Y-%m-%d")
        
        asistencias_fecha, _ = self.db_manager.obtener_asistencias_por_fecha(fecha_str)
        
        asistencias_dict = {a.id_estudiante: a.estado for a in asistencias_fecha}
        
        for est in self.estudiantes:
            estado = asistencias_dict.get(est.id_estudiante, "No registrado")
            self.tree_estudiantes.insert('', 'end', values=(
                est.id_estudiante, est.nombre, est.apellido, estado)
            )

    def actualizar_combobox_estudiantes(self):
        opciones_estudiantes = [f"{est.id_estudiante} - {est.nombre} {est.apellido}" for est in self.estudiantes]
        fecha_actual = self.fecha_var.get()
        asistencias_fecha, _ = self.db_manager.obtener_asistencias_por_fecha(fecha_actual)

        asistencias_dict = {a.id_estudiante: a.estado for a in asistencias_fecha}

        for est in self.estudiantes:
            estado = asistencias_dict.get(est.id_estudiante, "No registrado")
            self.tree_estudiantes.insert('', 'end', values=(
                est.id_estudiante, est.nombre, est.apellido, estado
            ))

    def actualizar_combobox_estudiantes(self):
        opciones_estudiantes = [f"{est.id_estudiante} - {est.nombre} {est.apellido}"
                                for est in self.estudiantes]
        self.combo_estudiantes['values'] = opciones_estudiantes
        if opciones_estudiantes:
            self.filtro_estudiante_var.set(opciones_estudiantes[0])

    def on_estudiante_seleccionado(self, event):
        seleccion = self.tree_estudiantes.selection()
        if seleccion:
            valores = self.tree_estudiantes.item(seleccion[0], 'values')
            if valores and len(valores) > 3:
                self.estado_var.set(valores[3])

    def aplicar_estado_seleccionados(self):
        seleccionados = self.tree_estudiantes.selection()
        if not seleccionados:
            messagebox.showwarning("Advertencia", "Seleccione al menos un estudiante")
            return
        

        for item in seleccionados:
            valores = self.tree_estudiantes.item(item, 'values')
            nuevos_valores = (valores[0], valores[1], valores[2], self.estado_var.get())
            self.tree_estudiantes.item(item, values=nuevos_valores)

    def guardar_asistencias(self):
        fecha_seleccionada = self.calendario_registro.get_date()
        fecha = fecha_seleccionada.strftime("%Y-%m-%d")
        
        fecha = self.fecha_var.get()

        try:
            datetime.strptime(fecha, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Formato de fecha inválido. Use YYYY-MM-DD")
            return

        for item in self.tree_estudiantes.get_children():
            valores = self.tree_estudiantes.item(item, 'values')
            id_estudiante = valores[0]
            estado = valores[3]
            
            if estado != "No registrado":
                asistencia = Asistencia(id_estudiante, fecha, estado)
                resultado, mensaje = self.db_manager.insertar_asistencia(asistencia)
                
                if not resultado:
                    messagebox.showerror("Error", mensaje)
                    return
        

            if estado != "No registrado":
                asistencia = Asistencia(id_estudiante, fecha, estado)
                resultado, mensaje = self.db_manager.insertar_asistencia(asistencia)

                if not resultado:
                    messagebox.showerror("Error", mensaje)
                    return

        self.asistencias, _ = self.db_manager.obtener_asistencias()
        messagebox.showinfo("Éxito", "Asistencias guardadas correctamente en la base de datos")

    def buscar_por_fecha(self):
        fecha_seleccionada = self.calendario_consulta.get_date()
        fecha = fecha_seleccionada.strftime("%Y-%m-%d")
        
        for item in self.tree_consulta.get_children():
            self.tree_consulta.delete(item)
        
        asistencias, mensaje = self.db_manager.obtener_asistencias_por_fecha(fecha)
        
        for a in asistencias:
            estudiante = next((est for est in self.estudiantes if est.id_estudiante == a.id_estudiante), None)
            
            if estudiante:
                self.tree_consulta.insert('', 'end', values=(
                    a.fecha, a.id_estudiante, estudiante.nombre, estudiante.apellido, a.estado)
                )
        fecha = self.filtro_fecha_var.get()

        try:
            datetime.strptime(fecha, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Formato de fecha inválido. Use YYYY-MM-DD")
            return

        for item in self.tree_consulta.get_children():
            self.tree_consulta.delete(item)

        asistencias, mensaje = self.db_manager.obtener_asistencias_por_fecha(fecha)

        for a in asistencias:
            estudiante = next((est for est in self.estudiantes
                               if est.id_estudiante == a.id_estudiante), None)

            if estudiante:
                self.tree_consulta.insert('', 'end', values=(
                    a.fecha, a.id_estudiante, estudiante.nombre, estudiante.apellido, a.estado
                ))

    def buscar_por_estudiante(self):
        estudiante_nombre = self.filtro_estudiante_var.get()
        if not estudiante_nombre:
            messagebox.showwarning("Advertencia", "Seleccione un estudiante")
            return
        
        id_estudiante = estudiante_nombre.split(' - ')[0]
        
        for item in self.tree_consulta.get_children():
            self.tree_consulta.delete(item)
        
        asistencias, mensaje = self.db_manager.obtener_asistencias_por_estudiante(id_estudiante)
        
        estudiante = next((est for est in self.estudiantes if est.id_estudiante == id_estudiante), None)
        
        if estudiante:
            for a in asistencias:
                self.tree_consulta.insert('', 'end', values=(a.fecha, a.id_estudiante, estudiante.nombre, estudiante.apellido, a.estado)
                )

        id_estudiante = estudiante_nombre.split(' - ')[0]

        for item in self.tree_consulta.get_children():
            self.tree_consulta.delete(item)

        asistencias, mensaje = self.db_manager.obtener_asistencias_por_estudiante(id_estudiante)

        estudiante = next((est for est in self.estudiantes
                           if est.id_estudiante == id_estudiante), None)

        if estudiante:
            for a in asistencias:
                self.tree_consulta.insert('', 'end', values=(
                    a.fecha, a.id_estudiante, estudiante.nombre, estudiante.apellido, a.estado
                ))

    def generar_reporte_asistencia(self):
        for item in self.tree_reportes.get_children():
            self.tree_reportes.delete(item)
        
        reporte = self.generador_reportes.generar_reporte_general()
        
        for item in reporte:
            self.tree_reportes.insert('', 'end', values=(
                item['id_estudiante'], 
                item['nombre'], 
                item['apellido'], 
                f"{item['porcentaje']:.2f}%", 

        reporte = self.generador_reportes.generar_reporte_general()

        for item in reporte:
            self.tree_reportes.insert('', 'end', values=(
                item['id_estudiante'],
                item['nombre'],
                item['apellido'],
                f"{item['porcentaje']:.2f}%",
                item['estado']
            ))

    def mostrar_alertas(self):
        estudiantes_baja = self.generador_reportes.obtener_estudiantes_baja_asistencia()
        
        if estudiantes_baja:
            alertas = "\n".join([f"{est['estudiante'].nombre} {est['estudiante'].apellido}: {est['porcentaje']:.2f}%"for est in estudiantes_baja])
            messagebox.showwarning("Alertas de Baja Asistencia", alertas)
        else:
            messagebox.showinfo("Alertas de Baja Asistencia","No hay estudiantes con baja asistencia")

    def exportar_reporte_csv(self):
        archivo = filedialog.asksaveasfilename(
            defaultextension=".csv",filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        

        if estudiantes_baja:
            alertas = "\n".join([f"{est['estudiante'].nombre} {est['estudiante'].apellido}: {est['porcentaje']:.2f}%"
                                 for est in estudiantes_baja])
            messagebox.showwarning("Alertas de Baja Asistencia", alertas)
        else:
            messagebox.showinfo("Alertas de Baja Asistencia",
                                "No hay estudiantes con baja asistencia")

    def exportar_reporte_csv(self):
        archivo = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )

        if archivo:
            try:
                datos = []
                for item in self.tree_reportes.get_children():
                    valores = self.tree_reportes.item(item, 'values')
                    datos.append(valores)

                with open(archivo, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(['ID', 'Nombre', 'Apellido', 'Porcentaje', 'Estado'])
                    for fila in datos:
                        writer.writerow(fila)
                

                messagebox.showinfo("Éxito", f"Reporte exportado a {archivo}")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo exportar: {str(e)}")

    def exportar_reporte_pdf(self):
        archivo = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        
        if archivo:
            try:
                from fpdf import FPDF
                from datetime import datetime
                
                reporte_data = self.generador_reportes.generar_reporte_general()
                
                pdf = FPDF()
                pdf.add_page()
                
                pdf.set_font("Arial", 'B', 16)
                pdf.cell(0, 10, "REPORTE DE ASISTENCIA ESTUDIANTIL", 0, 1, 'C')
                pdf.ln(5)
                
                pdf.set_font("Arial", 'I', 10)
                fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                pdf.cell(0, 10, f"Generado el: {fecha}", 0, 1, 'C')
                pdf.ln(10)
                
                pdf.set_font("Arial", 'B', 12)
                pdf.set_fill_color(200, 200, 200)
                
                pdf.cell(30, 10, "ID", 1, 0, 'C', True)
                pdf.cell(50, 10, "Nombre", 1, 0, 'C', True)
                pdf.cell(50, 10, "Apellido", 1, 0, 'C', True)
                pdf.cell(30, 10, "Porcentaje", 1, 0, 'C', True)
                pdf.cell(30, 10, "Estado", 1, 1, 'C', True)
                
                pdf.set_font("Arial", '', 10)
                for estudiante in reporte_data:
                    pdf.cell(30, 10, estudiante['id_estudiante'], 1, 0, 'C')
                    pdf.cell(50, 10, estudiante['nombre'], 1, 0, 'L')
                    pdf.cell(50, 10, estudiante['apellido'], 1, 0, 'L')
                    pdf.cell(30, 10, f"{estudiante['porcentaje']:.1f}%", 1, 0, 'C')
                    pdf.cell(30, 10, estudiante['estado'], 1, 1, 'C')
                
                pdf.output(archivo)
                messagebox.showinfo("Éxito", f"PDF exportado: {archivo}")
                
            except ImportError:
                messagebox.showerror("Error", "Necesitas instalar FPDF: pip install fpdf")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo crear el PDF: {str(e)}")

    def generar_plantilla_csv(self):
        archivo = filedialog.asksaveasfilename(
            title="Guardar plantilla CSV",defaultextension=".csv", filetypes=[("Archivos CSV", "*.csv")]
    def cargar_estudiantes_dialogo(self):
        archivo = filedialog.askopenfilename(
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )

        if archivo:
            try:
                nuevos_estudiantes = []
                with open(archivo, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        from modelos.estudiante import Estudiante
                        estudiante = Estudiante(
                            row['id_estudiante'].strip(),
                            row['nombre'].strip(),
                            row['apellido'].strip()
                        )
                        nuevos_estudiantes.append(estudiante)

                for est in nuevos_estudiantes:
                    self.db_manager.insertar_estudiante(est)

                self.estudiantes, _ = self.db_manager.obtener_estudiantes()
                self.generador_reportes.estudiantes = self.estudiantes
                self.actualizar_lista_estudiantes()
                self.actualizar_combobox_estudiantes()

                messagebox.showinfo("Éxito", f"{len(nuevos_estudiantes)} estudiantes cargados correctamente")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo cargar el archivo: {str(e)}")

    def respaldar_base_datos(self):
        archivo = filedialog.asksaveasfilename(
            defaultextension=".db",
            filetypes=[("SQLite Database", "*.db"), ("All files", "*.*")]
        )

        if archivo:
            try:
                with open(archivo, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(['id_estudiante', 'nombre', 'apellido'])
                    writer.writerow(['001', 'Juan', 'Pérez'])
                    writer.writerow(['002', 'María', 'García'])
                    writer.writerow(['003', 'Carlos', 'López'])

                messagebox.showinfo("Plantilla generada", f" Plantilla CSV generada correctamente en:\n{archivo}\n\n""Por favor complete con los datos de sus estudiantes.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo generar la plantilla: {str(e)}")
                import shutil
                shutil.copy2("asistencia.db", archivo)
                messagebox.showinfo("Éxito", f"Base de datos respaldada en {archivo}")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo respaldar: {str(e)}")

    def mostrar_estadisticas(self):
        try:
            estudiantes, _ = self.db_manager.obtener_estudiantes()
            asistencias, _ = self.db_manager.obtener_asistencias()

            estadisticas = f"""
            ESTADÍSTICAS DE LA BASE DE DATOS:

            • Total de estudiantes: {len(estudiantes)}
            • Total de registros de asistencia: {len(asistencias)}
            • Promedio de asistencias por estudiante: {len(asistencias) / len(estudiantes) if estudiantes else 0:.1f}

            Estudiantes con baja asistencia (<70%):"""

            baja_asistencia = self.generador_reportes.obtener_estudiantes_baja_asistencia()
            for est in baja_asistencia:
                estadisticas += f"\n   - {est['estudiante'].nombre} {est['estudiante'].apellido}: {est['porcentaje']:.1f}%"

            messagebox.showinfo("Estadísticas de la Base de Datos", estadisticas)

        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron obtener estadísticas: {str(e)}")

    def actualizar_contador_estudiantes(self):
        self.label_info_estudiantes.config(text=f"Estudiantes cargados: {len(self.estudiantes)}")

    def on_salir(self):
        self.db_manager.close()
        self.root.quit()