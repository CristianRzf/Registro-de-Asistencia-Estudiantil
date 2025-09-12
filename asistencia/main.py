import tkinter as tk
import os
import sys
import random
from servicios.database import DatabaseManager
from servicios.reportes import GeneradorReportes
from ui.main_window import MainWindow

def generar_datos_ejemplo(db_manager):
    
    try:
        
        estudiantes, _ = db_manager.obtener_estudiantes()
        
        if not estudiantes:
            print("Generando datos de ejemplo...")
            
            
            nombres = ["Ana", "Carlos", "María", "José", "Laura", "Miguel", "Elena", "David", "Sofía", "Juan"]
            apellidos = ["García", "Rodríguez", "González", "Fernández", "López", "Martínez", "Pérez", "Sánchez", "Ramírez", "Torres"]
            
            from modelos.estudiante import Estudiante
            from modelos.asistencia import Asistencia
            from datetime import datetime, timedelta
            
            
            for i in range(1, 11):
                nombre = random.choice(nombres)
                apellido = random.choice(apellidos)
                estudiante = Estudiante(f"E{i:03d}", nombre, apellido)
                db_manager.insertar_estudiante(estudiante)
            
            
            hoy = datetime.now()
            for i in range(7):
                fecha_ejemplo = (hoy - timedelta(days=i)).strftime("%Y-%m-%d")
                
                for j in range(1, 11):
                    estado = random.choices(["Presente", "Tarde", "Ausente"], weights=[8, 1, 1])[0]
                    asistencia = Asistencia(f"E{j:03d}", fecha_ejemplo, estado)
                    db_manager.insertar_asistencia(asistencia)
            
            print("Datos de ejemplo generados correctamente")
        else:
            print("La base de datos ya contiene datos")
            
    except Exception as e:
        print(f"Error generando datos de ejemplo: {e}")

def main():
    
    db_manager = DatabaseManager("asistencia.db")
    
    
    generar_datos_ejemplo(db_manager)
    
    
    estudiantes, mensaje_est = db_manager.obtener_estudiantes()
    print(mensaje_est)
    
    asistencias, mensaje_asis = db_manager.obtener_asistencias()
    print(mensaje_asis)
    
    generador_reportes = GeneradorReportes(db_manager)
    
    
    root = tk.Tk()
    
    
    app = MainWindow(root, estudiantes, asistencias, db_manager, generador_reportes)
    
    
    def on_closing():
        db_manager.close()
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    
    root.mainloop()

if __name__ == "__main__":
    main()