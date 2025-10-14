import os
import sys
from rdflib.graph import Graph
from rdflib import compare
import unittest
ruta_relativa = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'src'))
if ruta_relativa not in sys.path:
    sys.path.insert(0, ruta_relativa)
import ontoripple

class TestRemoveObjectProperty01(unittest.TestCase):
    
    """Case 0: The object Property is removed. Domain and range have to be included to have an effect on mappings."""
    def test_RemoveObjectProperty00(self):
        change_data = Graph().parse(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'changes_RemoveObjectProperty.ttl'))
        old_mapping = Graph().parse(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'outdated_mapping_RemoveObjectProperty.ttl'))
        ontology = Graph()
        review_mappings = Graph()
        updated_mapping, updated_shapes = ontoripple.propagate(change_data, old_mapping, review_mappings, ontology,None)
        expected_mapping = Graph().parse(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'expected_mapping_RemoveObjectProperty.ttl'))
        self.assertEqual(compare.isomorphic(expected_mapping,updated_mapping),True)

if __name__ == "__main__":
    unittest.main()
    print("Tests RemoveObjectProperty Passed")