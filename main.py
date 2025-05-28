from db.database import Database
from services.grupo_service import GrupoService
from services.semillero_service import SemilleroService
from ui.menu import Menu
from services.entregable_service import EntregableService


def main():
    """Función principal del programa"""
    print("Bienvenido al Sistema de Gestión de Grupos y Semilleros de Investigación - Universidad EAN")

    # Inicializar la base de datos y servicios
    db = Database()
    grupo_service = GrupoService(db)
    semillero_service = SemilleroService(db)
    entregable_service = EntregableService(db)

    # Cargar datos iniciales de grupos
    grupos_cargados = grupo_service.cargar_datos_iniciales()
    if grupos_cargados > 0:
        print(f"Se han cargado {grupos_cargados} grupos de investigación.")
    else:
        print("Los datos de grupos ya están cargados en la base de datos.")

    # Iniciar la interfaz de usuario
    menu = Menu(grupo_service, semillero_service, entregable_service)
    menu.mostrar_menu()


if __name__ == "__main__":
    main()
