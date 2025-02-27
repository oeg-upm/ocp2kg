import os
import sys
import ocp2kg
from rdflib.graph import Graph
from rdflib import compare
import unittest
ruta_relativa = os.path.abspath(os.path.join(os.path.dirname(__file__), '..','..','..'))
sys.path.append(ruta_relativa)

class TestRemoveSubClass01(unittest.TestCase):
    
    """Case 0: A rdsf:subClassOf relation is removed between two classes."""
    def test_remove_subclass00(self):
        change_data = Graph().parse(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'changes_RemoveSubClass.ttl'))
        old_mapping = Graph().parse(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'outdated_mapping_RemoveSubClass.ttl'))
        ontology = Graph()
        review_mappings = Graph()
        updated_mapping=ocp2kg.propagate(change_data, old_mapping, review_mappings, ontology)
        updated_mapping.serialize(destination=os.path.join(os.path.dirname(os.path.realpath(__file__)), 'output1.ttl'), format='turtle')
        expected_mapping = Graph().parse(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'expected_mapping_RemoveSubClass.ttl'))
        self.assertEqual(compare.isomorphic(expected_mapping,updated_mapping),True)

if __name__ == "__main__":
    unittest.main()
    print("Tests RemoveSubClass Passed")