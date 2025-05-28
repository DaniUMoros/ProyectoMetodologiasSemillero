class Investigador:
    """Modelo para representar un Investigador (estudiante o tutor)"""

    def __init__(self, id=None, nombre="", tipo="estudiante", email="", semillero_id=None):
        self.id = id
        self.nombre = nombre
        self.tipo = tipo  # "estudiante" o "tutor"
        self.email = email
        self.semillero_id = semillero_id

    def __str__(self):
        return f"{self.nombre} ({self.email})"
