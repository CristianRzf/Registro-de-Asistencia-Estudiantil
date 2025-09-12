from datetime import datetime

class Asistencia:
    def init(self, id_estudiante, fecha, estado):
        self.id_estudiante = id_estudiante
        self.fecha = fecha
        self.estado = estado

    def to_dict(self):
        return {
            'id_estudiante': self.id_estudiante,
            'fecha': self.fecha,
            'estado': self.estado
        }

    def from_dict(cls, data):
        return cls(data['id_estudiante'], data['fecha'], data['estado'])

    def es_fecha_valida(self):
        try:
            datetime.strptime(self.fecha, "%Y-%m-%d")
            return True
        except ValueError:
            return False