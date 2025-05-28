from ui.prompts import (
    mostrar_lista_grupos, mostrar_detalles_grupo, solicitar_id_grupo,
    mostrar_lista_semilleros, mostrar_detalles_semillero, solicitar_id_semillero,
    solicitar_datos_semillero
)
from models.semillero import Semillero
from models.entregable import Entregable


class Menu:
    """Menú principal de la aplicación"""

    def __init__(self, grupo_service, semillero_service, entregable_service):
        self.grupo_service = grupo_service
        self.semillero_service = semillero_service
        self.entregable_service = entregable_service

    def mostrar_menu(self):
        """Muestra el menú principal de la aplicación"""
        while True:
            print("\n==== SISTEMA DE GESTIÓN DE GRUPOS DE INVESTIGACIÓN ====")
            print("1. Gestionar Grupos de Investigación")
            print("2. Gestionar Semilleros de Investigación")
            print("0. Salir")
            print("=" * 56)

            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                self._menu_grupos()
            elif opcion == "2":
                self._menu_semilleros()
            elif opcion == "0":
                print("Gracias por usar el sistema. ¡Hasta pronto!")
                break
            else:
                print("Opción no válida. Intente de nuevo.")

    def _menu_grupos(self):
        """Submenú para gestionar grupos de investigación"""
        while True:
            print("\n==== GESTIÓN DE GRUPOS DE INVESTIGACIÓN ====")
            print("1. Listar todos los grupos")
            print("2. Ver detalles de un grupo")
            print("3. Ver semilleros de un grupo")
            print("0. Volver al menú principal")
            print("=" * 45)

            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                self._listar_grupos()
            elif opcion == "2":
                self._ver_detalles_grupo()
            elif opcion == "3":
                self._ver_semilleros_grupo()
            elif opcion == "0":
                break
            else:
                print("Opción no válida. Intente de nuevo.")

    def _menu_semilleros(self):
        """Submenú para gestionar semilleros de investigación"""
        while True:
            print("\n==== GESTIÓN DE SEMILLEROS DE INVESTIGACIÓN ====")
            print("1. Crear nuevo semillero")
            print("2. Ver todos los semilleros")
            print("3. Buscar semillero")
            print("4. Asignar entregable a semillero")
            print("5. Ver entregable de semillero")
            print("0. Volver al menú principal")
            print("=" * 45)

            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                self._crear_semillero()
            elif opcion == "2":
                self._listar_semilleros()
            elif opcion == "3":
                self._ver_detalles_semillero()
            elif opcion == "4":
                self._asignar_entregable()
            elif opcion == "5":
                self._ver_entregable_semillero()
            elif opcion == "0":
                break
            else:
                print("Opción no válida. Intente de nuevo.")

    def _listar_grupos(self):
        """Muestra la lista de todos los grupos disponibles"""
        grupos = self.grupo_service.obtener_todos()
        mostrar_lista_grupos(grupos)

    def _ver_detalles_grupo(self):
        """Permite seleccionar y ver los detalles de un grupo"""
        grupos = self.grupo_service.obtener_todos()
        if mostrar_lista_grupos(grupos):
            grupo_id = solicitar_id_grupo()
            if grupo_id is not None:
                grupo = self.grupo_service.obtener_por_id(grupo_id)
                mostrar_detalles_grupo(grupo)

    def _ver_semilleros_grupo(self):
        """Muestra los semilleros asociados a un grupo"""
        grupos = self.grupo_service.obtener_todos()
        if mostrar_lista_grupos(grupos):
            grupo_id = solicitar_id_grupo()
            if grupo_id is not None:
                semilleros = self.semillero_service.obtener_por_grupo(grupo_id)
                if not mostrar_lista_semilleros(semilleros):
                    print(f"El grupo seleccionado no tiene semilleros asociados.")

    def _listar_semilleros(self):
        """Muestra la lista de todos los semilleros disponibles (activos y pendientes)"""
        # Obtener todos los semilleros
        semilleros = self.semillero_service.obtener_todos()

        if not semilleros:
            print("\nNo hay semilleros registrados en el sistema.")
            input("\nPresione Enter para continuar...")
            return False

        # Filtrar semilleros activos y pendientes
        semilleros_validos = [s for s in semilleros if s.status in ["activo", "pendiente"]]

        if not semilleros_validos:
            print("\nNo hay semilleros activos o pendientes en el sistema.")
            input("\nPresione Enter para continuar...")
            return False

        print("\n=== LISTA DE SEMILLEROS ===")
        print(f"{'ID':<5} {'NOMBRE':<30} {'ESTADO':<10} {'GRUPO':<20}")
        print("-" * 70)

        for semillero in semilleros_validos:
            # Obtener nombre del grupo asociado
            grupo = self.grupo_service.obtener_por_id(semillero.grupo_id)
            grupo_nombre = grupo.nombre if grupo else "Grupo no encontrado"

            estado = semillero.status.upper()
            print(f"{semillero.id:<5} {semillero.nombre:<30} {estado:<10} {grupo_nombre:<20}")

        print("-" * 70)
        print(f"Total de semilleros: {len(semilleros_validos)}")
        input("\nPresione Enter para continuar...")
        return True

    def _ver_detalles_semillero(self):
        """Permite seleccionar y ver los detalles de un semillero"""
        semilleros = self.semillero_service.obtener_todos()
        if mostrar_lista_semilleros(semilleros):
            semillero_id = solicitar_id_semillero()
            if semillero_id is not None:
                semillero = self.semillero_service.obtener_por_id(semillero_id)
                mostrar_detalles_semillero(semillero)

    def _crear_semillero(self):
        """Permite crear un nuevo semillero"""
        # Obtener los grupos disponibles
        grupos = self.grupo_service.obtener_todos()
        if not grupos:
            print("No hay grupos de investigación disponibles para asociar el semillero.")
            return

        # Solicitar los datos del semillero
        datos = solicitar_datos_semillero(grupos)
        if not datos:
            return

        # Obtener líneas de investigación para el grupo seleccionado
        lineas = self.grupo_service.obtener_lineas_investigacion(datos["grupo_id"])
        if lineas:
            print("\nLíneas de investigación del grupo seleccionado:")
            for i, linea in enumerate(lineas, 1):
                print(f"{i}. {linea}")

            # Preguntar si quiere usar alguna línea como objetivo
            usar_linea = input("\n¿Desea añadir alguna línea como objetivo específico? (s/n): ").lower() == 's'
            if usar_linea:
                try:
                    indice = int(input("Ingrese el número de la línea a añadir: "))
                    if 1 <= indice <= len(lineas):
                        datos["objetivos_especificos"].append(lineas[indice - 1])
                        print(f"Línea añadida como objetivo específico: {lineas[indice - 1]}")
                except ValueError:
                    print("Número inválido, continuando sin añadir línea.")

        # Crear el objeto Semillero
        semillero = Semillero(
            nombre=datos["nombre"],
            objetivo_principal=datos["objetivo_principal"],
            objetivos_especificos=datos["objetivos_especificos"],
            grupo_id=datos["grupo_id"],
            status=datos["status"]
        )

        # Asignar estudiantes y tutores
        semillero.estudiantes = datos["estudiantes"]
        semillero.tutores = datos["tutores"]

        # Guardar el semillero
        semillero_id, errores = self.semillero_service.crear_semillero(semillero)

        if semillero_id:
            print(f"\n¡Semillero '{datos['nombre']}' creado correctamente!")
            semillero = self.semillero_service.obtener_por_id(semillero_id)
            mostrar_detalles_semillero(semillero)
        else:
            print("\nError al crear el semillero:")
            for error in errores:
                print(f"- {error}")

    def _cambiar_estado_semillero(self):
        """Permite cambiar el estado de un semillero"""
        semilleros = self.semillero_service.obtener_todos()
        if mostrar_lista_semilleros(semilleros):
            semillero_id = solicitar_id_semillero()
            if semillero_id is None:
                return

            semillero = self.semillero_service.obtener_por_id(semillero_id)
            if not semillero:
                print("Semillero no encontrado.")
                return

            estado_actual = "activo" if semillero.status == "activo" else "pendiente"
            print(f"\nEl estado actual del semillero es: {estado_actual.upper()}")

            nuevo_estado = "pendiente" if estado_actual == "activo" else "activo"
            confirmacion = input(f"¿Desea cambiar el estado a {nuevo_estado.upper()}? (s/n): ").lower() == 's'

            if confirmacion:
                if self.semillero_service.cambiar_status(semillero_id, nuevo_estado):
                    print(f"Estado del semillero actualizado a: {nuevo_estado.upper()}")
                else:
                    print("Error al actualizar el estado del semillero")

    def _asignar_entregable(self):
        """Asigna un entregable a un semillero"""
        semilleros = self.semillero_service.obtener_todos()

        if not semilleros:
            print("\nNo hay semilleros registrados.")
            input("\nPresione Enter para continuar...")
            return

        print("\n--- SEMILLEROS DISPONIBLES ---")
        for i, semillero in enumerate(semilleros, 1):
            print(f"{i}. {semillero}")

        try:
            opcion = int(input("\nSeleccione un semillero: ")) - 1
            if opcion < 0 or opcion >= len(semilleros):
                print("\nOpción inválida.")
                input("\nPresione Enter para continuar...")
                return
        except ValueError:
            print("\nOpción inválida.")
            input("\nPresione Enter para continuar...")
            return

        semillero_seleccionado = semilleros[opcion]

        # Verificar si ya tiene un entregable
        entregable_existente = self.entregable_service.obtener_por_semillero(semillero_seleccionado.id)
        if entregable_existente:
            print(f"\nEl semillero ya tiene un entregable asignado: {entregable_existente}")
            input("\nPresione Enter para continuar...")
            return

        print(f"\n--- ASIGNAR ENTREGABLE AL SEMILLERO: {semillero_seleccionado.nombre} ---")

        # Mostrar tipos de entregables disponibles
        print("\nTIPOS DE ENTREGABLES DISPONIBLES:")
        for i, tipo in enumerate(Entregable.TIPOS_VALIDOS, 1):
            print(f"{i}. {tipo}")

        try:
            tipo_opcion = int(input("\nSeleccione el tipo de entregable: ")) - 1
            if tipo_opcion < 0 or tipo_opcion >= len(Entregable.TIPOS_VALIDOS):
                print("\nOpción inválida.")
                input("\nPresione Enter para continuar...")
                return
        except ValueError:
            print("\nOpción inválida.")
            input("\nPresione Enter para continuar...")
            return

        tipo_seleccionado = Entregable.TIPOS_VALIDOS[tipo_opcion]

        titulo = input("\nTítulo del entregable: ")
        descripcion = input("Descripción: ")

        # Crear entregable
        entregable = Entregable(
            titulo=titulo,
            descripcion=descripcion,
            tipo=tipo_seleccionado,
            semillero_id=semillero_seleccionado.id
        )

        # Validar entregable
        errores = entregable.validar()
        if errores:
            print("\nERRORES EN EL ENTREGABLE:")
            for error in errores:
                print(f"- {error}")
            input("\nPresione Enter para continuar...")
            return

        # Guardar entregable
        resultado, mensaje = self.entregable_service.crear_entregable(entregable)

        print(f"\n{mensaje}")
        input("\nPresione Enter para continuar...")

    def _ver_entregable_semillero(self):
        """Muestra el entregable asociado a un semillero"""
        semilleros = self.semillero_service.obtener_todos()

        if not semilleros:
            print("\nNo hay semilleros registrados.")
            input("\nPresione Enter para continuar...")
            return

        print("\n--- SEMILLEROS DISPONIBLES ---")
        for i, semillero in enumerate(semilleros, 1):
            print(f"{i}. {semillero}")

        try:
            opcion = int(input("\nSeleccione un semillero: ")) - 1
            if opcion < 0 or opcion >= len(semilleros):
                print("\nOpción inválida.")
                input("\nPresione Enter para continuar...")
                return
        except ValueError:
            print("\nOpción inválida.")
            input("\nPresione Enter para continuar...")
            return

        semillero_seleccionado = semilleros[opcion]

        # Obtener entregable
        entregable = self.entregable_service.obtener_por_semillero(semillero_seleccionado.id)

        if not entregable:
            print(f"\nEl semillero {semillero_seleccionado.nombre} no tiene entregables asignados.")
        else:
            print(f"\n{entregable.detalles()}")

            # Si es el director, mostrar opción para cambiar estado
            if hasattr(self, 'rol') and self.rol == "director":
                print("\n¿Desea cambiar el estado del entregable?")
                print("1. Aprobar")
                print("2. Rechazar")
                print("3. Volver a pendiente")
                print("4. Cancelar")

                try:
                    estado_opcion = int(input("\nSeleccione una opción: "))
                    if estado_opcion == 1:
                        nuevo_estado = "aprobado"
                    elif estado_opcion == 2:
                        nuevo_estado = "rechazado"
                    elif estado_opcion == 3:
                        nuevo_estado = "pendiente"
                    else:
                        input("\nPresione Enter para continuar...")
                        return

                    resultado, mensaje = self.entregable_service.cambiar_estado(entregable.id, nuevo_estado)
                    print(f"\n{mensaje}")
                except ValueError:
                    print("\nOpción inválida.")

        input("\nPresione Enter para continuar...")
