
from rdflib import Graph, URIRef, Variable

import yatter
from ruamel.yaml import YAML
import argparse
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
        output_mappings = Graph()
        yaml = YAML(typ='safe', pure=True)
        output_mappings.parse(yatter.translate(yaml.load(open(args.old_mapping_path)), RML_URI), format="ttl")
    else:
        output_mappings = Graph().parse(args.old_mapping_path, format="ttl")

    if args.ontology_path:
        ontology = Graph().parse(args.ontology_path)

    review_mappings = Graph()

    changes_order = (OCH_ADD_CLASS, OCH_ADD_SUBCLASS, OCH_ADD_OBJECT_PROPERTY, OCH_ADD_DATA_PROPERTY, OCH_REMOVE_CLASS,
                     OCH_REMOVE_SUBCLASS, OCH_REMOVE_OBJECT_PROPERTY, OCH_REMOVE_DATA_PROPERTY)

    # ToDo: removing subclass action needs to be implemented
    for change_type in changes_order:

        q = f'  SELECT DISTINCT ?change WHERE {{ ' \
            f'  ?change {RDF_TYPE} {URIRef(change_type)} . }}'

        for change_result in change_data.query(q):
            if URIRef(change_type) == URIRef(OCH_ADD_CLASS):
                add_class(change_result["change"])
            elif URIRef(change_type) == URIRef(OCH_REMOVE_CLASS):
                remove_class(change_result["change"])
            elif URIRef(change_type) == URIRef(OCH_ADD_SUBCLASS):
                add_super_class(change_result["change"])
            elif URIRef(change_type) == URIRef(OCH_REMOVE_SUBCLASS):
                remove_super_class(change_result["change"])
            elif URIRef(change_type) == URIRef(OCH_ADD_OBJECT_PROPERTY):
                add_object_property(change_result["change"])
            elif URIRef(change_type) == URIRef(OCH_REMOVE_OBJECT_PROPERTY):
                remove_object_property(change_result["change"])
            elif URIRef(change_type) == URIRef(OCH_ADD_DATA_PROPERTY):
                add_data_property(change_result["change"])
            elif URIRef(change_type) == URIRef(OCH_REMOVE_DATA_PROPERTY):
                remove_data_property(change_result["change"])

    logger.info("Changes propagated over the mapping rules, writing results...")

    output_mappings.serialize(destination=args.new_mappings_path)
    review_mappings.serialize(destination="review_mappings.ttl")
    yarrrml_content = yatter.inverse_translation(output_mappings)
    with open(args.new_mappings_path.replace(".ttl", ".yml"), "wb") as f:
        yaml = YAML()
        yaml.default_flow_style = False
        yaml.width = 3000
        yaml.dump(yarrrml_content, f)