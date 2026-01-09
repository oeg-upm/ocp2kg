import os
import sys
from rdflib.graph import Graph
from rdflib import compare
import unittest
import importlib.util
import ontoripple
ruta_relativa = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'src'))
if ruta_relativa not in sys.path:
    sys.path.insert(0, ruta_relativa)

change_data = Graph().parse(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'changelog.ttl'), format='turtle')
old_mappings = Graph().parse(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'mapping_hinojosa_2024.ttl'), format='turtle')
old_shapes = Graph().parse(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'emolex_scoop.ttl'), format='turtle')
ontology = Graph().parse(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'emolex.ttl'), format='ttl')
updated_mapping, updated_shapes =   ontoripple.propagate(change_data, old_mappings, None, ontology, old_shapes)
updated_shapes.serialize(destination=os.path.join(os.path.dirname(os.path.realpath(__file__)), 'updated_shapes.ttl'), format='turtle')
updated_mapping.serialize(destination=os.path.join(os.path.dirname(os.path.realpath(__file__)), 'updated_mappings.ttl'), format='turtle')