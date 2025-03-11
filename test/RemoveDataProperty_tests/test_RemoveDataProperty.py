import os
import ocp2kg
from rdflib.graph import Graph
from rdflib import compare
import unittest


class TestRemoveDataProperty01(unittest.TestCase):
    
    """Case 0: A Data property is Removeed. Domain and Range need to be included as well to have an effect in the mappings."""
    def test_RemoveDataProperty00(self):
        change_data = Graph().parse(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'changes_RemoveDataProperty.ttl'))
        old_mapping = Graph().parse(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'outdated_mapping_RemoveDataProperty.ttl'))
        updated_mapping=ocp2kg.propagate(change_data, old_mapping, Graph(), Graph())
        expected_mapping = Graph().parse(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'expected_mapping_RemoveDataProperty.ttl'))
        self.assertEqual(compare.isomorphic(expected_mapping,updated_mapping),True)

if __name__ == "__main__":
    unittest.main()
    print("Tests RemoveDataProperty Passed")