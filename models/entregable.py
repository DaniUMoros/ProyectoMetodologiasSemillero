class Entregable:
    """Modelo para representar un Entregable de un Semillero"""

    TIPOS_VALIDOS = [
        "Artículo científico",
        "Working paper",
        "Boletín divulgativo",
        "Evento científico",
        "Prototipo"
    ]

    ESTADOS = ["pendiente", "aprobado", "rechazado"]

    def __init__(self, id=None, titulo="", descripcion="", tipo="",
                 semillero_id=None, fecha_entrega=None, estado="pendiente"):
        self.id = id
        self.titulo = titulo
        self.descripcion = descripcion
        self.tipo = tipo
        self.semillero_id = semillero_id
        self.fecha_entrega = fecha_entrega
        self.estado = estado

        # Relaciones
        self.semillero_nombre = None

    def __str__(self):
        return f"{self.titulo} - {self.tipo} ({self.estado.upper()})"

    def validar(self):
        """Valida que el entregable cumpla con los requisitos mínimos"""
        errores = []

        if not self.titulo:
            errores.append("El título del entregable es obligatorio")

        if not self.descripcion:
            errores.append("La descripción del entregable es obligatoria")

        if not self.tipo:
            errores.append("El tipo de entregable es obligatorio")
        elif self.tipo not in self.TIPOS_VALIDOS:
            errores.append(f"El tipo de entregable debe ser uno de: {', '.join(self.TIPOS_VALIDOS)}")

        if not self.semillero_id:
            errores.append("Debe estar asociado a un semillero")

        return errores

    def detalles(self):
        """Retorna los detalles completos del entregable"""
        estado_fmt = self.estado.upper()

        detalles = [
            f"TÍTULO: {self.titulo}",
            f"TIPO: {self.tipo}",
            f"ESTADO: {estado_fmt}",
            f"SEMILLERO: {self.semillero_nombre or 'No asignado'}",
            f"FECHA DE ENTREGA: {self.fecha_entrega or 'No definida'}",
            f"\nDESCRIPCIÓN: {self.descripcion}"
        ]

        return "\n".join(detalles)
