import os
import sys
from rdflib.graph import Graph
from rdflib import compare
import unittest
ruta_relativa = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'src'))
if ruta_relativa not in sys.path:
    sys.path.insert(0, ruta_relativa)
import ontoripple


class TestDeprecateEntity01(unittest.TestCase):
    
    """Case 0: Case where the deprecated entity is a class."""
    def test_deprecate_class00(self):
        change_data = Graph().parse(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Class_Tests/changes_deprecate_class.ttl'))
        old_mapping = Graph().parse(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Class_Tests/outdated_mapping_deprecate_class.ttl'))
        ontology = Graph().parse(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'ontology.ttl'))
        expected_deprecated_mappings = Graph().parse(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Class_Tests/expected_deprecated_mappings_class.ttl'))
        deprecated_mappings = Graph()
        updated_mapping,updated_shapes=ontoripple.propagate(change_data, old_mapping, deprecated_mappings, ontology,None)
        expected_mapping = Graph().parse(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Class_Tests/expected_mapping_deprecate_class.ttl'))
        expected_iso= compare.to_isomorphic(expected_mapping)
        output_iso= compare.to_isomorphic(updated_mapping)
        deprecated_iso = compare.to_isomorphic(deprecated_mappings)
        expected_deprecated_iso = compare.to_isomorphic(expected_deprecated_mappings)
        expected_iso.serialize(destination=os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Class_Tests/output1.ttl'), format='turtle')
        output_iso.serialize(destination=os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Class_Tests/output2.ttl'), format='turtle')
        deprecated_iso.serialize(destination=os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Class_Tests/output3.ttl'), format='turtle')
        expected_deprecated_iso.serialize(destination=os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Class_Tests/output4.ttl'), format='turtle')
        self.assertEqual(compare.isomorphic(expected_iso,output_iso),True)
        self.assertEqual(compare.isomorphic(deprecated_iso,expected_deprecated_iso),True)

    """Case 1: Case where the deprecated entity is an object property."""
    def test_deprecate_class01(self):
        change_data = Graph().parse(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'OP_Tests/changes_deprecate_op.ttl'))
        old_mapping = Graph().parse(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'OP_Tests/outdated_mapping_deprecate_op.ttl'))
        ontology = Graph().parse(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'ontology.ttl'))
        expected_deprecated_mappings = Graph().parse(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'OP_Tests/expected_deprecated_mappings_op.ttl'))
        deprecated_mappings = Graph()
        updated_mapping,updated_shapes=ontoripple.propagate(change_data, old_mapping, deprecated_mappings, ontology,None)
        expected_mapping = Graph().parse(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'OP_Tests/expected_mapping_deprecate_op.ttl'))
        expected_iso= compare.to_isomorphic(expected_mapping)
        output_iso= compare.to_isomorphic(updated_mapping)
        deprecated_iso = compare.to_isomorphic(deprecated_mappings)
        expected_deprecated_iso = compare.to_isomorphic(expected_deprecated_mappings)
        expected_iso.serialize(destination=os.path.join(os.path.dirname(os.path.realpath(__file__)), 'OP_Tests/output1.ttl'), format='turtle')
        output_iso.serialize(destination=os.path.join(os.path.dirname(os.path.realpath(__file__)), 'OP_Tests/output2.ttl'), format='turtle')
        deprecated_iso.serialize(destination=os.path.join(os.path.dirname(os.path.realpath(__file__)), 'OP_Tests/output3.ttl'), format='turtle')
        expected_deprecated_iso.serialize(destination=os.path.join(os.path.dirname(os.path.realpath(__file__)), 'OP_Tests/output4.ttl'), format='turtle')
        self.assertEqual(compare.isomorphic(expected_iso,output_iso),True)
        self.assertEqual(compare.isomorphic(deprecated_iso,expected_deprecated_iso),True)

    """Case 2: Case where the deprecated entity is a data property."""
    def test_deprecate_class02(self):
        change_data = Graph().parse(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'DP_Tests/changes_deprecate_dp.ttl'))
        old_mapping = Graph().parse(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'DP_Tests/outdated_mapping_deprecate_dp.ttl'))
        ontology = Graph().parse(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'ontology.ttl'))
        expected_deprecated_mappings = Graph().parse(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'DP_Tests/expected_deprecated_mappings_dp.ttl'))
        deprecated_mappings = Graph()
        updated_mapping,updated_shapes=ontoripple.propagate(change_data, old_mapping, deprecated_mappings, ontology,None)
        expected_mapping = Graph().parse(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'DP_Tests/expected_mapping_deprecate_dp.ttl'))
        expected_iso= compare.to_isomorphic(expected_mapping)
        output_iso= compare.to_isomorphic(updated_mapping)
        deprecated_iso = compare.to_isomorphic(deprecated_mappings)
        expected_deprecated_iso = compare.to_isomorphic(expected_deprecated_mappings)
        expected_iso.serialize(destination=os.path.join(os.path.dirname(os.path.realpath(__file__)), 'DP_Tests/output1.ttl'), format='turtle')
        output_iso.serialize(destination=os.path.join(os.path.dirname(os.path.realpath(__file__)), 'DP_Tests/output2.ttl'), format='turtle')
        deprecated_iso.serialize(destination=os.path.join(os.path.dirname(os.path.realpath(__file__)), 'DP_Tests/output3.ttl'), format='turtle')
        expected_deprecated_iso.serialize(destination=os.path.join(os.path.dirname(os.path.realpath(__file__)), 'DP_Tests/output4.ttl'), format='turtle')
        self.assertEqual(compare.isomorphic(expected_iso,output_iso),True)
        self.assertEqual(compare.isomorphic(deprecated_iso,expected_deprecated_iso),True)

if __name__ == "__main__":
    unittest.main()
    print("Tests DeprecateEntity Passed")