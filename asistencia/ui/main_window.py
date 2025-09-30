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
        label_fecha = tk.Label(frame_fecha_actual,
                               text=f"Fecha actual: {fecha_hoy}",
                               font=('Arial', 10, 'italic'),
                               bg=self.color_fondo,
                               fg=self.color_texto)
        label_fecha.pack(side=tk.LEFT)

        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)

        frame_registro = ttk.Frame(notebook)
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

    def crear_menu(self):
        menubar = tk.Menu(self.root, bg=self.color_fondo, fg=self.color_texto, activebackground=self.color_secundario)
        self.root.config(menu=menubar)

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

        self.asistencias, _ = self.db_manager.obtener_asistencias()
        messagebox.showinfo("Éxito", "Asistencias guardadas correctamente en la base de datos")

    def buscar_por_fecha(self):
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
                item['estado']
            ))

    def mostrar_alertas(self):
        estudiantes_baja = self.generador_reportes.obtener_estudiantes_baja_asistencia()

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

    def on_salir(self):
        self.db_manager.close()
        self.root.quit()