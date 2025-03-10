import os
import sys
import ocp2kg
from rdflib.graph import Graph
from rdflib import compare
import unittest
ruta_relativa = os.path.abspath(os.path.join(os.path.dirname(__file__), '..','..','..'))
sys.path.append(ruta_relativa)

class TestAddDataProperty01(unittest.TestCase):
    
    """Case 0: A Data property is added. Domain and Range need to be included as well to have an effect in the mappings."""
    def test_add_dataproperty00(self):
        change_data = Graph().parse(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'changes_AddDataProperty.ttl'))
        old_mapping = Graph().parse(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'outdated_mapping_AddDataProperty.ttl'))
        ontology = Graph()
        review_mappings = Graph()
        updated_mapping=ocp2kg.propagate(change_data, old_mapping, review_mappings, ontology)
        expected_mapping = Graph().parse(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'expected_mapping_AddDataProperty.ttl'))
        expected_iso = compare.to_isomorphic(expected_mapping)
        output_iso = compare.to_isomorphic(updated_mapping)
        expected_iso.serialize(destination=os.path.join(os.path.dirname(os.path.realpath(__file__)), 'output1.ttl'), format='turtle')
        output_iso.serialize(destination=os.path.join(os.path.dirname(os.path.realpath(__file__)), 'output2.ttl'), format='turtle')
        self.assertEqual(compare.isomorphic(expected_iso,output_iso),True)

if __name__ == "__main__":
    unittest.main()
    print("Tests AddDataProperty Passed")