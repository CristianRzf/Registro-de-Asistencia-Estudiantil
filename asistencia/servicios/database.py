import sqlite3
import os
from modelos.estudiante import Estudiante
from modelos.asistencia import Asistencia

class DatabaseManager:
    def __init__(self, db_name="asistencia.db"):
        self.db_name = db_name
        self.connection = None
        self.connect()
        self.create_tables()
    
    def connect(self):
        try:
            self.connection = sqlite3.connect(self.db_name)
            print(f"Conexión establecida con {self.db_name}")
        except sqlite3.Error as e:
            print(f"Error conectando a la base de datos: {e}")
    
    def create_tables(self):
        try:
            cursor = self.connection.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS estudiantes (
                    id_estudiante TEXT PRIMARY KEY,
                    nombre TEXT NOT NULL,
                    apellido TEXT NOT NULL
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS asistencias (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_estudiante TEXT NOT NULL,
                    fecha TEXT NOT NULL,
                    estado TEXT NOT NULL,
                    FOREIGN KEY (id_estudiante) REFERENCES estudiantes (id_estudiante),
                    UNIQUE(id_estudiante, fecha)
                )
            ''')
            
            self.connection.commit()
            print("Tablas verificadas/creadas correctamente")
            
        except sqlite3.Error as e:
            print(f"Error creando tablas: {e}")
    
    def insertar_estudiante(self, estudiante):
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                "INSERT INTO estudiantes (id_estudiante, nombre, apellido) VALUES (?, ?, ?)",
                (estudiante.id_estudiante, estudiante.nombre, estudiante.apellido)
            )
            self.connection.commit()
            return True, "Estudiante insertado correctamente"
        except sqlite3.Error as e:
            return False, f"Error insertando estudiante: {e}"
    
    def obtener_estudiantes(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM estudiantes")
            rows = cursor.fetchall()
            
            estudiantes = []
            for row in rows:
                estudiantes.append(Estudiante(row[0], row[1], row[2]))
            
            return estudiantes, "Estudiantes obtenidos correctamente"
        except sqlite3.Error as e:
            return [], f"Error obteniendo estudiantes: {e}"
    
    def insertar_asistencia(self, asistencia):
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                '''INSERT OR REPLACE INTO asistencias 
                (id_estudiante, fecha, estado) VALUES (?, ?, ?)''',
                (asistencia.id_estudiante, asistencia.fecha, asistencia.estado)
            )
            self.connection.commit()
            return True, "Asistencia registrada correctamente"
        except sqlite3.Error as e:
            return False, f"Error registrando asistencia: {e}"
    
    def obtener_asistencias(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM asistencias")
            rows = cursor.fetchall()
            
            asistencias = []
            for row in rows:
                asistencias.append(Asistencia(row[1], row[2], row[3]))
            
            return asistencias, "Asistencias obtenidas correctamente"
        except sqlite3.Error as e:
            return [], f"Error obteniendo asistencias: {e}"
    
    def obtener_asistencias_por_estudiante(self, id_estudiante):
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                "SELECT * FROM asistencias WHERE id_estudiante = ?",
                (id_estudiante,)
            )
            rows = cursor.fetchall()
            
            asistencias = []
            for row in rows:
                asistencias.append(Asistencia(row[1], row[2], row[3]))
            
            return asistencias, "Asistencias por estudiante obtenidas"
        except sqlite3.Error as e:
            return [], f"Error obteniendo asistencias: {e}"
    
    def obtener_asistencias_por_fecha(self, fecha):
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                "SELECT * FROM asistencias WHERE fecha = ?",
                (fecha,)
            )
            rows = cursor.fetchall()
            
            asistencias = []
            for row in rows:
                asistencias.append(Asistencia(row[1], row[2], row[3]))
            
            return asistencias, "Asistencias por fecha obtenidas"
        except sqlite3.Error as e:
            return [], f"Error obteniendo asistencias: {e}"
    
    def close(self):
        if self.connection:
            self.connection.close()
            print("Conexión cerrada")