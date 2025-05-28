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
                SELECT s.id, s.nombre, s.objetivo_principal, s.objetivos_especificos, 
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
                id=row['id'],
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
            SELECT s.id, s.nombre, s.objetivo_principal, s.objetivos_especificos, 
                   s.grupo_id, s.status, g.nombre as grupo_nombre
            FROM semilleros s
            JOIN grupos_investigacion g ON s.grupo_id = g.id
            WHERE s.id = ?
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
