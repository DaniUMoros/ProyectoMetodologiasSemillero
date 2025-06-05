import json
from models.semillero import Semillero
from models.investigador import Investigador


class SemilleroService:
    """Lógica de negocio para semilleros de investigación"""

    def __init__(self, database):
        self.db = database

    def crear_semillero(self, semillero):
        """Crea un nuevo semillero en la base de datos

        Args:
            semillero (Semillero): Objeto Semillero a crear

        Returns:
            int: ID del semillero creado o None si hay errores
        """
        # Validar que cumpla con los requisitos
        errores = semillero.validar()
        if errores:
            return None, errores

        # Insertar el semillero en la base de datos
        query = """
            INSERT INTO semilleros 
            (nombre, objetivo_principal, objetivos_especificos, grupo_id, status) 
            VALUES (?, ?, ?, ?, ?)
        """

        # Convertir lista de objetivos a JSON para almacenar
        objetivos_json = json.dumps(semillero.objetivos_especificos)

        params = (
            semillero.nombre,
            semillero.objetivo_principal,
            objetivos_json,
            semillero.grupo_id,
            semillero.status
        )

        semillero_id = self.db.execute_query(query, params)

        # Si se creó correctamente, añadir los investigadores
        if semillero_id:
            self._guardar_investigadores(semillero_id, semillero.estudiantes, "estudiante")
            self._guardar_investigadores(semillero_id, semillero.tutores, "tutor")

            return semillero_id, []

        return None, ["Error al crear el semillero en la base de datos"]

    def _guardar_investigadores(self, semillero_id, investigadores, tipo):
        """Guarda los investigadores asociados a un semillero

        Args:
            semillero_id (int): ID del semillero
            investigadores (list): Lista de nombres o objetos Investigador
            tipo (str): Tipo de investigador ('estudiante' o 'tutor')
        """
        if not investigadores:
            return

        query = """
            INSERT INTO investigadores 
            (nombre, tipo, email, semillero_id) 
            VALUES (?, ?, ?, ?)
        """

        params_list = []
        for inv in investigadores:
            # Si es un objeto Investigador
            if isinstance(inv, Investigador):
                params_list.append((inv.nombre, tipo, inv.email, semillero_id))
            # Si es un diccionario
            elif isinstance(inv, dict):
                params_list.append((
                    inv.get('nombre', ''),
                    tipo,
                    inv.get('email', ''),
                    semillero_id
                ))
            # Si es un string (solo nombre)
            else:
                params_list.append((str(inv), tipo, "", semillero_id))

        if params_list:
            self.db.execute_many(query, params_list)
    
    # services/semillero_service.py





    # ... tus otros métodos (obtener_todos, crear_semillero, eliminar_semillero, etc.) ...

    def editar_semillero(self, semillero_id, nombre, objetivo_principal, objetivos_especificos, grupo_id, status):
        """
        Actualiza los campos de un semillero existente en la base de datos.
        - semillero_id (int): ID del semillero a actualizar.
        - nombre (str): nuevo nombre.
        - objetivo_principal (str): nuevo objetivo principal.
        - objetivos_especificos (list): nueva lista de objetivos específicos.
        - grupo_id (int): nuevo grupo asignado.
        - status (str): nuevo estado ("activo" o "pendiente", por ejemplo).

        Retorna True si se actualizó al menos una fila, False en caso contrario.
        """
        # Convertir la lista de objetivos a JSON
        objetivos_json = json.dumps(objetivos_especificos)

        query = """
            UPDATE semilleros
            SET nombre = ?,
                objetivo_principal = ?,
                objetivos_especificos = ?,
                grupo_id = ?,
                status = ?
            WHERE semillero_id = ?;
        """
        params = (
            nombre,
            objetivo_principal,
            objetivos_json,
            grupo_id,
            status,
            semillero_id
        )
        try:
            filas_afectadas = self.db.execute_query(query, params)
            return (filas_afectadas > 0)
        except Exception as e:
            print(f"Error al editar el semillero: {e}")
            return False

    
    def eliminar_semillero(self, semillero_id):
        """
        Borra de la base de datos el semillero cuyo semillero_id fue pasado como parámetro.
        Primero elimina investigadores asociados, luego el semillero en sí.

        Args:
            semillero_id (int): ID del semillero a eliminar.

        Returns:
            bool: True si se borró el semillero (al menos una fila afectada), False en caso contrario.
        """
        # 1) Eliminar TODOS los investigadores cuyo semillero_id coincide:
        query_investigadores = """
            DELETE FROM investigadores
            WHERE semillero_id = ?
        """
        try:
            # Ejecutamos el delete; asumimos que execute_query devuelve cursor o rowcount
            self.db.execute_query(query_investigadores, (semillero_id,))
        except Exception as e:
            # Podrías loguear e ignorar (porque tal vez no haya investigadores asociados) o propagar el error
            # Por simplicidad, lo imprimimos y seguimos
            print(f"Advertencia al eliminar investigadores asociados: {e}")

        # 2) Ahora eliminamos el semillero:
        query_semillero = """
            DELETE FROM semilleros
            WHERE semillero_id = ?
        """
        try:
            resultado = self.db.execute_query(query_semillero, (semillero_id,))
            # Dependiendo de tu implementación de execute_query:
            # - Si retorna rowcount: usar `return resultado > 0`
            # - Si retorna None pero ejecuta commit, hacemos luego un SELECT para revisar
            if isinstance(resultado, int):
                return (resultado > 0)
            else:
                # Si tu execute_query no devuelve rowcount, puedes ejecutar:
                # cursor = self.db.execute_query(query_semillero, (semillero_id,))
                # return cursor.rowcount > 0
                return True
        except Exception as e:
            print(f"Error al eliminar el semillero: {e}")
            return False

    def obtener_todos(self):
        """Obtiene todos los semilleros de investigación

            Returns:
                list: Lista de objetos Semillero
            """
        # Primero verificamos la estructura de la tabla
        query_estructura = """
                PRAGMA table_info(semilleros)
            """
        estructura = self.db.execute_query(query_estructura, fetch='all')

        # Basado en la estructura, ajustamos la consulta
        # Suponiendo que la columna se llama 'objetivos' en lugar de 'objetivos_especificos'
        query = """
                SELECT s.semillero_id, s.nombre, s.objetivo_principal, s.objetivos_especificos, 
                s.grupo_id, g.nombre as grupo_nombre, s.status
                FROM semilleros s
                LEFT JOIN grupos_investigacion g ON s.grupo_id = g.id
                ORDER BY s.nombre
            """

        resultados = self.db.execute_query(query, fetch='all')

        semilleros = []
        for row in resultados:
            # Convertir el JSON a lista (ajustamos el nombre de la columna)
            objetivos = json.loads(row['objetivos_especificos'])

            semillero = Semillero(
                id=row['semillero_id'],
                nombre=row['nombre'],
                objetivo_principal=row['objetivo_principal'],
                objetivos_especificos=objetivos,  # Mantenemos el nombre del atributo del objeto
                grupo_id=row['grupo_id'],
                status=row['status']
            )

            semillero.grupo_nombre = row['grupo_nombre']

            # Cargar investigadores asociados
            self._cargar_investigadores(semillero)

            semilleros.append(semillero)

        return semilleros

    def obtener_por_id(self, semillero_id):
        """Obtiene un semillero por su ID

        Args:
            semillero_id (int): ID del semillero

        Returns:
            Semillero: Objeto Semillero o None si no existe
        """
        query = """
            SELECT s.semillero_id, s.nombre, s.objetivo_principal, s.objetivos_especificos, 
                   s.grupo_id, s.status, g.nombre as grupo_nombre
            FROM semilleros s
            JOIN grupos_investigacion g ON s.grupo_id = g.id
            WHERE s.semillero_id = ?
        """

        row = self.db.execute_query(query, (semillero_id,), fetch='one')

        if not row:
            return None

        # Convertir el JSON a lista
        objetivos = json.loads(row['objetivos_especificos'])

        semillero = Semillero(
            id=row['id'],
            nombre=row['nombre'],
            objetivo_principal=row['objetivo_principal'],
            objetivos_especificos=objetivos,
            grupo_id=row['grupo_id'],
            status=row['status']
        )

        semillero.grupo_nombre = row['grupo_nombre']

        # Cargar investigadores asociados
        self._cargar_investigadores(semillero)

        return semillero

    def _cargar_investigadores(self, semillero):
        """Carga los investigadores asociados a un semillero

        Args:
            semillero (Semillero): Objeto Semillero al que cargar los investigadores
        """
        query = """
            SELECT id, nombre, tipo, email
            FROM investigadores
            WHERE semillero_id = ?
            ORDER BY tipo, nombre
        """

        resultados = self.db.execute_query(query, (semillero.id,), fetch='all')

        for row in resultados:
            investigador = Investigador(
                id=row['id'],
                nombre=row['nombre'],
                tipo=row['tipo'],
                email=row['email'],
                semillero_id=semillero.id
            )

            if row['tipo'] == 'estudiante':
                semillero.estudiantes.append(investigador)
            elif row['tipo'] == 'tutor':
                semillero.tutores.append(investigador)

    def cambiar_status(self, semillero_id, nuevo_status):
        """Cambia el estado de un semillero

        Args:
            semillero_id (int): ID del semillero
            nuevo_status (str): Nuevo estado ('activo' o 'pendiente')

        Returns:
            bool: True si se cambió correctamente, False en caso contrario
        """
        if nuevo_status not in ['activo', 'pendiente']:
            return False

        query = "UPDATE semilleros SET status = ? WHERE id = ?"
        self.db.execute_query(query, (nuevo_status, semillero_id))

        return True

    def obtener_por_grupo(self, grupo_id):
        """Obtiene los semilleros asociados a un grupo de investigación

        Args:
            grupo_id (int): ID del grupo de investigación

        Returns:
            list: Lista de objetos Semillero
        """
        query = """
            SELECT s.id, s.nombre, s.objetivo_principal, s.objetivos_especificos, 
                   s.grupo_id, s.status, g.nombre as grupo_nombre
            FROM semilleros s
            JOIN grupos_investigacion g ON s.grupo_id = g.id
            WHERE s.grupo_id = ?
            ORDER BY s.nombre
        """

        resultados = self.db.execute_query(query, (grupo_id,), fetch='all')

        semilleros = []
        for row in resultados:
            # Convertir el JSON a lista
            objetivos = json.loads(row['objetivos_especificos'])

            semillero = Semillero(
                id=row['id'],
                nombre=row['nombre'],
                objetivo_principal=row['objetivo_principal'],
                objetivos_especificos=objetivos,
                grupo_id=row['grupo_id'],
                status=row['status']
            )

            semillero.grupo_nombre = row['grupo_nombre']
            semilleros.append(semillero)

        return semilleros
    

    