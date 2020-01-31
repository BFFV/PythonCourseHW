import unittest

###############################################################################
"""
Tests
Acá escribe los test pedidos.
"""
class Testing(unittest.TestCase):

    def setUp(self):
        pass
        #self.Supermercado

    def test_codigo_invalido(self):
        self.assertRaises(ValueError, Supermercado.agregar_producto, ['@asd', Producto('pan', 100, 0.3)])

    def test_in(self):
        p = Producto('pan', 100, 0.3)
        self.assertRaises(KeyError, p in Supermercado.catalogo)

    def test_online(self):
        self.assertEqual(PedidoOnline(Supermercado).total, 0)
###############################################################################

if __name__ == '__main__':
    unittest.main()
