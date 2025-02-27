import os
import sys
import ocp2kg
from rdflib.graph import Graph
from rdflib.compare import isomorphic, to_isomorphic
import unittest
ruta_relativa = os.path.abspath(os.path.join(os.path.dirname(__file__), '..','..','..'))
sys.path.append(ruta_relativa)

class TestAddObjectProperty01(unittest.TestCase):
    
    """Case 0: An object property is added. Domain and Range need to be included as well to have an effect in the mappings."""
    def test_add_objectproperty00(self):
        change_data = Graph().parse(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'changes_AddObjectProperty.ttl'))
        old_mapping = Graph().parse(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'outdated_mapping_AddObjectProperty.ttl'))
        ontology = Graph()
        review_mappings = Graph()
        updated_mapping=ocp2kg.propagate(change_data, old_mapping, review_mappings, ontology)
        expected_mapping = Graph().parse(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'expected_mapping_AddObjectProperty.ttl'))
        expected_iso= to_isomorphic(expected_mapping)
        output_iso= to_isomorphic(updated_mapping)
        self.assertEqual(isomorphic(expected_iso,output_iso),True)

if __name__ == "__main__":
    unittest.main()
    print("Tests AddObjectProperty Passed")