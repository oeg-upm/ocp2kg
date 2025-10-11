import os
import sys
from rdflib.graph import Graph
from rdflib import compare
import unittest
ruta_relativa = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'src'))
if ruta_relativa not in sys.path:
    sys.path.insert(0, ruta_relativa)
import ontoripple

class TestRenameEntity00(unittest.TestCase):
    
    """Case 0: An OWL Entity is renamed from a URI to a new URI."""
    def test_rename_entity00(self):
        change_data = Graph().parse(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'changes_RenameEntity.ttl'))
        old_mapping = Graph().parse(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'outdated_mapping_RenameEntity.ttl'))
        ontology = Graph()
        review_mappings = Graph()
        updated_mapping, updated_shapes =   ontoripple.propagate(change_data, old_mapping, review_mappings, ontology,None)
        updated_mapping.serialize(destination=os.path.join(os.path.dirname(os.path.realpath(__file__)), 'output1.ttl'), format='turtle')
        expected_mapping = Graph().parse(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'expected_mapping_RenameEntity.ttl'))
        self.assertEqual(compare.isomorphic(expected_mapping,updated_mapping),True)

if __name__ == "__main__":
    unittest.main()
    print("Tests RenameEntity Passed")