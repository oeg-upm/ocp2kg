import os
import sys
from rdflib.graph import Graph
from rdflib import compare
import unittest
ruta_relativa = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'src'))
if ruta_relativa not in sys.path:
    sys.path.insert(0, ruta_relativa)
import ocp2kg

class TestAddDisjointClassSH(unittest.TestCase):
    
    def test_Disjoint_class00(self):
        change_data = Graph().parse(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'changes_AddDisjointClass.ttl'))
        old_shapes = Graph().parse(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'outdated_shapes.shacl'))
        updated_mapping, updated_shapes =   ocp2kg.propagate(change_data, None, None, None, old_shapes)
        expected_shapes = Graph().parse(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'expected_shapes.shacl'))
        updated_shapes.serialize(destination=os.path.join(os.path.dirname(os.path.realpath(__file__)), 'output.shacl'), format='turtle')
        expected_iso = compare.to_isomorphic(expected_shapes)
        output_iso = compare.to_isomorphic(updated_shapes)
        #expected_iso.serialize(destination=os.path.join(os.path.dirname(os.path.realpath(__file__)), 'output2.shacl'), format='turtle')
        #output_iso.serialize(destination=os.path.join(os.path.dirname(os.path.realpath(__file__)), 'output3.shacl'), format='turtle')
        self.assertEqual(compare.isomorphic(expected_iso,output_iso),True)

if __name__ == "__main__":
    unittest.main()
    print("Tests AddDisjointClass Passed for SHACL Shapes")