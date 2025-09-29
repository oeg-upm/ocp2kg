import os
import sys
from rdflib.graph import Graph
from rdflib import compare
import unittest
ruta_relativa = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'src'))
if ruta_relativa not in sys.path:
    sys.path.insert(0, ruta_relativa)
import ocp2kg    

change_data = Graph().parse(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'change_data_3.0.1.ttl'), format='turtle')
old_mappings = Graph().parse(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'ePO_mappings.rml.ttl'), format='turtle')
old_shapes = Graph().parse(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'ePO_shacl_shapes_3.0.0.rdf'), format='xml')
ontology = Graph().parse(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'ePO_owl_core_3.0.1.rdf'), format='xml')
updated_mapping, updated_shapes =   ocp2kg.propagate(change_data, old_mappings, None, ontology, old_shapes)
updated_shapes.serialize(destination=os.path.join(os.path.dirname(os.path.realpath(__file__)), 'updated_shapes.ttl'), format='turtle')
updated_mapping.serialize(destination=os.path.join(os.path.dirname(os.path.realpath(__file__)), 'updated_mappings.ttl'), format='turtle')