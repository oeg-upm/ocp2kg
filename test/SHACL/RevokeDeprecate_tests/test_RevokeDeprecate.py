import os
import sys
from rdflib.graph import Graph
from rdflib import compare
import unittest
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..','src'))
print(src_path)
if src_path not in sys.path:
    sys.path.insert(0, src_path)
import ocp2kg


class TestDeprecateEntity01(unittest.TestCase):
    
    """Case 0: Case where the deprecated entity is a class."""
    def test_revoke_deprecate_entity00(self):
        change_data = Graph().parse(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Class_Tests/changes_revoke_deprecate_class.ttl'))
        old_shapes = Graph().parse(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Class_Tests/outdated_shapes.shacl'))
        updated_mapping,updated_shapes=ocp2kg.propagate(change_data, None, None, None, old_shapes)
        expected_shapes = Graph().parse(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Class_Tests/expected_shapes.shacl'))
        expected_iso= compare.to_isomorphic(expected_shapes)
        output_iso= compare.to_isomorphic(updated_shapes)
        expected_iso.serialize(destination=os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Class_Tests/output1.ttl'), format='turtle')
        output_iso.serialize(destination=os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Class_Tests/output2.ttl'), format='turtle')
        self.assertEqual(compare.isomorphic(expected_iso,output_iso),True)

    """Case 1: Case where the deprecated entity is a property."""
    def test_revoke_deprecate_entity01(self):
        change_data = Graph().parse(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Property_Tests/changes_revoke_deprecate_property.ttl'))
        old_shapes = Graph().parse(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Property_Tests/outdated_shapes.shacl'))
        updated_mapping,updated_shapes=ocp2kg.propagate(change_data, None, None, None, old_shapes)
        expected_shapes = Graph().parse(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Property_Tests/expected_shapes.shacl'))
        expected_iso= compare.to_isomorphic(expected_shapes)
        output_iso= compare.to_isomorphic(updated_shapes)
        expected_iso.serialize(destination=os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Property_Tests/output1.ttl'), format='turtle')
        output_iso.serialize(destination=os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Property_Tests/output2.ttl'), format='turtle')
        self.assertEqual(compare.isomorphic(expected_iso,output_iso),True)


if __name__ == "__main__":
    unittest.main()
    print("Tests RevokeDeprecate Passed for SHACL Shapes")