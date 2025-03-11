import os
import ocp2kg
from rdflib.graph import Graph
from rdflib import compare
import unittest


class TestAddClass01(unittest.TestCase):
    
    """Case 0: Where the added class is already included in the mappings."""
    def test_add_class00(self):
        change_data = Graph().parse(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'changes_add_class.ttl'))
        ontology = Graph().parse(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'ontology.ttl'))
        expected_mapping = Graph().parse(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'expected_mapping_add_class.ttl'))
        updated_mapping = ocp2kg.propagate(change_data, expected_mapping, Graph(), ontology)
        self.assertEqual(compare.isomorphic(expected_mapping,updated_mapping),True)

    """Case 1: where the added class is not within the mappings."""
    def test_add_class01(self):
        change_data = Graph().parse(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'changes_add_class.ttl'))
        old_mapping = Graph().parse(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'outdated_mapping_add_class.ttl'))
        ontology = Graph().parse(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'ontology.ttl'))
        updated_mapping = ocp2kg.propagate(change_data, old_mapping, Graph(), ontology)
        expected_mapping = Graph().parse(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'expected_mapping_add_class.ttl'))
        self.assertEqual(compare.isomorphic(expected_mapping,updated_mapping),True)

if __name__ == "__main__":
    unittest.main()
    print("Tests Add Class Passed")