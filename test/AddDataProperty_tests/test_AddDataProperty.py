import os
import ocp2kg
from rdflib.graph import Graph
from rdflib import compare
import unittest


class TestAddDataProperty01(unittest.TestCase):
    
    """Case 0: A Data property is added. Domain and Range need to be included as well to have an effect in the mappings."""
    def test_add_dataproperty00(self):
        change_data = Graph().parse(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'changes_AddDataProperty.ttl'))
        old_mapping = Graph().parse(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'outdated_mapping_AddDataProperty.ttl'))
        updated_mapping=ocp2kg.propagate(change_data, old_mapping, Graph(), Graph())
        expected_mapping = Graph().parse(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'expected_mapping_AddDataProperty.ttl'))
        expected_iso = compare.to_isomorphic(expected_mapping)
        output_iso = compare.to_isomorphic(updated_mapping)
        self.assertEqual(compare.isomorphic(expected_iso,output_iso),True)

if __name__ == "__main__":
    unittest.main()
    print("Tests AddDataProperty Passed")