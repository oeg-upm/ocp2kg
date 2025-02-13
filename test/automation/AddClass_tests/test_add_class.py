import ocp2kg
import os
from rdflib.graph import Graph
from rdflib import compare
import unittest


class TestAddClass01(unittest.TestCase):
    
    """Case 0: Where the added class is already included in the mappings."""
    def test_add_class00(self):

        change_data = Graph().parse(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'changes_add_class.ttl'))
        old_mapping = Graph().parse(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'outdated_mapping_add_class.ttl'))
        ontology = Graph().parse(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'ontology.ttl'))
        review_mappings = Graph()
        updated_mapping=ocp2kg.propagate(change_data, old_mapping, review_mappings, ontology)
        #print(" Test for the AddClas Operation 1")
        expected_mapping = Graph().parse(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'expected_mapping_add_class.ttl'))
        self.assertEqual(compare.isomorphic(expected_mapping,updated_mapping),True)

    """Case 1: where the added class is not within the mappings."""
    def test_add_class01(self):
        expected_mapping = Graph()
        expected_mapping.parse(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'expected_mapping_add_class.ttl'))
        os.system(f"python3 {ruta_relativa}/src/ocp2kg/evol_kg.py -c {ruta_relativa}/test/automation/AddClass_tests/changes_add_class.ttl -m {ruta_relativa}/test/automation/AddClass_tests/outdated_mapping_add_class.ttl -o {ruta_relativa}/examples/ppds/epo-ontology/ePO_3.1.ttl -n {ruta_relativa}/test/automation/AddClass_tests/output.ttl")
        updated_mapping=Graph()
        updated_mapping.parse(f"{ruta_relativa}/test/automation/AddClass_tests/output.ttl")

        self.assertEqual(compare.isomorphic(expected_mapping,updated_mapping),True)

if __name__ == "__main__":
    unittest.main()
    print("Tests Add Class Passed")