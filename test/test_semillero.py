import unittest
from models.semillero import Semillero

class TestSemillero(unittest.TestCase):
    def setUp(self):
        self.semillero = Semillero(
            id=1,
            nombre="Semillero Test",
            objetivo_principal="Objetivo principal de prueba",
            objetivos_especificos=["Objetivo específico 1", "Objetivo específico 2"],
            grupo_id=1,
            status="pendiente"
        )

    def test_creacion_semillero(self):
        self.assertEqual(self.semillero.id, 1)
        self.assertEqual(self.semillero.nombre, "Semillero Test")
        self.assertEqual(self.semillero.objetivo_principal, "Objetivo principal de prueba")
        self.assertEqual(len(self.semillero.objetivos_especificos), 2)
        self.assertEqual(self.semillero.grupo_id, 1)
        self.assertEqual(self.semillero.status, "pendiente")

    def test_validacion_semillero_invalido(self):
        semillero_invalido = Semillero(
            id=1,
            nombre="",
            objetivo_principal="",
            objetivos_especificos=[],
            grupo_id=None
        )
        errores = semillero_invalido.validar()
        self.assertGreater(len(errores), 0)

    def test_detalles(self):
        detalles = self.semillero.detalles()
        self.assertIn("NOMBRE: Semillero Test", detalles)
        self.assertIn("ESTADO: PENDIENTE", detalles)
        self.assertIn("OBJETIVO PRINCIPAL: Objetivo principal de prueba", detalles)