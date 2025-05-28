class Semillero:
    """Modelo para representar un Semillero de Investigación"""

    def __init__(self, id=None, nombre="", objetivo_principal="", objetivos_especificos=None,
                 grupo_id=None, status="pendiente"):
        self.id = id
        self.nombre = nombre
        self.objetivo_principal = objetivo_principal
        self.objetivos_especificos = objetivos_especificos or []
        self.grupo_id = grupo_id
        self.status = status  # "activo" o "pendiente"

        # Relaciones
        self.estudiantes = []
        self.tutores = []
        self.grupo_nombre = None  # Para mostrar el nombre del grupo asociado

    def __str__(self):
        return f"{self.nombre} - {self.status.upper()}"

    def validar(self):
        """Valida que el semillero cumpla con los requisitos mínimos"""
        errores = []

        # Validar campos obligatorios
        if not self.nombre:
            errores.append("El nombre del semillero es obligatorio")

        if not self.objetivo_principal:
            errores.append("El objetivo principal es obligatorio")

        if not self.objetivos_especificos:
            errores.append("Debe tener al menos un objetivo específico")

        if not self.grupo_id:
            errores.append("Debe estar adscrito a un grupo de investigación")

        # Validar relaciones
        if len(self.estudiantes) < 2:
            errores.append("Debe tener al menos dos estudiantes")

        if len(self.tutores) < 1 or len(self.tutores) > 2:
            errores.append("Debe tener uno o dos tutores")

        return errores

    def detalles(self):
        """Retorna los detalles completos del semillero"""
        estado = "ACTIVO" if self.status == "activo" else "PENDIENTE"

        detalles = [
            f"NOMBRE: {self.nombre}",
            f"ESTADO: {estado}",
            f"OBJETIVO PRINCIPAL: {self.objetivo_principal}",
            f"GRUPO DE INVESTIGACIÓN: {self.grupo_nombre or 'No asignado'}",
            "\nOBJETIVOS ESPECÍFICOS:"
        ]

        for i, objetivo in enumerate(self.objetivos_especificos, 1):
            detalles.append(f"  {i}. {objetivo}")

        detalles.append("\nESTUDIANTES:")
        for estudiante in self.estudiantes:
            detalles.append(f"  - {estudiante}")

        detalles.append("\nTUTORES:")
        for tutor in self.tutores:
            detalles.append(f"  - {tutor}")

        return "\n".join(detalles)
