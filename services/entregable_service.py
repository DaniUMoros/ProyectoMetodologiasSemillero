from datetime import datetime
from models.entregable import Entregable


class EntregableService:
    """Servicio para gestionar entregables de semilleros"""

    def __init__(self, db):
        self.db = db

    def crear_entregable(self, entregable):
        """Crea un nuevo entregable en la base de datos"""
        # Verificar si el semillero ya tiene un entregable
        query_check = """
            SELECT COUNT(*) as total FROM entregables 
            WHERE semillero_id = ?
        """
        result = self.db.execute_query(query_check, (entregable.semillero_id,), fetch='one')

        if result and result['total'] > 0:
            return False, "Este semillero ya tiene un entregable asignado"

        # Guardar la fecha actual si no se proporcionó una
        if not entregable.fecha_entrega:
            entregable.fecha_entrega = datetime.now().strftime("%Y-%m-%d")

        # Insertar el entregable
        query = """
            INSERT INTO entregables (titulo, descripcion, tipo, semillero_id, fecha_entrega, estado)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        params = (
            entregable.titulo,
            entregable.descripcion,
            entregable.tipo,
            entregable.semillero_id,
            entregable.fecha_entrega,
            entregable.estado
        )

        entregable.id = self.db.execute_query(query, params)
        return True, "Entregable creado correctamente"

    def obtener_por_semillero(self, semillero_id):
        """Obtiene el entregable asociado a un semillero"""
        query = """
            SELECT e.*, s.nombre as semillero_nombre
            FROM entregables e
            LEFT JOIN semilleros s ON e.semillero_id = s.id
            WHERE e.semillero_id = ?
        """

        result = self.db.execute_query(query, (semillero_id,), fetch='one')

        if not result:
            return None

        entregable = Entregable(
            id=result['id'],
            titulo=result['titulo'],
            descripcion=result['descripcion'],
            tipo=result['tipo'],
            semillero_id=result['semillero_id'],
            fecha_entrega=result['fecha_entrega'],
            estado=result['estado']
        )

        entregable.semillero_nombre = result['semillero_nombre']
        return entregable

    def cambiar_estado(self, entregable_id, nuevo_estado):
        """Cambia el estado de un entregable (pendiente, aprobado, rechazado)"""
        if nuevo_estado not in Entregable.ESTADOS:
            return False, f"Estado no válido. Debe ser uno de: {', '.join(Entregable.ESTADOS)}"

        query = "UPDATE entregables SET estado = ? WHERE id = ?"
        self.db.execute_query(query, (nuevo_estado, entregable_id))

        return True, f"Estado del entregable actualizado a: {nuevo_estado}"
