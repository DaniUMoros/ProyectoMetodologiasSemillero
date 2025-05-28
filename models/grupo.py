class Grupo:
    """Modelo para representar un Grupo de Investigación"""

    def __init__(self, id=None, nombre="", campo="", identificador="", director="", semillero_id=None):
        self.id = id
        self.nombre = nombre
        self.campo = campo
        self.identificador = identificador
        self.director = director
        self.semillero_id = semillero_id

    def __str__(self):
        return f"{self.nombre} - {self.identificador}"

    def detalles(self):
        """Retorna los detalles completos del grupo de investigación"""
        semillero_info = f"Asignado: {self.semillero_id}" if self.semillero_id else "No asignado"

        return (f"NOMBRE: {self.nombre}\n"
                f"CAMPO: {self.campo}\n"
                f"IDENTIFICADOR: {self.identificador}\n"
                f"DIRECTOR: {self.director}\n"
                f"SEMILLERO: {semillero_info}")
