from rdflib import URIRef, Graph
from .constants import *
from .evol_kg import *

def propagate(change_data, output_mappings, review_mappings, ontology, output_shacl):
    changes_order = (OCH_ADD_CLASS, OCH_ADD_SUBCLASS, OCH_ADD_OBJECT_PROPERTY, OCH_ADD_DATA_PROPERTY, OCH_REMOVE_CLASS,
                     OCH_REMOVE_SUBCLASS, OCH_REMOVE_OBJECT_PROPERTY, OCH_REMOVE_DATA_PROPERTY,OCH_DEPRECATE_ENTITY, OCH_REVOKE_DEPRECATE, OCH_RENAME_ENTITY, OCH_ADD_EQUIVALENT_CLASS, OCH_REMOVE_EQUIVALENT_CLASS, OCH_ADD_DISJOINT_CLASS, OCH_REMOVE_DISJOINT_CLASS, OCH_ADD_CHARACTERISTIC, OCH_REMOVE_CHARACTERISTIC, OCH_ADD_INVERSE_PROPERTY, OCH_REMOVE_INVERSE_PROPERTY, OCH_ADD_DISJOINT_PROPERTY, OCH_REMOVE_DISJOINT_PROPERTY, OCH_ADD_SUBPROPERTY, OCH_REMOVE_SUBPROPERTY, OCH_ADD_EQUIVALENT_PROPERTY, OCH_REMOVE_EQUIVALENT_PROPERTY)

    for change_type in changes_order:

        q = f'  SELECT DISTINCT ?change WHERE {{ ' \
            f'  ?change {RDF_TYPE} {URIRef(change_type)} . }}'
        #print(q)
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
            elif URIRef(change_type) == URIRef(OCH_ADD_EQUIVALENT_CLASS):
                if output_shacl is not None:
                    add_equivalent_class_shacl(change_result["change"], change_data, output_shacl)
            elif URIRef(change_type) == URIRef(OCH_REMOVE_EQUIVALENT_CLASS):
                if output_shacl is not None:
                    remove_equivalent_class_shacl(change_result["change"], change_data, output_shacl)
            elif URIRef(change_type) == URIRef(OCH_ADD_DISJOINT_CLASS):
                if output_shacl is not None:
                    add_disjoint_class_shacl(change_result["change"], change_data, output_shacl)
            elif URIRef(change_type) == URIRef(OCH_REMOVE_DISJOINT_CLASS):
                if output_shacl is not None:
                    remove_disjoint_class_shacl(change_result["change"], change_data, output_shacl)
            elif URIRef(change_type) == URIRef(OCH_ADD_CHARACTERISTIC):
                if output_shacl is not None:
                    add_characteristic_shacl(change_result["change"], change_data, output_shacl)
            elif URIRef(change_type) == URIRef(OCH_REMOVE_CHARACTERISTIC):
                if output_shacl is not None:
                    remove_characteristic_shacl(change_result["change"], change_data, output_shacl)
            elif URIRef(change_type) == URIRef(OCH_ADD_INVERSE_PROPERTY):
                if output_shacl is not None:
                    add_inverse_property_shacl(change_result["change"], change_data, output_shacl)
            elif URIRef(change_type) == URIRef(OCH_REMOVE_INVERSE_PROPERTY):
                if output_shacl is not None:
                    remove_inverse_property_shacl(change_result["change"], change_data, output_shacl)
            elif URIRef(change_type) == URIRef(OCH_ADD_DISJOINT_PROPERTY):
                if output_shacl is not None:
                    add_disjoint_property_shacl(change_result["change"], change_data, output_shacl)
            elif URIRef(change_type) == URIRef(OCH_REMOVE_DISJOINT_PROPERTY):
                if output_shacl is not None:
                    remove_disjoint_property_shacl(change_result["change"], change_data, output_shacl)
            elif URIRef(change_type) == URIRef(OCH_ADD_SUBPROPERTY):
                if output_shacl is not None:
                    add_superproperty_shacl(change_result["change"], change_data, output_shacl)
            elif URIRef(change_type) == URIRef(OCH_REMOVE_SUBPROPERTY):
                if output_shacl is not None:
                    remove_superproperty_shacl(change_result["change"], change_data, output_shacl)
            elif URIRef(change_type) == URIRef(OCH_ADD_EQUIVALENT_PROPERTY):
                if output_shacl is not None:
                    add_equivalent_property_shacl(change_result["change"], change_data, output_shacl)
            elif URIRef(change_type) == URIRef(OCH_REMOVE_EQUIVALENT_PROPERTY):
                if output_shacl is not None:
                    remove_equivalent_property_shacl(change_result["change"], change_data, output_shacl)

    logger.info("Changes propagated over semantic artefacts, writing results...")
    return output_mappings, output_shacl