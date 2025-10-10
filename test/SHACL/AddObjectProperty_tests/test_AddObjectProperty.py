import os
import sys
from rdflib.graph import Graph
from rdflib.compare import isomorphic, to_isomorphic
import unittest
ruta_relativa = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'src'))
if ruta_relativa not in sys.path:
    sys.path.insert(0, ruta_relativa)
import ontoripple

class TestAddObjectProperty01(unittest.TestCase):
    
    def test_add_objectproperty00(self):
        change_data = Graph().parse(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'changes_AddObjectProperty.ttl'))
        old_shapes = Graph().parse(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'outdated_shapes.shacl'))
        updated_mapping,updated_shapes=ontoripple.propagate(change_data, None, None, None,old_shapes)
        expected_shapes = Graph().parse(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'expected_shapes.shacl'))
        expected_iso= to_isomorphic(expected_shapes)
        expected_iso.serialize(destination=os.path.join(os.path.dirname(os.path.realpath(__file__)), 'output1.ttl'), format='turtle')
        output_iso= to_isomorphic(updated_shapes)
        output_iso.serialize(destination=os.path.join(os.path.dirname(os.path.realpath(__file__)), 'output2.ttl'), format='turtle')
        self.assertEqual(isomorphic(expected_iso,output_iso),True)

if __name__ == "__main__":
    unittest.main()
    print("Tests AddObjectProperty Passed")