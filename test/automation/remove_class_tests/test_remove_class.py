import os
import sys
from rdflib.graph import Graph
from rdflib import compare
import unittest
RML_URI = 'http://semweb.mmlab.be/ns/rml#'
ruta_relativa = os.path.abspath(os.path.join(os.path.dirname(__file__), '..','..','..', 'src'))
sys.path.append(ruta_relativa)

class TestRemoveClass01(unittest.TestCase):
    
    """Case 0: Where the removed class has no parent class in the ontology."""
    def test_remove_class00(self):
        expected_mapping = Graph()
        expected_mapping.parse(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'expected_mapping_remove_class.ttl'))
        os.system("python3 ./src/evol_kg.py -c ./test/automation/remove_class_tests/changes_remove_class.ttl -m ./test/automation/remove_class_tests/outdated_mapping_remove_class.ttl -o ./examples/ppds/epo-ontology/ePO_3.1.ttl -n ./test/automation/remove_class_tests/output.ttl")
        updated_mapping=Graph()
        updated_mapping.parse("./test/automation/remove_class_tests/output.ttl")
        self.assertEqual(compare.isomorphic(expected_mapping,updated_mapping),True)

    """Case 1: Where the removed class has parent class in the ontology."""
    def test_remove_class01(self):
        expected_mapping = Graph()
        expected_mapping.parse(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'expected_mapping_remove_class.ttl'))
        os.system("python3 ./src/evol_kg.py -c ./test/automation/remove_class_tests/changes_remove_class.ttl -m ./test/automation/remove_class_tests/outdated_mapping_remove_class.ttl -o ./test/automation/remove_class_tests/ontology.ttl -n ./test/automation/remove_class_tests/output1.ttl")
        updated_mapping=Graph()
        updated_mapping.parse("./test/automation/remove_class_tests/output1.ttl")
        self.assertEqual(compare.isomorphic(expected_mapping,updated_mapping),True)

if __name__ == "__main__":
    unittest.main()
    print("Tests Remove Class Passed") 