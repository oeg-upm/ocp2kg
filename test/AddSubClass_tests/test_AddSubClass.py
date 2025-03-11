import os
import ocp2kg
from rdflib.graph import Graph
from rdflib import compare
import unittest

class TestAddSubClass01(unittest.TestCase):
    
    """Case 0: A rdsf:subClassOf relation is added between two classes."""
    def test_add_subclass00(self):
        change_data = Graph().parse(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'changes_AddSubClass.ttl'))
        old_mapping = Graph().parse(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'outdated_mapping_AddSubClass.ttl'))
        updated_mapping=ocp2kg.propagate(change_data, old_mapping, Graph(), Graph())
        expected_mapping = Graph().parse(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'expected_mapping_AddSubClass.ttl'))
        expected_iso= compare.to_isomorphic(expected_mapping)
        output_iso= compare.to_isomorphic(updated_mapping)
        self.assertEqual(compare.isomorphic(expected_iso,output_iso),True)

if __name__ == "__main__":
    unittest.main()
    print("Tests AddSubClass Passed")