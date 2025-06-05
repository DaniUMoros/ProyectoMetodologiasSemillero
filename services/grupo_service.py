from models.grupo import Grupo
from db.database import Database


class GrupoService:
    """Lógica de negocio para grupos de investigación"""

    def __init__(self, database=None):
        self.db = database or Database()

    def crear_grupo(self, grupo):
        """Crea un nuevo grupo de investigación en la base de datos"""
        query = """
            INSERT INTO grupos_investigacion 
            (nombre, campo, identificador, director) 
            VALUES (?, ?, ?, ?)
        """
        params = (grupo.nombre, grupo.campo, grupo.identificador, grupo.director)

        return self.db.execute_query(query, params)
    
    def obtener_semilleros(self):
        """Obtiene todos los grupos de investigación"""
        query = "SELECT id, nombre, objetivo_principal, objetivos_especificos, status FROM semilleros ORDER BY nombre"
        resultados = self.db.execute_query(query, fetch='all')

        grupos = []
        for resultado in resultados:
            grupo = Grupo(
                id=resultado['id'],
                nombre=resultado['nombre'],
                campo=resultado['objetivo_principal'],
                identificador=resultado['objetivos_especificos'],
                status=resultado['status']
            )
            grupos.append(grupo)
        return grupos

        

    def obtener_todos(self):
        """Obtiene todos los grupos de investigación"""
        query = "SELECT id, nombre, campo, identificador, director FROM grupos_investigacion ORDER BY nombre"
        resultados = self.db.execute_query(query, fetch='all')

        grupos = []
        for resultado in resultados:
            grupo = Grupo(
                id=resultado['id'],
                nombre=resultado['nombre'],
                campo=resultado['campo'],
                identificador=resultado['identificador'],
                director=resultado['director']
            )
            grupos.append(grupo)

        return grupos

    def obtener_por_id(self, grupo_id):
        """Obtiene un grupo de investigación por su ID"""
        query = """
            SELECT g.id, g.nombre, g.campo, g.identificador, g.director
            FROM grupos_investigacion g
            WHERE g.id = ?
        """
        resultado = self.db.execute_query(query, (grupo_id,), fetch='one')

        if resultado:
            grupo = Grupo(
                id=resultado['id'],
                nombre=resultado['nombre'],
                campo=resultado['campo'],
                identificador=resultado['identificador'],
                director=resultado['director']
            )
            return grupo

        return None
    
    def obtener_por_identificador(self, identificador):
        """Obtiene un grupo de investigación por su identificador único"""
        query = """
            SELECT g.id, g.nombre, g.campo, g.identificador, g.director
            FROM grupos_investigacion g
            WHERE g.identificador = ?
        """
        resultado = self.db.execute_query(query, (identificador,), fetch='one')

        if resultado:
            grupo = Grupo(
                id=resultado['id'],
                nombre=resultado['nombre'],
                campo=resultado['campo'],
                identificador=resultado['identificador'],
                director=resultado['director']
            )
            return grupo

        return None


    def cargar_datos_iniciales(self):
        """Carga los datos iniciales de grupos de investigación si no existen"""
        # Verificar si ya existen datos
        count = self.db.execute_query("SELECT COUNT(*) FROM grupos_investigacion", fetch='one')[0]

        if count == 0:
            # Datos obtenidos de https://universidadean.edu.co/investigacion/grupos-de-investigacion
            grupos = [
                ("ENTREPRENEURSHIP GROUP", "Emprendimiento y gerencia", "COL0011599", "LEON DARIO PARRA BERNAL"),
                ("GRUPO DE INVESTIGACIÓN EN AMBIENTES SOSTENIBLES", "Sostenibilidad", "COL0188929",
                 "YESID ALEXANDER MUÑOZ LOZANO"),
                ("GRUPO DE INVESTIGACIÓN EN INGENIERÍA DE PROCESOS", "Ingeniería de procesos", "COL0033962",
                 "JAVIER DARIO MEJIA SAENZ"),
                ("ONTARE", "Tecnologías de información", "COL0007814", "RICARDO BUITRAGO PULIDO"),
                ("COMUNICACIÓN Y APRENDIZAJE", "Educación", "COL0026909", "CLAUDIA PATRICIA VILLAFAÑE BUSTOS"),
                ("CULTURA Y GESTIÓN SOCIAL", "Humanidades", "COL0050898", "LUIS ALFREDO VARGAS PINTO"),
                ("LINGÜÍSTICA Y COMUNICACIÓN", "Lingüística", "COL0082400", "MARÍA TERESA GÓMEZ LOZANO"),
                ("GESTIÓN DEL CONOCIMIENTO", "Conocimiento e información", "COL0110523",
                 "MONICA BIBIANA GONZALEZ CALIXTO")
            ]

            # Insertar datos en la base de datos
            query = """
                INSERT INTO grupos_investigacion 
                (nombre, campo, identificador, director) 
                VALUES (?, ?, ?, ?)
            """
            self.db.execute_many(query, grupos)
            return len(grupos)

        return 0

    def obtener_lineas_investigacion(self, grupo_id):
        """Obtiene las líneas de investigación de un grupo
        Esta función podría consultar una tabla adicional o una API externa
        Por ahora, retornamos datos ficticios para cada grupo
        """
        # Datos ficticios para las líneas de investigación de cada grupo
        lineas_por_grupo = {
            1: ["Emprendimiento sostenible", "Gestión de la innovación", "Desarrollo empresarial"],
            2: ["Construcción sostenible", "Energías renovables", "Gestión ambiental"],
            3: ["Optimización de procesos", "Ingeniería de materiales", "Biotecnología"],
            4: ["Inteligencia artificial", "Desarrollo de software", "Seguridad informática"],
            5: ["Pedagogía virtual", "Aprendizaje basado en proyectos", "Competencias digitales"],
            6: ["Estudios culturales", "Responsabilidad social", "Impacto comunitario"],
            7: ["Lingüística aplicada", "Comunicación organizacional", "Análisis del discurso"],
            8: ["Gestión del conocimiento", "Sistemas de información", "Aprendizaje organizacional"]
        }

        # Convertir grupo_id a entero si es necesario
        if isinstance(grupo_id, str) and grupo_id.isdigit():
            grupo_id = int(grupo_id)

        return lineas_por_grupo.get(grupo_id, ["No hay líneas de investigación registradas"])
