import unittest
from models.semillero import Semillero
from models.investigador import Investigador

class TestSemillero(unittest.TestCase):
    def setUp(self):
        """Configuración inicial para cada prueba"""
        self.semillero = Semillero(
            id=1,
            nombre="Semillero de Prueba",
            objetivo_principal="Objetivo de prueba",
            objetivos_especificos=["Objetivo específico 1", "Objetivo específico 2"],
            grupo_id=1,
            status="pendiente"
        )

    def test_creacion_semillero(self):
        """Prueba la creación básica de un semillero"""
        self.assertEqual(self.semillero.id, 1)
        self.assertEqual(self.semillero.nombre, "Semillero de Prueba")
        self.assertEqual(self.semillero.objetivo_principal, "Objetivo de prueba")
        self.assertEqual(len(self.semillero.objetivos_especificos), 2)
        self.assertEqual(self.semillero.grupo_id, 1)
        self.assertEqual(self.semillero.status, "pendiente")

    def test_validacion_semillero_invalido(self):
        """Prueba la validación de un semillero inválido"""
        semillero_invalido = Semillero(
            id=1,
            nombre="",
            objetivo_principal="",
            objetivos_especificos=[],
            grupo_id=None
        )
        errores = semillero_invalido.validar()
        self.assertGreater(len(errores), 0)

    def test_agregar_tutor(self):
        """Prueba para agregar tutores al semillero"""
        # Crear tutores de prueba
        tutor1 = Investigador(id=1, nombre="Tutor 1", tipo="tutor", email="tutor1@test.com")
        tutor2 = Investigador(id=2, nombre="Tutor 2", tipo="tutor", email="tutor2@test.com")
        tutor3 = Investigador(id=3, nombre="Tutor 3", tipo="tutor", email="tutor3@test.com")

        # Probar agregar un tutor
        self.semillero.tutores.append(tutor1)
        self.assertEqual(len(self.semillero.tutores), 1)
        self.assertEqual(self.semillero.tutores[0].nombre, "Tutor 1")

        # Probar agregar un segundo tutor
        self.semillero.tutores.append(tutor2)
        self.assertEqual(len(self.semillero.tutores), 2)

        # Verificar que no se pueden agregar más de 2 tutores
        self.semillero.tutores.append(tutor3)
        errores = self.semillero.validar()
        self.assertTrue(any("tutores" in error.lower() for error in errores))

    def test_agregar_estudiante(self):
        """Prueba para agregar estudiantes al semillero"""
        # Crear estudiantes de prueba
        estudiante1 = Investigador(id=1, nombre="Estudiante 1", tipo="estudiante", email="est1@test.com")
        estudiante2 = Investigador(id=2, nombre="Estudiante 2", tipo="estudiante", email="est2@test.com")

        # Probar agregar estudiantes
        self.semillero.estudiantes.append(estudiante1)
        self.assertEqual(len(self.semillero.estudiantes), 1)

        self.semillero.estudiantes.append(estudiante2)
        self.assertEqual(len(self.semillero.estudiantes), 2)

        # Verificar que se requieren al menos 2 estudiantes
        self.semillero.estudiantes = [estudiante1]  # Solo un estudiante
        errores = self.semillero.validar()
        self.assertTrue(any("estudiantes" in error.lower() for error in errores))

    def test_cambio_estado_semillero(self):
        """Prueba para verificar el cambio de estado del semillero"""
        # Verificar estado inicial
        self.assertEqual(self.semillero.status, "pendiente")

        # Cambiar a activo
        self.semillero.status = "activo"
        self.assertEqual(self.semillero.status, "activo")

        # Cambiar de nuevo a pendiente
        self.semillero.status = "pendiente"
        self.assertEqual(self.semillero.status, "pendiente")

    def test_detalles_semillero(self):
        """Prueba la generación de detalles del semillero"""
        detalles = self.semillero.detalles()
        self.assertIn("NOMBRE: Semillero de Prueba", detalles)
        self.assertIn("ESTADO: PENDIENTE", detalles)
        self.assertIn("OBJETIVO PRINCIPAL: Objetivo de prueba", detalles)

if __name__ == '__main__':
    unittest.main()
