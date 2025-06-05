import sqlite3
import os
import json
import re  # Añadido para usar re.search en el método execute_query


class Database:
    """Gestión de conexión y operaciones con SQLite"""

    def __init__(self, db_path="db/semilleros.db"):
        self.db_path = db_path
        self._crear_estructura()
        self._verificar_estructura()  # Añadimos verificación adicional

    def _get_connection(self):
        """Abre la conexión y activa claves foráneas."""
        conn = sqlite3.connect(self.db_path)   # ← conexión directa, no recurse aquí
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    def _crear_estructura(self):
        """Crea la estructura de la base de datos si no existe"""
        conn = self._get_connection()
        cursor = conn.cursor()

        # Tabla de grupos de investigación
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS grupos_investigacion (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            facultad TEXT,
            area_conocimiento TEXT,
            director TEXT,
            campo TEXT,
            identificador TEXT
        )
        ''')

        # Tabla de semilleros
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS semilleros (
            semillero_id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            objetivo_principal TEXT,
            objetivos_especificos TEXT,
            grupo_id INTEGER,
            status TEXT DEFAULT 'pendiente',
            FOREIGN KEY (grupo_id) REFERENCES grupos_investigacion(id)
        )
        ''')

        # Tabla de investigadores
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS investigadores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            tipo TEXT NOT NULL,
            identificacion TEXT,
            programa TEXT,
            email TEXT,
            semillero_id INTEGER,
            FOREIGN KEY (semillero_id) REFERENCES semilleros(semillero_id)
        );       
        ''')

        # Tabla de relación entre semilleros e investigadores
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS semillero_investigador (
            semillero_id INTEGER,
            investigador_id INTEGER,
            rol TEXT,
            PRIMARY KEY (semillero_id, investigador_id),
            FOREIGN KEY (semillero_id) REFERENCES semilleros(semillero_id),
            FOREIGN KEY (investigador_id) REFERENCES investigadores(id)
        )
        ''')

        # Tabla de entregables
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS entregables (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            descripcion TEXT,
            tipo TEXT NOT NULL,
            semillero_id INTEGER NOT NULL,
            fecha_entrega TEXT,
            estado TEXT DEFAULT 'pendiente',
            FOREIGN KEY (semillero_id) REFERENCES semilleros(semillero_id)
        )
        ''')

        conn.commit()
        conn.close()

    def _verificar_estructura(self):
        """Verifica y actualiza la estructura de la base de datos si es necesario"""
        conn = self._get_connection()
        cursor = conn.cursor()

        # Verificar si existe la columna objetivo_principal en la tabla semilleros
        cursor.execute("PRAGMA table_info(semilleros)")
        columnas = [info[1] for info in cursor.fetchall()]

        # Si no existe la columna, añadirla
        if 'objetivo_principal' not in columnas:
            try:
                cursor.execute('ALTER TABLE semilleros ADD COLUMN objetivo_principal TEXT NOT NULL DEFAULT ""')
                conn.commit()
                print("Base de datos actualizada: añadida columna objetivo_principal a la tabla semilleros")
            except sqlite3.Error as e:
                print(f"Error al actualizar la estructura de la base de datos: {e}")

        conn.close()

    def execute_query(self, query, params=None, fetch=None):
        """Ejecuta una consulta SQL y opcionalmente devuelve resultados

                Args:
                    query (str): Consulta SQL a ejecutar
                    params (tuple, optional): Parámetros para la consulta
                    fetch (str, optional): Tipo de fetch a realizar ('one', 'all', None)

                Returns:
                    Resultados de la consulta según el parámetro fetch
                """
        conn = self._get_connection()
        conn.row_factory = sqlite3.Row  # Para poder acceder por nombre de columna
        cursor = conn.cursor()

        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)

            result = None
            if fetch == 'one':
                result = cursor.fetchone()
            elif fetch == 'all':
                result = cursor.fetchall()
            else:
                conn.commit()
                result = cursor.lastrowid  # Retornar el ID de la última fila insertada

        except sqlite3.OperationalError as e:
            if "no such column" in str(e):
                print(f"Error de columna: {e}")
                # Obtener la estructura de la tabla mencionada en el error
                tabla = str(e).split(":")[-1].strip().split(".")[0]
                if tabla:
                    tabla_real = tabla
                    # Si es un alias, intentar obtener el nombre real de la tabla
                    if "FROM" in query and tabla in query:
                        # Buscar el alias en la consulta
                        match = re.search(r'FROM\s+(\w+)\s+' + tabla, query, re.IGNORECASE)
                        if match:
                            tabla_real = match.group(1)
                        else:
                            # Intenta buscar el alias en cualquier parte
                            match = re.search(r'(\w+)\s+' + tabla + r'\b', query, re.IGNORECASE)
                            if match:
                                tabla_real = match.group(1)

                    cursor.execute(f"PRAGMA table_info({tabla_real})")
                    columnas = cursor.fetchall()
                    print(f"Columnas disponibles en la tabla {tabla_real}:")
                    for col in columnas:
                        print(f"- {col[1]} ({col[2]})")
            raise
        finally:
            conn.close()

        return result

    def execute_many(self, query, params_list):
        """Ejecuta una consulta SQL múltiple veces con diferentes parámetros

        Args:
            query (str): Consulta SQL a ejecutar
            params_list (list): Lista de tuplas con parámetros
        """
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.executemany(query, params_list)
        conn.commit()

        conn.close()

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
        # Incluimos la columna objetivos_especificos que existe en la tabla
        query = """
                INSERT INTO semilleros 
                (nombre, objetivo_principal, objetivos_especificos, grupo_id, status) 
                VALUES (?, ?, ?, ?, ?)
            """

        params = (
            semillero.nombre,
            semillero.objetivo_principal,
            semillero.objetivos_especificos,  # Añadido este campo que faltaba
            semillero.grupo_id,
            semillero.status
        )

        # Corregido: self.db debería ser self porque ya estamos en la clase Database
        semillero_id = self.execute_query(query, params)

        # Si se creó correctamente, añadir los investigadores
        if semillero_id:
            self._guardar_investigadores(semillero_id, semillero.estudiantes, "estudiante")
            self._guardar_investigadores(semillero_id, semillero.tutores, "tutor")

            return semillero_id, []

        return None, ["Error al crear el semillero en la base de datos"]
