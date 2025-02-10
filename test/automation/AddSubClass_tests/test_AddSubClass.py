import os
import sys
from rdflib.graph import Graph
from rdflib import compare
import unittest
ruta_relativa = os.path.abspath(os.path.join(os.path.dirname(__file__), '..','..','..'))
sys.path.append(ruta_relativa)

class TestAddSubClass01(unittest.TestCase):
    
    """Case 0: A rdsf:subClassOf relation is added between two classes."""
    def test_add_class00(self):
        expected_mapping = Graph()
        expected_mapping.parse(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'expected_mapping_AddSubClass.ttl'))
        os.system(f"python3 {ruta_relativa}/src/ocp2kg/evol_kg.py -c {ruta_relativa}/test/automation/AddSubClass_tests/changes_AddSubClass.ttl -m {ruta_relativa}/test/automation/AddSubClass_tests/expected_mapping_AddSubClass.ttl -o {ruta_relativa}/examples/ppds/epo-ontology/ePO_3.1.ttl -n {ruta_relativa}/test/automation/AddSubClass_tests/output.ttl")
        updated_mapping=Graph()
        updated_mapping.parse(f"{ruta_relativa}/test/automation/AddSubClass_tests/output.ttl")
        self.assertEqual(compare.isomorphic(expected_mapping,updated_mapping),True)

if __name__ == "__main__":
    unittest.main()
    print("Tests AddSubClass Passed")