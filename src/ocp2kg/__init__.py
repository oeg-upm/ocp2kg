from rdflib import URIRef, Graph
from .constants import *
from .evol_kg import *

def propagate(change_data, output_mappings, review_mappings, ontology, output_shacl):
    changes_order = (OCH_ADD_CLASS, OCH_ADD_SUBCLASS, OCH_ADD_OBJECT_PROPERTY, OCH_ADD_DATA_PROPERTY, OCH_REMOVE_CLASS,
                     OCH_REMOVE_SUBCLASS, OCH_REMOVE_OBJECT_PROPERTY, OCH_REMOVE_DATA_PROPERTY,OCH_DEPRECATE_ENTITY, OCH_REVOKE_DEPRECATE, OCH_RENAME_ENTITY)

    for change_type in changes_order:

        q = f'  SELECT DISTINCT ?change WHERE {{ ' \
            f'  ?change {RDF_TYPE} {URIRef(change_type)} . }}'

        for change_result in change_data.query(q):
            if URIRef(change_type) == URIRef(OCH_ADD_CLASS):
                if output_mappings is not None:
                    add_class_rml(change_result["change"], change_data, output_mappings)
                if output_shacl is not None:
                    add_class_shacl(change_result["change"], change_data,output_shacl)
            elif URIRef(change_type) == URIRef(OCH_REMOVE_CLASS):
                if output_mappings is not None:
                    remove_class_rml(change_result["change"], change_data, output_mappings, review_mappings, ontology)
                if output_shacl is not None:
                    remove_class_shacl(change_result["change"], change_data, output_shacl)
            elif URIRef(change_type) == URIRef(OCH_ADD_SUBCLASS):
                if output_mappings is not None:
                    add_super_class_rml(change_result["change"], change_data, output_mappings)
                if output_shacl is not None:
                    add_super_class_shacl(change_result["change"], change_data, output_shacl)
            elif URIRef(change_type) == URIRef(OCH_REMOVE_SUBCLASS):
                if output_mappings is not None:
                    remove_super_class_rml(change_result["change"], change_data, output_mappings)
                if output_shacl is not None:
                    remove_super_class_shacl(change_result["change"], change_data, output_shacl)
            elif URIRef(change_type) == URIRef(OCH_ADD_OBJECT_PROPERTY):
                if output_mappings is not None:
                    add_object_property_rml(change_result["change"], change_data, output_mappings)
                if output_shacl is not None:
                    add_object_property_shacl(change_result["change"], change_data, output_shacl)
            elif URIRef(change_type) == URIRef(OCH_REMOVE_OBJECT_PROPERTY):
                if output_mappings is not None:
                    remove_object_property_rml(change_result["change"], change_data, output_mappings)
                if output_shacl is not None:
                    remove_object_property_shacl(change_result["change"], change_data, output_shacl)
            elif URIRef(change_type) == URIRef(OCH_ADD_DATA_PROPERTY):
                if output_mappings is not None:
                    add_data_property_rml(change_result["change"], change_data, output_mappings)
                if output_shacl is not None:
                    add_data_property_shacl(change_result["change"], change_data, output_shacl)
            elif URIRef(change_type) == URIRef(OCH_REMOVE_DATA_PROPERTY):
                if output_mappings is not None:
                    remove_data_property_rml(change_result["change"], change_data, output_mappings)
                if output_shacl is not None:
                    remove_data_property_shacl(change_result["change"], change_data, output_shacl)
            elif URIRef(change_type) == URIRef(OCH_DEPRECATE_ENTITY):
                if output_mappings is not None:
                    deprecate_entity_rml(change_result["change"], change_data, output_mappings, review_mappings, ontology)
                if output_shacl is not None:
                    deprecate_entity_shacl(change_result["change"], change_data, output_shacl)
            elif URIRef(change_type) == URIRef(OCH_REVOKE_DEPRECATE):
                if output_mappings is not None:
                    revoke_deprecate_entity_rml(change_result["change"], change_data, output_mappings, review_mappings, ontology)
                if output_shacl is not None:
                    revoke_deprecate_entity_shacl(change_result["change"], change_data, output_shacl)
            elif URIRef(change_type) == URIRef(OCH_RENAME_ENTITY):
                if output_mappings is not None:
                    rename_entity(change_result["change"], change_data, output_mappings)
                if output_shacl is not None:
                    rename_entity(change_result["change"], change_data, output_shacl)

    logger.info("Changes propagated over semantic artefacts, writing results...")
    return output_mappings, output_shacl