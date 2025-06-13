from ui.prompts import (
    mostrar_lista_grupos, mostrar_detalles_grupo, solicitar_id_grupo,
    mostrar_lista_semilleros, mostrar_detalles_semillero, solicitar_id_semillero,
    solicitar_datos_semillero
)
from models.semillero import Semillero
from models.entregable import Entregable
import time
import json


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
            print("4. Asignar semillero a grupo investigador")
            print("5. Asignar entregable a semillero")
            print("6. Ver entregable de semillero")
            print("7. Activar semillero")
            print("8. Aprobar/Denegar entregable")
            print("9. Ver lista de entregables")
            print("10. Gestionar tutores y estudiantes")
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
                self._asignar_semillero()
            elif opcion == "5":
                self._asignar_entregable()    
            elif opcion == "6":
                self._ver_entregable_semillero()
            elif opcion == "7":
                self._activar_semillero()
            elif opcion == "8":
                self._aprobar_denegar_entregable()
            elif opcion == "9":
                self._ver_lista_entregables()
            elif opcion == "10":
                self._menu_investigadores()
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
        respuesta = input("\nSi desea eliminar un semillero presione 'D',\n Si desea Editar un semillero Precione 'E'\n de lo contrario presione Enter para continuar: ").strip().lower()


        # Si elige Enter, no hace nada y regresa
        if respuesta == "":
            print("No se realizó ninguna acción.")
            input("\nPresione Enter para continuar...")
            return True

        # Validar que la opción sea 'd' o 'e'
        if respuesta not in ('d', 'e'):
            print("Opción inválida. Solo 'D' para eliminar, 'E' para editar o Enter para cancelar.")
            input("\nPresione Enter para continuar...")
            return True

        # Pedir el ID del semillero a procesar
        id_texto = input("Digite el identificador del semillero: ").strip()
        try:
            sem_id = int(id_texto)
        except ValueError:
            print("Debe ingresar un número válido.")
            input("\nPresione Enter para continuar...")
            return True

        # Verificar que exista en semilleros_validos
        sem_obj = None
        for s in semilleros_validos:
            if s.id == sem_id:
                sem_obj = s
                break

        if sem_obj is None:
            print(f"No existe ningún semillero con ID = {sem_id}.")
            input("\nPresione Enter para continuar...")
            return True

        # Si la opción es 'd' → ELIMINAR
        if respuesta == 'd':
            confirmar_del = input(
                f"¿Está seguro de que desea eliminar el semillero "
                f"'{sem_obj.nombre}' (ID {sem_id})? (S/N): "
            ).strip().lower()
            if confirmar_del != 's':
                print("Eliminación cancelada.")
                input("\nPresione Enter para continuar...")
                return True

            print("Procediendo a eliminar el semillero...")
            exito = False
            exito = self.semillero_service.eliminar_semillero(sem_id)
            if exito:
                print("No se eliminó ningún semillero.")
            else:
                print(f"El semillero '{sem_obj.nombre}' (ID {sem_id}) fue eliminado correctamente.")

            input("\nPresione Enter para continuar...")
            return True

        # Si la opción es 'e' → EDITAR
        if respuesta == 'e':
            print(f"\n=== EDITAR SEMILLERO (ID {sem_id}) ===")
            print("Si deja un campo vacío, se mantendrá el valor anterior.\n")

            # 1) Nuevo nombre
            nuevo_nombre = input(f"Nuevo nombre (actual: '{sem_obj.nombre}'): ").strip()
            if nuevo_nombre == "":
                nuevo_nombre = sem_obj.nombre

            # 2) Nuevo objetivo principal
            nuevo_objetivo_principal = input(
                f"Nuevo objetivo principal (actual: '{sem_obj.objetivo_principal}'): "
            ).strip()
            if nuevo_objetivo_principal == "":
                nuevo_objetivo_principal = sem_obj.objetivo_principal

            # 3) Nuevos objetivos específicos (JSON)
            objetivos_actuales_json = json.dumps(sem_obj.objetivos_especificos)
            nuevos_objetivos_input = input(
                f"Nuevos objetivos específicos en JSON (actual: {objetivos_actuales_json}): "
            ).strip()
            if nuevos_objetivos_input == "":
                objetivos_json = objetivos_actuales_json
            else:
                try:
                    # Validar que sea JSON válido
                    lista_obj = json.loads(nuevos_objetivos_input)
                    objetivos_json = nuevos_objetivos_input
                except Exception:
                    print("JSON inválido para objetivos específicos. Se mantendrán los anteriores.")
                    objetivos_json = objetivos_actuales_json

            # 4) Nuevo grupo (ID)
            grupo_actual = sem_obj.grupo_id
            nuevo_grupo_input = input(f"Nuevo grupo_id (actual: {grupo_actual}): ").strip()
            if nuevo_grupo_input == "":
                grupo_id_final = grupo_actual
            else:
                try:
                    posible_grupo = int(nuevo_grupo_input)
                    # Validar que el grupo exista
                    if not self.grupo_service.obtener_por_id(posible_grupo):
                        print(f"Grupo con ID {posible_grupo} no existe. Se mantiene el anterior ({grupo_actual}).")
                        grupo_id_final = grupo_actual
                    else:
                        grupo_id_final = posible_grupo
                except ValueError:
                    print("ID de grupo inválido. Se mantiene el anterior.")
                    grupo_id_final = grupo_actual

            # 5) Nuevo status
#            status_actual = sem_obj.status
#            nuevo_status_input = input(f"Nuevo status (actual: '{status_actual}'): ").strip().lower()
#            if nuevo_status_input == "":
#                status_final = status_actual
#            else:
#                if nuevo_status_input not in ("activo", "pendiente"):
#                    print("Status inválido. Se mantiene el anterior.")
#                    status_final = status_actual
#                else:
#                    status_final = nuevo_status_input

            # 6) Llamar al servicio para editar
            print("\nGuardando cambios...")
            try:
                exito_editar = self.semillero_service.editar_semillero(
                    sem_id,
                    nuevo_nombre,
                    nuevo_objetivo_principal,
                    json.loads(objetivos_json),
                    grupo_id_final,
#                    status_final
                )
            except Exception as e:
                print(f"Error interno al intentar editar: {e}")
                exito_editar = False
            print("Semillero actualizado correctamente.")

            input("\nPresione Enter para continuar...")
            return True

        # (No hace falta otro else, porque ya cubrimos '', 'd' y 'e')
        input("\nPresione Enter para continuar...")
        return True
    
    def _eliminar_semillero(self):
        """ Permite al usuario seleccionar un semillero (por ID) y eliminarlo """
        semilleros = self.semillero_service.obtener_todos()
        if not semilleros:
            print("\nNo hay semilleros registrados en el sistema.")
            input("\nPresione Enter para continuar...")
            return False

        # (Opcional) Solo mostrar semilleros activos/pendientes. Si quieres listar
        # todos, comenta la siguiente línea:
        semilleros = [s for s in semilleros if s.status in ["activo", "pendiente"]]

        if not semilleros:
            print("\nNo hay semilleros activos o pendientes para eliminar.")
            input("\nPresione Enter para continuar...")
            return False

        # Mostrar tabla con semilleros y su ID
        print("\n=== ELIMINAR SEMILLERO ===")
        print(f"{'ID':<5} {'NOMBRE':<30} {'ESTADO':<10} {'GRUPO':<20}")
        print("-" * 70)
        for sem in semilleros:
            grupo = self.grupo_service.obtener_por_id(sem.grupo_id)
            grupo_nombre = grupo.nombre if grupo else "Grupo no encontrado"
            estado = sem.status.upper()
            print(f"{sem.semillero_id:<5} {sem.nombre:<30} {estado:<10} {grupo_nombre:<20}")
        print("-" * 70)

        # Pedir al usuario el ID a eliminar (o Enter para volver)
        seleccionado = input("\nSeleccione un semillero para eliminar o presione Enter para volver al menú principal: ").strip()
        if seleccionado == '':
            # El usuario decidió no borrar nada
            return False

        # Validar que exista un número entero
        try:
            sem_id = int(seleccionado)
        except ValueError:
            print("Debe ingresar un número válido.")
            input("\nPresione Enter para continuar...")
            return False

        # Verificar que el ID exista en la lista
        semillero_obj = None
        for s in semilleros:
            if s.id == sem_id:
                semillero_obj = s
                break

        if semillero_obj is None:
            print(f"No existe ningún semillero con ID = {sem_id}.")
            input("\nPresione Enter para continuar...")
            return False

        # Pedir confirmación
        confirmar = input(f"¿Está seguro de que desea eliminar el semillero '{semillero_obj.nombre}' (ID {sem_id})? (S/N): ").strip().lower()
        if confirmar != 's':
            print("Operación cancelada.")
            input("\nPresione Enter para continuar...")
            return False

        # Llamar al servicio para eliminar
        exito = self.semillero_service.eliminar_semillero(sem_id)
        if exito==True:
            print(f"El semillero '{semillero_obj.nombre}' (ID {sem_id}) fue eliminado correctamente.")
        else:
            print(f"Ocurrió un error al intentar eliminar el semillero con ID {sem_id}.")
        input("\nPresione Enter para continuar...")
        return exito

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


    def _asignar_semillero(self):
        grupos = self.grupo_service.obtener_todos()
        print("--->ESTOS SON LOS GRUPOS DISPONIBLES<---")
        for g in grupos:
         print(
        f"Grupo #{g.id}:\n"
        f"  • Nombre:           {g.nombre}\n"
        f"  • Identificador   :{g.identificador}\n"
        f"  • Campo:            {g.campo}\n"
        f"  • Director:         {g.director}\n"
         )

        while True:
            try:
                grupo_identificador = input("Ingrese el Identificador del grupo al que desea asignar un semillero: ")
                grupo = self.grupo_service.obtener_por_identificador(grupo_identificador)
                print(f"\nBuscando grupo con identificador: {grupo_identificador}")
                if not grupo_identificador:
                    print("Identificador no puede estar vacío. Intente de nuevo.")
                    continue
                if grupo:
                    print(f"\nGrupo seleccionado: (Nombre: {grupo.nombre} ID: {grupo.id})")
                    print("Ahora Selecciona el semillero que desea asignar al grupo")
                    time.sleep(4)
                    semilleros = self.grupo_service.obtener_semilleros()
                    if not semilleros:
                        print("\nNo hay semilleros registrados.")
                        input("\nPresione Enter para continuar...")
                        return  
                    break
                else:
                    print("Grupo no encontrado. Intente de nuevo.")
            except ValueError:
                print("ID inválido. Intente de nuevo.")

  
    
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

    def _activar_semillero(self):
        """Activa un semillero si su entregable ha sido aprobado"""
        # Mostrar lista de semilleros pendientes
        semilleros = [s for s in self.semillero_service.obtener_todos() if s.status == "pendiente"]

        if not semilleros:
            print("\nNo hay semilleros pendientes de activación.")
            input("\nPresione Enter para continuar...")
            return

        print("\n=== SEMILLEROS PENDIENTES DE ACTIVACIÓN ===")
        for semillero in semilleros:
            print(f"\nID: {semillero.id}")
            print(f"Nombre: {semillero.nombre}")
            print(f"Grupo: {semillero.grupo_nombre}")
            print("-" * 40)

        try:
            semillero_id = int(input("\nIngrese el ID del semillero a activar (0 para cancelar): "))
            if semillero_id == 0:
                return

            # Verificar si el semillero existe y está pendiente
            semillero = next((s for s in semilleros if s.id == semillero_id), None)
            if not semillero:
                print("\nID de semillero no válido o el semillero ya está activo.")
                input("\nPresione Enter para continuar...")
                return

            # Intentar activar el semillero
            if self.semillero_service.activar_semillero(semillero_id):
                print(f"\nEl semillero '{semillero.nombre}' ha sido activado exitosamente.")
            else:
                print("\nNo se pudo activar el semillero. Asegúrese de que el entregable esté aprobado.")

        except ValueError:
            print("\nPor favor, ingrese un número válido.")

        input("\nPresione Enter para continuar...")

    def _aprobar_denegar_entregable(self):
        """Permite aprobar o denegar un entregable de un semillero"""
        semilleros = self.semillero_service.obtener_todos()

        if not semilleros:
            print("\nNo hay semilleros registrados.")
            input("\nPresione Enter para continuar...")
            return

        print("\n=== APROBAR/DENEGAR ENTREGABLE ===")
        print("\nSemilleros disponibles:")
        for i, semillero in enumerate(semilleros, 1):
            print(f"{i}. {semillero.nombre}")

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
        entregable = self.entregable_service.obtener_por_semillero(semillero_seleccionado.id)

        if not entregable:
            print(f"\nEl semillero {semillero_seleccionado.nombre} no tiene entregables asignados.")
            input("\nPresione Enter para continuar...")
            return

        print(f"\nEntregable actual: {entregable.titulo}")
        print(f"Estado actual: {entregable.estado.upper()}")
        print("\nAcciones disponibles:")
        print("1. Aprobar entregable")
        print("2. Denegar entregable")
        print("3. Cancelar")

        try:
            accion = int(input("\nSeleccione una acción: "))
            if accion == 1:
                resultado, mensaje = self.entregable_service.aprobar_denegar_entregable(entregable.id, True)
            elif accion == 2:
                resultado, mensaje = self.entregable_service.aprobar_denegar_entregable(entregable.id, False)
            elif accion == 3:
                return
            else:
                print("\nOpción inválida.")
                input("\nPresione Enter para continuar...")
                return

            print(f"\n{mensaje}")

        except ValueError:
            print("\nOpción inválida.")

        input("\nPresione Enter para continuar...")

    def _ver_lista_entregables(self):
        """Muestra la lista completa de entregables y sus semilleros asociados"""
        entregables = self.entregable_service.obtener_todos()

        if not entregables:
            print("\nNo hay entregables registrados en el sistema.")
            input("\nPresione Enter para continuar...")
            return

        print("\n=== LISTA DE ENTREGABLES ===")
        print(f"{'ID':<5} {'TÍTULO':<30} {'TIPO':<20} {'ESTADO':<12} {'SEMILLERO':<25}")
        print("-" * 92)

        for entregable in entregables:
            print(f"{entregable.id:<5} {entregable.titulo[:28]+'...' if len(entregable.titulo) > 28 else entregable.titulo:<30} "
                  f"{entregable.tipo[:18]+'...' if len(entregable.tipo) > 18 else entregable.tipo:<20} "
                  f"{entregable.estado.upper():<12} "
                  f"{entregable.semillero_nombre[:23]+'...' if len(entregable.semillero_nombre or '') > 23 else (entregable.semillero_nombre or 'Sin semillero'):<25}")

        print("-" * 92)
        print(f"Total de entregables: {len(entregables)}")

        # Opción para ver detalles de un entregable específico
        ver_detalles = input("\n¿Desea ver los detalles de algún entregable? (S/N): ").strip().lower()
        if ver_detalles == 's':
            try:
                entregable_id = int(input("Ingrese el ID del entregable: "))
                entregable = next((e for e in entregables if e.id == entregable_id), None)
                if entregable:
                    print("\n" + "=" * 50)
                    print(entregable.detalles())
                    print("=" * 50)
                else:
                    print("\nNo se encontró el entregable con ese ID.")
            except ValueError:
                print("\nID inválido.")

        input("\nPresione Enter para continuar...")

    def _menu_investigadores(self):
        """Submenú para gestionar tutores y estudiantes"""
        while True:
            print("\n==== GESTIÓN DE INVESTIGADORES ====")
            print("1. Ver lista de tutores")
            print("2. Ver lista de estudiantes")
            print("3. Agregar tutor")
            print("4. Agregar estudiante")
            print("5. Asignar tutor a semillero")
            print("6. Asignar estudiante a semillero")
            print("0. Volver al menú anterior")
            print("=" * 45)

            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                self._listar_tutores()
            elif opcion == "2":
                self._listar_estudiantes()
            elif opcion == "3":
                self._agregar_tutor()
            elif opcion == "4":
                self._agregar_estudiante()
            elif opcion == "5":
                self._asignar_tutor_semillero()
            elif opcion == "6":
                self._asignar_estudiante_semillero()
            elif opcion == "0":
                break
            else:
                print("Opción no válida. Intente de nuevo.")

    def _listar_tutores(self):
        """Muestra la lista de todos los tutores registrados"""
        tutores = self.semillero_service.obtener_tutores()

        if not tutores:
            print("\nNo hay tutores registrados en el sistema.")
            input("\nPresione Enter para continuar...")
            return

        print("\n=== LISTA DE TUTORES ===")
        print(f"{'ID':<5} {'NOMBRE':<30} {'EMAIL':<30} {'SEMILLERO':<20}")
        print("-" * 85)

        for tutor in tutores:
            semillero = self.semillero_service.obtener_por_id(tutor.semillero_id) if tutor.semillero_id else None
            semillero_nombre = semillero.nombre if semillero else "No asignado"
            print(f"{tutor.id:<5} {tutor.nombre:<30} {tutor.email:<30} {semillero_nombre:<20}")

        print("-" * 85)
        print(f"Total de tutores: {len(tutores)}")
        input("\nPresione Enter para continuar...")

    def _listar_estudiantes(self):
        """Muestra la lista de todos los estudiantes registrados"""
        estudiantes = self.semillero_service.obtener_estudiantes()

        if not estudiantes:
            print("\nNo hay estudiantes registrados en el sistema.")
            input("\nPresione Enter para continuar...")
            return

        print("\n=== LISTA DE ESTUDIANTES ===")
        print(f"{'ID':<5} {'NOMBRE':<30} {'EMAIL':<30} {'SEMILLERO':<20}")
        print("-" * 85)

        for estudiante in estudiantes:
            semillero = self.semillero_service.obtener_por_id(estudiante.semillero_id) if estudiante.semillero_id else None
            semillero_nombre = semillero.nombre if semillero else "No asignado"
            print(f"{estudiante.id:<5} {estudiante.nombre:<30} {estudiante.email:<30} {semillero_nombre:<20}")

        print("-" * 85)
        print(f"Total de estudiantes: {len(estudiantes)}")
        input("\nPresione Enter para continuar...")

    def _agregar_tutor(self):
        """Agrega un nuevo tutor al sistema"""
        print("\n=== AGREGAR NUEVO TUTOR ===")
        nombre = input("Nombre del tutor: ").strip()
        if not nombre:
            print("El nombre es obligatorio.")
            input("\nPresione Enter para continuar...")
            return

        email = input("Email del tutor: ").strip()

        tutor = Investigador(
            nombre=nombre,
            tipo="tutor",
            email=email
        )

        resultado, mensaje = self.semillero_service.agregar_investigador(tutor)
        print(f"\n{mensaje}")
        input("\nPresione Enter para continuar...")

    def _agregar_estudiante(self):
        """Agrega un nuevo estudiante al sistema"""
        print("\n=== AGREGAR NUEVO ESTUDIANTE ===")
        nombre = input("Nombre del estudiante: ").strip()
        if not nombre:
            print("El nombre es obligatorio.")
            input("\nPresione Enter para continuar...")
            return

        email = input("Email del estudiante: ").strip()

        estudiante = Investigador(
            nombre=nombre,
            tipo="estudiante",
            email=email
        )

        resultado, mensaje = self.semillero_service.agregar_investigador(estudiante)
        print(f"\n{mensaje}")
        input("\nPresione Enter para continuar...")

    def _asignar_tutor_semillero(self):
        """Asigna un tutor a un semillero"""
        # Mostrar lista de tutores disponibles
        tutores = self.semillero_service.obtener_tutores()
        if not tutores:
            print("\nNo hay tutores disponibles para asignar.")
            input("\nPresione Enter para continuar...")
            return

        print("\n=== TUTORES DISPONIBLES ===")
        for tutor in tutores:
            print(f"ID: {tutor.id} - {tutor.nombre}")

        try:
            tutor_id = int(input("\nSeleccione el ID del tutor: "))
            tutor = next((t for t in tutores if t.id == tutor_id), None)
            if not tutor:
                print("Tutor no encontrado.")
                input("\nPresione Enter para continuar...")
                return
        except ValueError:
            print("ID inválido.")
            input("\nPresione Enter para continuar...")
            return

        # Mostrar semilleros disponibles
        semilleros = self.semillero_service.obtener_todos()
        if not semilleros:
            print("\nNo hay semilleros disponibles.")
            input("\nPresione Enter para continuar...")
            return

        print("\n=== SEMILLEROS DISPONIBLES ===")
        for semillero in semilleros:
            print(f"ID: {semillero.id} - {semillero.nombre}")

        try:
            semillero_id = int(input("\nSeleccione el ID del semillero: "))
            if not any(s.id == semillero_id for s in semilleros):
                print("Semillero no encontrado.")
                input("\nPresione Enter para continuar...")
                return
        except ValueError:
            print("ID inválido.")
            input("\nPresione Enter para continuar...")
            return

        resultado, mensaje = self.semillero_service.asignar_investigador_semillero(tutor_id, semillero_id)
        print(f"\n{mensaje}")
        input("\nPresione Enter para continuar...")

    def _asignar_estudiante_semillero(self):
        """Asigna un estudiante a un semillero"""
        # Mostrar lista de estudiantes disponibles
        estudiantes = self.semillero_service.obtener_estudiantes()
        if not estudiantes:
            print("\nNo hay estudiantes disponibles para asignar.")
            input("\nPresione Enter para continuar...")
            return

        print("\n=== ESTUDIANTES DISPONIBLES ===")
        for estudiante in estudiantes:
            print(f"ID: {estudiante.id} - {estudiante.nombre}")

        try:
            estudiante_id = int(input("\nSeleccione el ID del estudiante: "))
            estudiante = next((e for e in estudiantes if e.id == estudiante_id), None)
            if not estudiante:
                print("Estudiante no encontrado.")
                input("\nPresione Enter para continuar...")
                return
        except ValueError:
            print("ID inválido.")
            input("\nPresione Enter para continuar...")
            return

        # Mostrar semilleros disponibles
        semilleros = self.semillero_service.obtener_todos()
        if not semilleros:
            print("\nNo hay semilleros disponibles.")
            input("\nPresione Enter para continuar...")
            return

        print("\n=== SEMILLEROS DISPONIBLES ===")
        for semillero in semilleros:
            print(f"ID: {semillero.id} - {semillero.nombre}")

        try:
            semillero_id = int(input("\nSeleccione el ID del semillero: "))
            if not any(s.id == semillero_id for s in semilleros):
                print("Semillero no encontrado.")
                input("\nPresione Enter para continuar...")
                return
        except ValueError:
            print("ID inválido.")
            input("\nPresione Enter para continuar...")
            return

        resultado, mensaje = self.semillero_service.asignar_investigador_semillero(estudiante_id, semillero_id)
