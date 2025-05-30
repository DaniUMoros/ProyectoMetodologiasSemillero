import unittest
from models.grupo import Grupo

class TestGrupo(unittest.TestCase):
    def setUp(self):
        self.grupo = Grupo(
            id=1,
            nombre="Grupo de Investigación Test",
            campo="Ingeniería de Software",
            identificador="GIT-001",
            director="Dr. Test"
        )

    def test_creacion_grupo(self):
        self.assertEqual(self.grupo.id, 1)
        self.assertEqual(self.grupo.nombre, "Grupo de Investigación Test")
        self.assertEqual(self.grupo.campo, "Ingeniería de Software")
        self.assertEqual(self.grupo.identificador, "GIT-001")
        self.assertEqual(self.grupo.director, "Dr. Test")

    def test_actualizar_grupo(self):
        nuevo_nombre = "Nuevo Nombre del Grupo"
        self.grupo.nombre = nuevo_nombre
        self.assertEqual(self.grupo.nombre, nuevo_nombre)

    def test_str_representation(self):
        expected_str = "Grupo de Investigación Test - GIT-001"
        self.assertEqual(str(self.grupo), expected_str)

    def test_detalles(self):
        detalles = self.grupo.detalles()
        self.assertIn("NOMBRE: Grupo de Investigación Test", detalles)
        self.assertIn("CAMPO: Ingeniería de Software", detalles)
        self.assertIn("IDENTIFICADOR: GIT-001", detalles)
        self.assertIn("DIRECTOR: Dr. Test", detalles)