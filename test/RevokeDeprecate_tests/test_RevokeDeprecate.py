import os
import sys
from rdflib.graph import Graph
from rdflib import compare
import unittest
ruta_relativa = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'src'))
if ruta_relativa not in sys.path:
    sys.path.insert(0, ruta_relativa)
import ocp2kg


class TestDeprecateEntity01(unittest.TestCase):
    
    """Case 0: Case where the deprecated entity is a class."""
    def test_revokedeprecate_class00(self):
        change_data = Graph().parse(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Class_Tests/changes_revoke_deprecate_class.ttl'))
        old_mapping = Graph().parse(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Class_Tests/outdated_mapping_revoke_deprecate_class.ttl'))
        ontology = Graph().parse(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'ontology.ttl'))
        deprecated_mappings = Graph().parse(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Class_Tests/deprecated_mappings_class.ttl'))
        updated_mapping=ocp2kg.propagate(change_data, old_mapping, deprecated_mappings, ontology)
        expected_mapping = Graph().parse(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Class_Tests/expected_mapping_revoke_deprecate_class.ttl'))
        expected_iso= compare.to_isomorphic(expected_mapping)
        output_iso= compare.to_isomorphic(updated_mapping)
        expected_iso.serialize(destination=os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Class_Tests/output1.ttl'), format='turtle')
        output_iso.serialize(destination=os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Class_Tests/output2.ttl'), format='turtle')
        self.assertEqual(compare.isomorphic(expected_iso,output_iso),True)

    """Case 1: Case where the deprecated entity is an object property."""
    def test_revokedeprecate_class01(self):
        change_data = Graph().parse(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'OP_Tests/changes_revoke_deprecate_op.ttl'))
        old_mapping = Graph().parse(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'OP_Tests/outdated_mapping_revoke_deprecate_op.ttl'))
        ontology = Graph().parse(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'ontology.ttl'))
        deprecated_mappings = Graph().parse(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'OP_Tests/deprecated_mappings_op.ttl'))
        updated_mapping=ocp2kg.propagate(change_data, old_mapping, deprecated_mappings, ontology)
        expected_mapping = Graph().parse(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'OP_Tests/expected_mapping_revoke_deprecate_op.ttl'))
        expected_iso= compare.to_isomorphic(expected_mapping)
        output_iso= compare.to_isomorphic(updated_mapping)
        expected_iso.serialize(destination=os.path.join(os.path.dirname(os.path.realpath(__file__)), 'OP_Tests/output1.ttl'), format='turtle')
        output_iso.serialize(destination=os.path.join(os.path.dirname(os.path.realpath(__file__)), 'OP_Tests/output2.ttl'), format='turtle')
        self.assertEqual(compare.isomorphic(expected_iso,output_iso),True)

    """Case 2: Case where the deprecated entity is a data property."""
    def test_revokedeprecate_class02(self):
        change_data = Graph().parse(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'DP_Tests/changes_revoke_deprecate_dp.ttl'))
        old_mapping = Graph().parse(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'DP_Tests/outdated_mapping_revoke_deprecate_dp.ttl'))
        ontology = Graph().parse(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'ontology.ttl'))
        deprecated_mappings = Graph().parse(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'DP_Tests/deprecated_mappings_dp.ttl'))
        updated_mapping=ocp2kg.propagate(change_data, old_mapping, deprecated_mappings, ontology)
        expected_mapping = Graph().parse(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'DP_Tests/expected_mapping_revoke_deprecate_dp.ttl'))
        expected_iso= compare.to_isomorphic(expected_mapping)
        output_iso= compare.to_isomorphic(updated_mapping)
        expected_iso.serialize(destination=os.path.join(os.path.dirname(os.path.realpath(__file__)), 'DP_Tests/output1.ttl'), format='turtle')
        output_iso.serialize(destination=os.path.join(os.path.dirname(os.path.realpath(__file__)), 'DP_Tests/output2.ttl'), format='turtle')
        self.assertEqual(compare.isomorphic(expected_iso,output_iso),True)

if __name__ == "__main__":
    unittest.main()
    print("Tests RevokeDeprecate Passed")