import os
import sys
import unittest
from rdflib import Graph, compare
RML_URI = 'http://semweb.mmlab.be/ns/rml#'
ruta_relativa = os.path.abspath(os.path.join(os.path.dirname(__file__), '..','..','..'))
sys.path.append(ruta_relativa)

class TestRemoveClass01(unittest.TestCase):
    
    """Case 0: Where the removed class has no parent class in the ontology."""
    def test_remove_class00(self):
        expected_mapping = Graph()
        expected_mapping.parse(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'expected_mapping_remove_class.ttl'))
        os.system(f"python3 {ruta_relativa}/src/ocp2kg/evol_kg.py -c {ruta_relativa}/test/automation/RemoveClass_tests/changes_remove_class.ttl -m {ruta_relativa}/test/automation/RemoveClass_tests/outdated_mapping_remove_class.ttl -o {ruta_relativa}/examples/ppds/epo-ontology/ePO_3.1.ttl -n {ruta_relativa}/test/automation/RemoveClass_tests/output.ttl")
        updated_mapping=Graph()
        updated_mapping.parse(f"{ruta_relativa}/test/automation/RemoveClass_tests/output.ttl")
        self.assertEqual(compare.isomorphic(expected_mapping,updated_mapping),True)

    """Case 1: Where the removed class has parent class in the ontology."""
    def test_remove_class01(self):
        expected_mapping = Graph()
        expected_mapping.parse(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'expected_mapping_remove_class.ttl'))
        os.system(f"python3 {ruta_relativa}/src/ocp2kg/evol_kg.py -c {ruta_relativa}/test/automation/RemoveClass_tests/changes_remove_class.ttl -m {ruta_relativa}/test/automation/RemoveClass_tests/outdated_mapping_remove_class.ttl -o {ruta_relativa}/test/automation/RemoveClass_tests/ontology.ttl -n {ruta_relativa}/test/automation/RemoveClass_tests/output.ttl")
        updated_mapping=Graph()
        updated_mapping.parse(f"{ruta_relativa}/test/automation/RemoveClass_tests/output.ttl")
        self.assertEqual(compare.isomorphic(expected_mapping,updated_mapping),True)
        expected_review_mapping=Graph()
        expected_review_mapping.parse(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'expected_review_mappings.ttl'))
        review_mapping=Graph()
        review_mapping.parse(os.path.join(os.path.dirname(os.path.realpath(__file__)), f'{ruta_relativa}/review_mappings.ttl'))
        self.assertEqual(compare.isomorphic(expected_review_mapping,review_mapping),True)

    """Case 2: Where the removed class has a parent triples map."""
    def test_remove_class02(self):
        expected_mapping = Graph()
        expected_mapping.parse(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'ptmexpected_mapping_remove_class.ttl'))
        os.system(f"python3 {ruta_relativa}/src/ocp2kg/evol_kg.py -c {ruta_relativa}/test/automation/RemoveClass_tests/ptmchanges_remove_class.ttl -m {ruta_relativa}/test/automation/RemoveClass_tests/ptmoutdated_mapping_remove_class.ttl -o {ruta_relativa}/examples/ppds/epo-ontology/ePO_3.1.ttl -n {ruta_relativa}/test/automation/RemoveClass_tests/output.ttl")
        updated_mapping=Graph()
        updated_mapping.parse(f"{ruta_relativa}/test/automation/RemoveClass_tests/output.ttl")
        self.assertEqual(compare.isomorphic(expected_mapping,updated_mapping),True)

if __name__ == "__main__":
    unittest.main()
    print("Tests Remove Class Passed") 