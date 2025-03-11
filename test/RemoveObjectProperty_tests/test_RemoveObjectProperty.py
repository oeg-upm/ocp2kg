import os
import ocp2kg
from rdflib.graph import Graph
from rdflib import compare
import unittest


class TestRemoveObjectProperty01(unittest.TestCase):
    
    """Case 0: The object Property is removed. Domain and range have to be included to have an effect on mappings."""
    def test_RemoveObjectProperty00(self):
        change_data = Graph().parse(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'changes_RemoveObjectProperty.ttl'))
        old_mapping = Graph().parse(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'outdated_mapping_RemoveObjectProperty.ttl'))
        updated_mapping=ocp2kg.propagate(change_data, old_mapping, Graph(), Graph())
        expected_mapping = Graph().parse(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'expected_mapping_RemoveObjectProperty.ttl'))
        self.assertEqual(compare.isomorphic(expected_mapping,updated_mapping),True)

if __name__ == "__main__":
    unittest.main()
    print("Tests RemoveObjectProperty Passed")