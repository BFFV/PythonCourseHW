import unittest
import structures as s
import functionalities as f
from entities import ElectricalOverload, ForbiddenAction, InvalidQuery, \
    Distribution, House


# Testing
class TestSystem(unittest.TestCase):

    def setUp(self):
        print('Comenzando Testing!')
        self.network = s.Container()
        for sys in s.Container('SING', 'SIC', 'AYSEN', 'MAGALLANES'):
            self.network.add(s.System(sys))

    def tearDown(self):
        print('Test Terminado!')

    # Consultas (se repite power_loss y largest_consumer)
    def test_Queries(self):
        result = s.Container(44642.53554080006, 3.923965258738392,
                             0.5262438971254364)
        self.assertEqual(f.testing_energy_by_commune(self.network, 'IQUIQUE'),
                         result)
        result = s.Container(1527, 'EL LOA', 'CALAMA')
        self.assertEqual(f.testing_largest_consumer(self.network, 'SING'),
                         result)
        result = s.Container(152, 'MELIPILLA', 'MELIPILLA')
        self.assertEqual(f.testing_largest_consumer(self.network, 'SIC'),
                         result)
        result = s.Container(57, 'CAPITAN PRAT', 'COCHRANE')
        self.assertEqual(f.testing_lowest_consumer(self.network, 'AYSEN'),
                         result)
        result = 4901.681580370846
        self.assertEqual(f.testing_power_loss(self.network, 1542),
                         result)
        result = 4565.596142401364
        self.assertEqual(f.testing_power_loss(self.network, 888),
                         result)
        result = 13.45124423996417
        self.assertEqual(f.testing_energy_by_substation(
            self.network, Distribution, 220), result)

    # Excepciones
    def test_Exceptions(self):
        with self.assertRaises(InvalidQuery):
            f.testing_energy_by_commune(self.network, 'NEW YORK')
        with self.assertRaises(ForbiddenAction):
            f.testing_delete_node(self.network, Distribution, 1542)
        with self.assertRaises(ElectricalOverload):
            f.testing_overload(self.network, House, 9999, 'AYSEN',
                               'province', 'AYSEN', 1000000, Distribution, 6, 1)


suite = unittest.TestLoader().loadTestsFromTestCase(TestSystem)
unittest.TextTestRunner().run(suite)
