from datetime import datetime, date
from servicios.database import DatabaseManager
class GeneradorReportes:
    def __init__(self, db_manager):
        self.db_manager = db_manager
    
    def obtener_asistencias_por_estudiante(self, id_estudiante):
        asistencias, _ = self.db_manager.obtener_asistencias_por_estudiante(id_estudiante)
        return asistencias
    
    def obtener_asistencias_por_fecha(self, fecha):
        asistencias, _ = self.db_manager.obtener_asistencias_por_fecha(fecha)
        return asistencias
    
    def calcular_porcentaje_asistencia(self, id_estudiante):
        asistencias_est = self.obtener_asistencias_por_estudiante(id_estudiante)
        if not asistencias_est:
            return 0
        
        presentes = sum(1 for a in asistencias_est if a.estado == "Presente")
        tardes = sum(1 for a in asistencias_est if a.estado == "Tarde")
        
        return (presentes + tardes * 0.7) / len(asistencias_est) * 100
    
    def generar_reporte_general(self):
        estudiantes, _ = self.db_manager.obtener_estudiantes()
        reporte = []
        
        for est in estudiantes:
            porcentaje = self.calcular_porcentaje_asistencia(est.id_estudiante)
            
            estado = "Normal"
            if porcentaje < 70:
                estado = "Baja"
            elif porcentaje < 80:
                estado = "Advertencia"
            
            reporte.append({
                'id_estudiante': est.id_estudiante,
                'nombre': est.nombre,
                'apellido': est.apellido,
                'porcentaje': porcentaje,
                'estado': estado
            })
        
        return reporte
    
    def obtener_estudiantes_baja_asistencia(self, umbral=70):
        estudiantes, _ = self.db_manager.obtener_estudiantes()
        estudiantes_baja = []
        
        for est in estudiantes:
            porcentaje = self.calcular_porcentaje_asistencia(est.id_estudiante)
            if porcentaje < umbral:
                estudiantes_baja.append({
                    'estudiante': est,
                    'porcentaje': porcentaje
                })
        return estudiantes_baja