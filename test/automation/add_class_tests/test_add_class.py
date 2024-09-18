import os
import sys
from rdflib.graph import Graph
from rdflib import compare
import unittest
RML_URI = 'http://semweb.mmlab.be/ns/rml#'
ruta_relativa = os.path.abspath(os.path.join(os.path.dirname(__file__), '..','..','..', 'src'))
sys.path.append(ruta_relativa)

class TestAddClass01(unittest.TestCase):
    
    """Case 0: Where the added class is already included in the mappings."""
    def test_add_class00(self):
        expected_mapping = Graph()
        expected_mapping.parse(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'expected_mapping_add_class.ttl'))
        os.system("python3 ./src/evol_kg.py -c ./test/automation/add_class_tests/changes_add_class.ttl -m ./test/automation/add_class_tests/expected_mapping_add_class.ttl -o ./examples/ppds/epo-ontology/ePO_3.1.ttl -n ./test/automation/add_class_tests/output.ttl")
        updated_mapping=Graph()
        updated_mapping.parse("./test/automation/add_class_tests/output.ttl")
        #print(" Test for the AddClas Operation 1")
        self.assertEqual(compare.isomorphic(expected_mapping,updated_mapping),True)

    """Case 1: where the added class is not within the mappings."""
    def test_add_class01(self):
        expected_mapping = Graph()
        expected_mapping.parse(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'expected_mapping_add_class.ttl'))
        os.system("python3 ./src/evol_kg.py -c ./test/automation/add_class_tests/changes_add_class.ttl -m ./test/automation/add_class_tests/outdated_mapping_add_class.ttl -o ./examples/ppds/epo-ontology/ePO_3.1.ttl -n ./test/automation/add_class_tests/output.ttl")
        updated_mapping=Graph()
        updated_mapping.parse("./test/automation/add_class_tests/output.ttl")
        #print(" Test for the AddClas Operation 1")
        self.assertEqual(compare.isomorphic(expected_mapping,updated_mapping),True)

if __name__ == "__main__":
    unittest.main()
    print("Tests Add Class Passed")