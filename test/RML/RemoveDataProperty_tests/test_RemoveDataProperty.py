import os
import sys
from rdflib.graph import Graph
from rdflib import compare
import unittest
ruta_relativa = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'src'))
if ruta_relativa not in sys.path:
    sys.path.insert(0, ruta_relativa)
import ontoripple

class TestRemoveDataProperty01(unittest.TestCase):
    
    """Case 0: A Data property is Removeed. Domain and Range need to be included as well to have an effect in the mappings."""
    def test_RemoveDataProperty00(self):
        change_data = Graph().parse(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'changes_RemoveDataProperty.ttl'))
        old_mapping = Graph().parse(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'outdated_mapping_RemoveDataProperty.ttl'))
        ontology = Graph()
        review_mappings = Graph()
        updated_mapping, updated_shapes = ontoripple.propagate(change_data, old_mapping, review_mappings, ontology,None)
        expected_mapping = Graph().parse(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'expected_mapping_RemoveDataProperty.ttl'))
        #updated_mapping.serialize(destination=os.path.join(os.path.dirname(os.path.realpath(__file__)), 'output1.ttl'), format='turtle')
        self.assertEqual(compare.isomorphic(expected_mapping,updated_mapping),True)
if __name__ == "__main__":
    unittest.main()
    print("Tests RemoveDataProperty Passed")