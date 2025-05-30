import unittest
from models.investigador import Investigador

class TestInvestigador(unittest.TestCase):
    def setUp(self):
        self.investigador = Investigador(
            id=1,
            nombre="Juan Pérez",
            tipo="estudiante",
            email="juan@test.com",
            semillero_id=1
        )

    def test_creacion_investigador(self):
        self.assertEqual(self.investigador.id, 1)
        self.assertEqual(self.investigador.nombre, "Juan Pérez")
        self.assertEqual(self.investigador.tipo, "estudiante")
        self.assertEqual(self.investigador.email, "juan@test.com")
        self.assertEqual(self.investigador.semillero_id, 1)

    def test_str_representation(self):
        expected_str = "Juan Pérez (juan@test.com)"
        self.assertEqual(str(self.investigador), expected_str)

    def test_tipo_investigador(self):
        investigador_tutor = Investigador(
            id=2,
            nombre="Dr. Smith",
            tipo="tutor",
            email="smith@test.com",
            semillero_id=1
        )
        self.assertEqual(investigador_tutor.tipo, "tutor")