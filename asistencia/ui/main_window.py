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
    
    def crear_pestaña_reportes(self, parent):
        
        frame_controles = ttk.Frame(parent)
        frame_controles.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(frame_controles, text="Generar Reporte de Asistencia", 
                command=self.generar_reporte_asistencia).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(frame_controles, text="Ver Alertas de Baja Asistencia", 
                command=self.mostrar_alertas).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(frame_controles, text="Exportar a CSV", 
                command=self.exportar_reporte_csv).pack(side=tk.RIGHT, padx=5)
        
        
        frame_reportes = ttk.Frame(parent)
        frame_reportes.pack(fill='both', expand=True, padx=10, pady=5)
        
        columns = ('id_estudiante', 'nombre', 'apellido', 'porcentaje', 'estado')
        self.tree_reportes = ttk.Treeview(frame_reportes, columns=columns, show='headings')
        
        self.tree_reportes.heading('id_estudiante', text='ID')
        self.tree_reportes.heading('nombre', text='Nombre')
        self.tree_reportes.heading('apellido', text='Apellido')
        self.tree_reportes.heading('porcentaje', text='Porcentaje (%)')
        self.tree_reportes.heading('estado', text='Estado')
        
        self.tree_reportes.column('id_estudiante', width=80)
        self.tree_reportes.column('nombre', width=150)
        self.tree_reportes.column('apellido', width=150)
        self.tree_reportes.column('porcentaje', width=100)
        self.tree_reportes.column('estado', width=100)
        
        scrollbar = ttk.Scrollbar(frame_reportes, orient=tk.VERTICAL, command=self.tree_reportes.yview)
        self.tree_reportes.configure(yscrollcommand=scrollbar.set)
        
        self.tree_reportes.pack(side=tk.LEFT, fill='both', expand=True)
        scrollbar.pack(side=tk.RIGHT, fill='y')
    
    def crear_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        
        menu_archivo = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Archivo", menu=menu_archivo)
        menu_archivo.add_command(label="Cargar Estudiantes CSV", command=self.cargar_estudiantes_dialogo)
        menu_archivo.add_command(label="Exportar Reporte CSV", command=self.exportar_reporte_csv)
        menu_archivo.add_separator()
        menu_archivo.add_command(label="Salir", command=self.on_salir)
        
        
        menu_db = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Base de Datos", menu=menu_db)
        menu_db.add_command(label="Respaldar BD", command=self.respaldar_base_datos)
        menu_db.add_command(label="Estadísticas BD", command=self.mostrar_estadisticas)
    
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