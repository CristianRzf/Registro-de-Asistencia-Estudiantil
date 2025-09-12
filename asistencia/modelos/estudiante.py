class Estudiante:
    def init(self, id_estudiante, nombre, apellido):
        self.id_estudiante = id_estudiante
        self.nombre = nombre
        self.apellido = apellido

    def str(self):
        return f"{self.nombre} {self.apellido}"

    def to_dict(self):
        return {
            'id_estudiante': self.id_estudiante,
            'nombre': self.nombre,
            'apellido': self.apellido
        }

    def from_dict(cls, data):
        return cls(data['id_estudiante'], data['nombre'], data['apellido'])