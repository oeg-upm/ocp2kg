import os
import unittest
import ocp2kg
from rdflib import Graph, compare


class TestRemoveClass01(unittest.TestCase):
    

    """Case 0: Where the removed class has no parent class in the ontology."""
    def test_remove_class00(self):
        change_data = Graph().parse(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'changes_remove_class.ttl'))
        old_mapping = Graph().parse(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'outdated_mapping_remove_class.ttl'))
        updated_mapping=ocp2kg.propagate(change_data, old_mapping, Graph(), Graph())
        expected_mapping = Graph().parse(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'expected_mapping_remove_class.ttl'))
        self.assertEqual(compare.isomorphic(expected_mapping,updated_mapping),True)

    """Case 1: Where the removed class has parent class in the ontology."""
    def test_remove_class01(self):
        change_data = Graph().parse(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'changes_remove_class.ttl'))
        old_mapping = Graph().parse(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'outdated_mapping_remove_class.ttl'))
        ontology = Graph().parse(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'ontology.ttl'))
        updated_mapping=ocp2kg.propagate(change_data, old_mapping, Graph(), ontology)
        expected_mapping = Graph().parse(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'expected_mapping_remove_class.ttl'))
        self.assertEqual(compare.isomorphic(expected_mapping,updated_mapping),True)

    """Case 2: Where the removed class has a parent triples map."""
    def test_remove_class02(self):
        change_data = Graph().parse(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'ptmchanges_remove_class.ttl'))
        old_mapping = Graph().parse(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'ptmoutdated_mapping_remove_class.ttl'))
        updated_mapping=ocp2kg.propagate(change_data, old_mapping, Graph(), Graph())
        expected_mapping = Graph().parse(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'ptmexpected_mapping_remove_class.ttl'))
        self.assertEqual(compare.isomorphic(expected_mapping,updated_mapping),True)

if __name__ == "__main__":
    unittest.main()
    print("Tests Remove Class Passed") 