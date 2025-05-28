def mostrar_lista_grupos(grupos):
    """Muestra una lista de grupos de investigación"""
    if not grupos:
        print("\nNo hay grupos de investigación registrados.")
        return False

    print("\n==== GRUPOS DE INVESTIGACIÓN DISPONIBLES ====")
    for grupo in grupos:
        print(f"{grupo.id}. {grupo.nombre}")
    print("=" * 45)

    return True


def mostrar_detalles_grupo(grupo):
    """Muestra los detalles completos de un grupo de investigación"""
    if not grupo:
        print("\nNo se encontró el grupo solicitado")
        return False

    # Mostrar información detallada
    print("\n" + "=" * 50)
    print("DETALLES DEL GRUPO DE INVESTIGACIÓN")
    print("=" * 50)
    print(f"NOMBRE: {grupo.nombre}")
    print(f"CAMPO: {grupo.campo}")
    print(f"IDENTIFICADOR: {grupo.identificador}")
    print(f"DIRECTOR: {grupo.director}")
    print("=" * 50)

    return True


def solicitar_id_grupo():
    """Solicita al usuario el ID de un grupo"""
    try:
        grupo_id = int(input("\nIngrese el ID del grupo: "))
        return grupo_id
    except ValueError:
        print("Error: Debe ingresar un número válido.")
        return None


def mostrar_lista_semilleros(semilleros):
    """Función auxiliar para mostrar la lista de semilleros"""
    if not semilleros:
        print("\nNo hay semilleros disponibles.")
        input("\nPresione Enter para continuar...")
        return False

    print("\n=== LISTA DE SEMILLEROS ===")
    print(f"{'ID':<5} {'NOMBRE':<30} {'ESTADO':<10}")
    print("-" * 50)

    for semillero in semilleros:
        estado = semillero.status.upper()
        print(f"{semillero.id:<5} {semillero.nombre:<30} {estado:<10}")

    print("-" * 50)
    input("\nPresione Enter para continuar...")
    return True


def mostrar_detalles_semillero(semillero):
    """Muestra los detalles completos de un semillero"""
    if not semillero:
        print("\nNo se encontró el semillero solicitado")
        return False

    # Mostrar información detallada
    print("\n" + "=" * 60)
    print("DETALLES DEL SEMILLERO DE INVESTIGACIÓN")
    print("=" * 60)
    print(semillero.detalles())
    print("=" * 60)

    return True


def solicitar_id_semillero():
    """Solicita al usuario el ID de un semillero"""
    try:
        semillero_id = int(input("\nIngrese el ID del semillero: "))
        return semillero_id
    except ValueError:
        print("Error: Debe ingresar un número válido.")
        return None


def solicitar_datos_semillero(grupos, lineas_investigacion=None):
    """Solicita al usuario los datos para crear un nuevo semillero

    Args:
        grupos (list): Lista de grupos de investigación disponibles
        lineas_investigacion (list, optional): Lista de líneas de investigación del grupo seleccionado

    Returns:
        dict: Diccionario con los datos del semillero o None si se cancela
    """
    print("\n==== CREAR NUEVO SEMILLERO ====")

    nombre = input("Nombre del semillero: ").strip()
    if not nombre:
        print("El nombre es obligatorio.")
        return None

    # Mostrar grupos disponibles
    mostrar_lista_grupos(grupos)
    grupo_id = solicitar_id_grupo()
    if grupo_id is None:
        return None

    # Validar que el grupo exista
    grupo_valido = False
    for grupo in grupos:
        if grupo.id == grupo_id:
            grupo_valido = True
            break

    if not grupo_valido:
        print(f"El grupo con ID {grupo_id} no existe.")
        return None

    # Solicitar objetivo principal
    objetivo_principal = input("Objetivo principal del semillero: ").strip()
    if not objetivo_principal:
        print("El objetivo principal es obligatorio.")
        return None

    # Solicitar objetivos específicos
    print("\nObjetivos específicos (ingrese uno por línea, línea vacía para terminar):")
    objetivos_especificos = []

    # Si hay líneas de investigación disponibles, mostrarlas como sugerencia
    if lineas_investigacion:
        print("\nLíneas de investigación sugeridas del grupo seleccionado:")
        for i, linea in enumerate(lineas_investigacion, 1):
            print(f"{i}. {linea}")
        print("Puede usarlas como objetivos específicos o ingresar otros.")

    while True:
        objetivo = input("- ").strip()
        if not objetivo:
            break
        objetivos_especificos.append(objetivo)

    if not objetivos_especificos:
        print("Debe ingresar al menos un objetivo específico.")
        return None

    # Solicitar estudiantes (mínimo 2)
    print("\nEstudiantes del semillero (ingrese uno por línea, línea vacía para terminar):")
    print("Formato: Nombre, Email")
    estudiantes = []

    while True:
        estudiante_input = input("- ").strip()
        if not estudiante_input:
            if len(estudiantes) >= 2:
                break
            else:
                print(f"Debe ingresar al menos 2 estudiantes (actualmente: {len(estudiantes)})")
                continue

        # Parsear nombre y email
        partes = estudiante_input.split(',')
        nombre = partes[0].strip()
        email = partes[1].strip() if len(partes) > 1 else ""

        estudiantes.append({"nombre": nombre, "email": email})

    # Solicitar tutores (1 o 2)
    print("\nTutores del semillero (ingrese uno por línea, línea vacía para terminar):")
    print("Formato: Nombre, Email")
    tutores = []

    while True:
        tutor_input = input("- ").strip()
        if not tutor_input:
            if len(tutores) >= 1:
                break
            else:
                print("Debe ingresar al menos un tutor")
                continue

        if len(tutores) >= 2:
            print("Solo se permiten máximo 2 tutores")
            break

        # Parsear nombre y email
        partes = tutor_input.split(',')
        nombre = partes[0].strip()
        email = partes[1].strip() if len(partes) > 1 else ""

        tutores.append({"nombre": nombre, "email": email})

    # Todos los semilleros empiezan con estado "pendiente"
    status = "pendiente"

    return {
        "nombre": nombre,
        "objetivo_principal": objetivo_principal,
        "objetivos_especificos": objetivos_especificos,
        "grupo_id": grupo_id,
        "estudiantes": estudiantes,
        "tutores": tutores,
        "status": status
    }
