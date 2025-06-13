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
            LEFT JOIN semilleros s ON e.semillero_id = s.semillero_id
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

    def obtener_todos(self):
        """Obtiene todos los entregables con información de sus semilleros asociados

        Returns:
            list: Lista de objetos Entregable con información del semillero
        """
        query = """
            SELECT e.*, s.nombre as semillero_nombre
            FROM entregables e
            LEFT JOIN semilleros s ON e.semillero_id = s.semillero_id
            ORDER BY e.estado, s.nombre
        """

        resultados = self.db.execute_query(query, fetch='all')
        entregables = []

        for row in resultados:
            entregable = Entregable(
                id=row['id'],
                titulo=row['titulo'],
                descripcion=row['descripcion'],
                tipo=row['tipo'],
                semillero_id=row['semillero_id'],
                fecha_entrega=row['fecha_entrega'],
                estado=row['estado']
            )
            entregable.semillero_nombre = row['semillero_nombre']
            entregables.append(entregable)

        return entregables

    def cambiar_estado(self, entregable_id, nuevo_estado):
        """Cambia el estado de un entregable (pendiente, aprobado, rechazado)"""
        if nuevo_estado not in Entregable.ESTADOS:
            return False, f"Estado no válido. Debe ser uno de: {', '.join(Entregable.ESTADOS)}"

        query = "UPDATE entregables SET estado = ? WHERE id = ?"
        self.db.execute_query(query, (nuevo_estado, entregable_id))

        return True, f"Estado del entregable actualizado a: {nuevo_estado}"

    def aprobar_denegar_entregable(self, entregable_id, aprobado=True):
        """Aprueba o deniega un entregable

        Args:
            entregable_id (int): ID del entregable
            aprobado (bool): True para aprobar, False para denegar

        Returns:
            tuple: (bool, str) - (éxito, mensaje)
        """
        nuevo_estado = "aprobado" if aprobado else "rechazado"

        query = "UPDATE entregables SET estado = ? WHERE id = ?"
        try:
            self.db.execute_query(query, (nuevo_estado, entregable_id))
            accion = "aprobado" if aprobado else "rechazado"
            return True, f"El entregable ha sido {accion} exitosamente"
        except Exception as e:
            return False, f"Error al {nuevo_estado} el entregable: {str(e)}"
