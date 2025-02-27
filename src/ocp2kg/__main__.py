
from rdflib import Graph, URIRef, Variable
from . import propagate
import yatter
import argparse
from ruamel.yaml import YAML
from .evol_kg import *

def define_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--changes_kg_path", required=True, help="Change KG following the Change Ontology")
    parser.add_argument("-m", "--old_mapping_path", required=True, help="Old version of the mappings in RML")
    parser.add_argument("-o", "--ontology_path", required=False, help="New version of the ontology")
    parser.add_argument("-n", "--new_mappings_path", required=True, help="Output path for the generated mapping")
    parser.add_argument("-y", "--yarrrml", nargs=argparse.OPTIONAL, required=False, help="Mappings are also converted into YARRRML")
    return parser


if __name__ == "__main__":
    args = define_args().parse_args()
    change_data = Graph().parse(args.changes_kg_path, format="ttl")

    if args.old_mapping_path.endswith(".yml") or args.old_mapping_path.endswith(".yaml"):
        logger.info("Starting the propagation of changes over the mapping rules")
        logger.info("Loading old mapping rules from YARRRML using YATTER")
        yaml = YAML(typ='safe', pure=True)
        output_mappings = Graph().parse(yatter.translate(yaml.load(open(args.old_mapping_path)), RML_URI), format="ttl")
    else:
        output_mappings = Graph().parse(args.old_mapping_path, format="ttl")

    if args.ontology_path:
        ontology = Graph().parse(args.ontology_path)

    review_mappings = Graph()

    new_mapping = propagate(change_data, output_mappings, review_mappings,ontology)

    new_mapping.serialize(destination=args.new_mappings_path)
    review_mappings.serialize(destination="review_mappings.ttl")
    yarrrml_content = yatter.inverse_translation(output_mappings)
    with open(args.new_mappings_path.replace(".ttl", ".yml"), "wb") as f:
        yaml = YAML()
        yaml.default_flow_style = False
        yaml.width = 3000
        yaml.dump(yarrrml_content, f)