import os
import sys
from rdflib.graph import Graph
from rdflib import compare
import unittest
ruta_relativa = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'src'))
if ruta_relativa not in sys.path:
    sys.path.insert(0, ruta_relativa)
import ocp2kg

class TestRemoveDisjointPropertySH(unittest.TestCase):
    def test_remove_TransitiveProperty00(self):
        change_data = Graph().parse(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'changes_RemoveDisjointProperty.ttl'))
        old_shapes = Graph().parse(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'outdated_shapes.shacl'))
        updated_mapping, updated_shapes =   ocp2kg.propagate(change_data, None, None, None, old_shapes)
        updated_shapes.serialize(destination=os.path.join(os.path.dirname(os.path.realpath(__file__)), 'output1.ttl'), format='turtle')
        expected_shapes = Graph().parse(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'expected_shapes.shacl'))
        expected_shapes.serialize(destination=os.path.join(os.path.dirname(os.path.realpath(__file__)), 'output2.ttl'), format='turtle')
        self.assertEqual(compare.isomorphic(expected_shapes,updated_shapes),True)

if __name__ == "__main__":
    unittest.main()
    print("Tests RemoveDisjointProperty Passed for SHACL Shapes")