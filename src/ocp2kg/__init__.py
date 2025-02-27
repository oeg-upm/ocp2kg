from rdflib import URIRef, Graph
from .constants import *
from .evol_kg import *

def propagate(change_data, output_mappings, review_mappings, ontology=Graph()):
    changes_order = (OCH_ADD_CLASS, OCH_ADD_SUBCLASS, OCH_ADD_OBJECT_PROPERTY, OCH_ADD_DATA_PROPERTY, OCH_REMOVE_CLASS,
                     OCH_REMOVE_SUBCLASS, OCH_REMOVE_OBJECT_PROPERTY, OCH_REMOVE_DATA_PROPERTY)

    for change_type in changes_order:

        q = f'  SELECT DISTINCT ?change WHERE {{ ' \
            f'  ?change {RDF_TYPE} {URIRef(change_type)} . }}'

        for change_result in change_data.query(q):
            if URIRef(change_type) == URIRef(OCH_ADD_CLASS):
                add_class(change_result["change"], change_data, output_mappings)
            elif URIRef(change_type) == URIRef(OCH_REMOVE_CLASS):
                remove_class(change_result["change"],change_data, output_mappings, review_mappings, ontology)
            elif URIRef(change_type) == URIRef(OCH_ADD_SUBCLASS):
                add_super_class(change_result["change"],change_data, output_mappings)
            elif URIRef(change_type) == URIRef(OCH_REMOVE_SUBCLASS):
                remove_super_class(change_result["change"],change_data, output_mappings)
            elif URIRef(change_type) == URIRef(OCH_ADD_OBJECT_PROPERTY):
                add_object_property(change_result["change"],change_data, output_mappings)
            elif URIRef(change_type) == URIRef(OCH_REMOVE_OBJECT_PROPERTY):
                remove_object_property(change_result["change"],change_data, output_mappings)
            elif URIRef(change_type) == URIRef(OCH_ADD_DATA_PROPERTY):
                add_data_property(change_result["change"],change_data, output_mappings)
            elif URIRef(change_type) == URIRef(OCH_REMOVE_DATA_PROPERTY):
                remove_data_property(change_result["change"],change_data, output_mappings)

    logger.info("Changes propagated over the mapping rules, writing results...")
    return output_mappings