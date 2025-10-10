
from rdflib import Graph, URIRef, Variable
import rdflib
from . import propagate
import yatter
import argparse
from ruamel.yaml import YAML
from .evol_kg import *

def define_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--changes_kg_path", required=True, help="Change KG following the Change Ontology")
    parser.add_argument("-m", "--old_mapping_path", required=False, help="Old version of the mappings in RML")
    parser.add_argument("-s", "--old_shacl_path", required=False, help="Old version of the shapes in SHACL")
    parser.add_argument("-o", "--ontology_path", required=False, help="New version of the ontology")
    parser.add_argument("-nm", "--new_mappings_path", required=False, help="Output path for the generated mapping")
    parser.add_argument("-nsh", "--new_shapes_path", required=False, help="Output path for the generated shapes")
    parser.add_argument("-y", "--yarrrml", nargs=argparse.OPTIONAL, required=False, help="Mappings are also converted into YARRRML")
    return parser


if __name__ == "__main__":
    args = define_args().parse_args()
    change_data = Graph().parse(args.changes_kg_path, format=rdflib.util.guess_format(args.changes_kg_path))

    # Case 1: Both mapping and SHACL parameters are provided
    if (
        args.old_mapping_path and args.new_mappings_path and
        args.old_shacl_path and args.new_shapes_path
    ):
        # Process mappings
        if args.old_mapping_path.endswith(".yml") or args.old_mapping_path.endswith(".yaml"):
            logger.info("Starting the propagation of changes over the mapping rules")
            logger.info("Loading old mapping rules from YARRRML using YATTER")
            yaml = YAML(typ='safe', pure=True)
            output_mappings = Graph().parse(
                yatter.translate(yaml.load(open(args.old_mapping_path)), RML_URI), format=rdflib.util.guess_format(args.old_mapping_path)
            )
        else:
            output_mappings = Graph().parse(args.old_mapping_path, format=rdflib.util.guess_format(args.old_mapping_path))
        ontology = None
        if args.ontology_path:
            ontology = Graph().parse(args.ontology_path)

        logger.info("Starting the propagation of changes over RML mappings and SHACL shapes")
        review_mappings = Graph()
        output_shapes = Graph().parse(args.old_shacl_path, format=rdflib.util.guess_format(args.old_shacl_path))

        new_mapping,new_shapes = propagate(change_data, output_mappings, review_mappings, ontology, output_shapes)
        new_mapping.serialize(destination=args.new_mappings_path)
        new_shapes.serialize(destination=args.new_shapes_path)
        review_mappings.serialize(destination="review_mappings.ttl")
        yarrrml_content = yatter.inverse_translation(output_mappings)
        with open(args.new_mappings_path.replace(".ttl", ".yml"), "wb") as f:
            yaml = YAML()
            yaml.default_flow_style = False
            yaml.width = 3000
            yaml.dump(yarrrml_content, f)

    # Case 2: Only mapping parameters are provided
    elif args.old_mapping_path and args.new_mappings_path:
        if args.old_mapping_path.endswith(".yml") or args.old_mapping_path.endswith(".yaml"):
            logger.info("Starting the propagation of changes over the mapping rules")
            logger.info("Loading old mapping rules from YARRRML using YATTER")
            yaml = YAML(typ='safe', pure=True)
            output_mappings = Graph().parse(
                yatter.translate(yaml.load(open(args.old_mapping_path)), RML_URI), format=rdflib.util.guess_format(args.old_mapping_path)
            )
        else:
            output_mappings = Graph().parse(args.old_mapping_path, format=rdflib.util.guess_format(args.old_mapping_path))

        ontology = None
        if args.ontology_path:
            ontology = Graph().parse(args.ontology_path)

        review_mappings = Graph()
        new_mapping,new_shapes = propagate(change_data, output_mappings, review_mappings, ontology, None)
        new_mapping.serialize(destination=args.new_mappings_path)
        review_mappings.serialize(destination="review_mappings.ttl")
        yarrrml_content = yatter.inverse_translation(output_mappings)
        with open(args.new_mappings_path.replace(".ttl", ".yml"), "wb") as f:
            yaml = YAML()
            yaml.default_flow_style = False
            yaml.width = 3000
            yaml.dump(yarrrml_content, f)

    # Case 3: Only SHACL parameters are provided
    elif args.old_shacl_path and args.new_shapes_path:
        logger.info("Starting the propagation of changes over the SHACL shapes")
        output_shapes = Graph().parse(args.old_shacl_path, format=rdflib.util.guess_format(args.old_shacl_path))
        ontology = None
        if args.ontology_path:
            ontology = Graph().parse(args.ontology_path)
        new_mapping,new_shapes = propagate(change_data, None, None, ontology, output_shapes)
        new_shapes.serialize(destination=args.new_shapes_path)
