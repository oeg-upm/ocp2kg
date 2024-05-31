from rdflib import Graph, URIRef, Variable

import yatter
from constants import *
from ruamel.yaml import YAML
import argparse


# ---------------------------------------------------------------------------------------------------------------------------

def add_class(change):
    """
    Adds a class defined in the change KG into the output_mappings.
    If there is a TriplesMap that creates instances of that class, the TriplesMap is not created
    Args:
        change: the URI of the change which needs to be of the type AddClass
    Returns:
        the output_mappings updated with a new class
    """
    select_change = f' SELECT DISTINCT ?class WHERE {{' \
                    f' <{change}> {OCH_ADDED_CLASS} ?class .}} '

    results = change_data.query(select_change)
    added_class = results.bindings[0][Variable('class')]
    check_query = f'ASK {{  ?triples_map {RDF_TYPE} {R2RML_TRIPLES_MAP} .' \
                  f'        ?triples_map {R2RML_SUBJECT} ?subject . ' \
                  f'        ?subject {R2RML_CLASS} <{added_class}> }}'

    check_res = output_mappings.query(check_query)
    if not check_res.askAnswer:
        triples_map_id = f'{added_class.split("#")[1]}_TM'
        insert_class_query = f' PREFIX {R2RML_PREFIX}: <{R2RML_URI}>' \
                             f' PREFIX {RML_PREFIX}: <{RML_URI}>' \
                             f' INSERT DATA {{' \
                             f'     <{triples_map_id}> {RDF_TYPE} {R2RML_TRIPLES_MAP}; ' \
                             f'        {RML_LOGICAL_SOURCE} [ ' \
                             f'             {RML_SOURCE} "XXXX"; ' \
                             f'             {RML_REFERENCE_FORMULATION} "XXXX" ' \
                             f'         ]; ' \
                             f'         {R2RML_SUBJECT} [ ' \
                             f'             {R2RML_TEMPLATE} "XXXX"; ' \
                             f'             {R2RML_CLASS} <{added_class}> ' \
                             f'         ]. }} '
        output_mappings.update(insert_class_query)
    else:
        print(f'The input mappings already has rules to create instances of {added_class}.')


# ---------------------------------------------------------------------------------------------------------------------------
def remove_class(change):
    """
        Remove a class defined in the change KG into the output_mappings.
        If there is a TriplesMap that creates instances of that class, the TriplesMap and associated POM are removed.
        Referenced TriplesMaps POMs are also removed.
        Args:
            change: the URI of the change which needs to be of the type AddClass
        Returns:
            the output_mappings updated with the data
        """
    # ToDo: Check if the class is a subclass of others to let the KE about the removals
    query = f' SELECT DISTINCT ?class_name WHERE {{ ' \
            f'      <{change}> {OCH_DELETED_CLASS} ?class_name . }}'

    for result in change_data.query(query):
        class_name = result["class_name"]
        query = f' PREFIX {R2RML_PREFIX}: <{R2RML_URI}>' \
                f' PREFIX {RML_PREFIX}: <{RML_URI}>' \
                f' DELETE {{' \
                f'      ?triples_map {R2RML_SUBJECT} ?subject.' \
                f'      ?subject ?subject_term ?subject_value .' \
                f'      ?subject {R2RML_CLASS} <{class_name}> .' \
                f'      ?triples_map {RML_LOGICAL_SOURCE} ?logical_source .' \
                f'      ?logical_source ?logical_source_term ?logical_source_value .' \
                f'      ?triples_map {R2RML_PREDICATE_OBJECT_MAP} ?pom. ' \
                f'      ?pom ?predicate_property ?predicate . ' \
                f'      ?predicate ?predicate_term ?predicate_value . ' \
                f'      ?pom ?object_property ?object. ' \
                f'      ?object ?object_term ?object_value.' \
                f'      ?object {R2RML_PARENT_TRIPLESMAP} ?parent_tm . ' \
                f'      ?object {R2RML_JOIN_CONDITION} ?join_condition . ' \
                f'      ?join_condition ?condition_term ?condition_value . ' \
                f'      ?parent_triples_map {R2RML_PREDICATE_OBJECT_MAP} ?parent_pom . ' \
                f'      ?parent_pom ?parent_predicate_property ?parent_predicate .' \
                f'      ?parent_predicate ?parent_predicate_term ?parent_predicate_value .' \
                f'      ?parent_pom {R2RML_OBJECT} ?parent_object . ' \
                f'      ?parent_object {R2RML_PARENT_TRIPLESMAP} ?triples_map . ' \
                f'      ?parent_object {R2RML_JOIN_CONDITION} ?parent_join_conditions . ' \
                f'      ?parent_join_conditions ?parent_condition_term ?parent_conditions_value .}} ' \
                f' WHERE {{ ' \
                f'      ?triples_map {R2RML_SUBJECT} ?subject.' \
                f'      ?subject ?subject_term ?subject_value .' \
                f'      ?subject {R2RML_CLASS} <{class_name}> .' \
                f'      ?triples_map {RML_LOGICAL_SOURCE} ?logical_source .' \
                f'      ?logical_source ?logical_source_term ?logical_source_value .' \
                f'      OPTIONAL {{ ' \
                f'          ?triples_map {R2RML_PREDICATE_OBJECT_MAP} ?pom.' \
                f'          ?pom {R2RML_SHORTCUT_PREDICATE}|{R2RML_PREDICATE} ?predicate .' \
                f'          OPTIONAL {{ ?predicate ?predicate_term ?predicate_value . }}' \
                f'          ?pom {R2RML_SHORTCUT_OBJECT}|{R2RML_OBJECT} ?object .' \
                f'          OPTIONAL {{ ?object ?object_term ?object_value. }}' \
                f'          OPTIONAL {{' \
                f'              ?object {R2RML_PARENT_TRIPLESMAP} ?parent_tm .' \
                f'              OPTIONAL {{ ' \
                f'                  ?object {R2RML_JOIN_CONDITION} ?join_condition . ' \
                f'                  ?join_condition ?condition_term ?condition_value .' \
                f'              }}' \
                f'          }}' \
                f'      }} ' \
                f'      OPTIONAL {{ ' \
                f'          ?parent_triples_map {R2RML_PREDICATE_OBJECT_MAP} ?parent_pom.' \
                f'          ?parent_pom {R2RML_SHORTCUT_PREDICATE}|{R2RML_PREDICATE} ?parent_predicate .' \
                f'          OPTIONAL {{ ?parent_predicate ?parent_predicate_term ?parent_predicate_value . }}' \
                f'          ?parent_pom {R2RML_OBJECT} ?parent_object .' \
                f'          ?parent_object {R2RML_PARENT_TRIPLESMAP} ?triples_map .' \
                f'          OPTIONAL {{ ' \
                f'              ?parent_object {R2RML_JOIN_CONDITION} ?parent_join_conditions . ' \
                f'              ?parent_join_conditions ?parent_condition_term ?parent_conditions_value .' \
                f'          }}' \
                f'      }} '

        output_mappings.update(query)


# ---------------------------------------------------------------------------------------------------------------------------------

def add_super_class(change):
    """
       Adds a superclass and its properties into the TriplesMap that instantiate the subclass .
       Args:
           change: the URI of the change which needs to be of the type add_sub_class
       Returns:
           the output_mappings updated with the TriplesMap of child adding the parent class and its properties
    """
    super_class = None
    sub_class = None
    query = f' SELECT DISTINCT ?super_class ?sub_class WHERE {{ ' \
            f'      <{change}> {OCH_ADD_SUBCLASS_DOMAIN} ?sub_class. ' \
            f'      <{change}> {OCH_ADD_SUBCLASS_RANGE} ?super_class. }}'

    for result in change_data.query(query):
        sub_class = result["sub_class"]
        super_class = result["super_class"]
        insert_super_class_query = f' PREFIX {R2RML_PREFIX}: <{R2RML_URI}>' \
                                   f' PREFIX {RML_PREFIX}: <{RML_URI}>' \
                                   f' INSERT {{ ?subjectMap {R2RML_CLASS} <{super_class}>. }}' \
                                   f' WHERE {{' \
                                   f'     ?triplesMap {R2RML_SUBJECT} ?subjectMap. ' \
                                   f'     ?subjectMap {R2RML_CLASS} <{sub_class}>. }}'

        output_mappings.update(insert_super_class_query)

    if super_class and sub_class:
        query_data_properties = f' SELECT DISTINCT ?dataproperty ?range WHERE {{' \
                                f'     ?dataproperty {RDF_TYPE} {OWL_DATA_PROPERTY}.' \
                                f'     ?dataproperty {RDFS_DOMAIN} <{super_class}> .' \
                                f'     ?dataproperty {RDFS_RANGE} ?range.}}'

        for result in ontology.query(query_data_properties): # ToDo: removes references to the ontology
            dataproperty = result["dataproperty"]
            property_range = result["range"]

            insert_data_property_query = f' PREFIX {R2RML_PREFIX}: <{R2RML_URI}>' \
                                         f' PREFIX {RML_PREFIX}: <{RML_URI}>' \
                                         f' INSERT {{  ' \
                                         f'     ?triplesMap {R2RML_PREDICATE_OBJECT_MAP} [ ' \
                                         f'         {R2RML_PREDICATE} <{dataproperty}> ; ' \
                                         f'         {R2RML_OBJECT} [ ' \
                                         f'             {RML_REFERENCE} "XXXX";' \
                                         f'             {R2RML_DATATYPE} <{property_range}>' \
                                         f'          ] ]. }}' \
                                         f'  WHERE {{' \
                                         f'     ?triplesMap {R2RML_SUBJECT} ?subjectMap . ' \
                                         f'     ?subjectMap {R2RML_CLASS} <{super_class}>, <{sub_class}> . }} '
            output_mappings.update(insert_data_property_query)

        query_object_properties = f' SELECT DISTINCT ?objectproperty ?range WHERE {{' \
                                  f'     ?objectproperty {RDF_TYPE} {OWL_OBJECT_PROPERTY}.' \
                                  f'     ?objectproperty {RDFS_DOMAIN} <{super_class}> .' \
                                  f'     ?objectproperty {RDFS_RANGE} ?range.}}'

        for result in ontology.query(query_object_properties): # ToDo: removes references to the ontology
            object_property = result["objectproperty"]
            property_range = result["range"]

            insert_object_property_query = f' PREFIX {R2RML_PREFIX}: <{R2RML_URI}>' \
                                           f' PREFIX {RML_PREFIX}: <{RML_URI}>' \
                                           f' INSERT {{  ' \
                                           f'     ?triplesMap {R2RML_PREDICATE_OBJECT_MAP} [ ' \
                                           f'         {R2RML_PREDICATE} <{object_property}> ; ' \
                                           f'         {R2RML_OBJECT} [ ' \
                                           f'             {R2RML_PARENT_TRIPLESMAP} ?parent_triplesMap;' \
                                           f'             {R2RML_JOIN_CONDITION} [ ' \
                                           f'               {R2RML_CHILD} "XXXX"; {R2RML_PARENT} "XXXX" ' \
                                           f'          ] ] ]. }}' \
                                           f'  WHERE {{' \
                                           f'     ?triplesMap {R2RML_SUBJECT} ?subjectMap . ' \
                                           f'     ?subjectMap {R2RML_CLASS} <{super_class}>, <{sub_class}> .' \
                                           f'     ?parent_triplesMap {R2RML_SUBJECT} ?parent_subjectMap . ' \
                                           f'     ?parent_subjectMap {R2RML_CLASS} {property_range} }}'

            output_mappings.update(insert_object_property_query)


# --------------------------------------------------------------------------------------------------------------
def remove_super_class(change):
    # When removing the subclass relationship between two classes the child one loses the parent in the rr:class part.
    query = f'SELECT DISTINCT ?super_class ?sub_class WHERE {{ ' \
            f' <{change}> {OCH_REMOVE_SUBCLASS_DOMAIN} ?sub_class.' \
            f' <{change}> {OCH_REMOVE_SUBCLASS_RANGE} ?super_class. }}'

    for result in change_data.query(query):
        super_class = result["super_class"]
        sub_class = result["sub_class"]
        delete_super_class_query = f' PREFIX {R2RML_PREFIX}: <{R2RML_URI}>' \
                                   f' PREFIX {RML_PREFIX}: <{RML_URI}>' \
                                   f' DELETE {{ ?subjectMap {R2RML_CLASS} <{super_class}> }}' \
                                   f' WHERE {{ ' \
                                   f'       ?triplesMap {R2RML_SUBJECT} ?subjectMap . ' \
                                   f'       ?triplesMap {R2RML_CLASS} <{super_class}>, <{sub_class}> .}}'

        output_mappings.update(delete_super_class_query)

        inherit_data_properties_query = f' SELECT DISTINCT ?data_property WHERE {{' \
                                        f'     ?dataProperty {RDF_TYPE} {OWL_DATA_PROPERTY} . ' \
                                        f'     ?dataProperty {RDFS_DOMAIN} <{super_class}>, {sub_class}. }}'

        for result2 in ontology.query(inherit_data_properties_query):  # ToDo: removes references to the ontology
            data_property = result2["data_property"]
            remove_data_property_query = f' PREFIX {R2RML_PREFIX}: <{R2RML_URI}>' \
                                         f' PREFIX {RML_PREFIX}: <{RML_URI}>' \
                                         f' DELETE {{' \
                                         f'     ?triplesMap {R2RML_PREDICATE_OBJECT_MAP} ?pom.' \
                                         f'     ?pom {R2RML_SHORTCUT_PREDICATE} <{data_property}> .' \
                                         f'     ?pom ?object_property ?objectMap.' \
                                         f'     ?objectMap ?object_term ?objectValue .}}' \
                                         f' WHERE {{' \
                                         f'     ?triplesMap {R2RML_SUBJECT} ?subjectMap.' \
                                         f'     ?subjectMap {R2RML_CLASS} <{sub_class}> . ' \
                                         f'     ?triplesMap {R2RML_PREDICATE_OBJECT_MAP} ?pom .' \
                                         f'     ?pom {R2RML_SHORTCUT_PREDICATE} <{data_property}> .' \
                                         f'     ?pom {R2RML_OBJECT}|{R2RML_SHORTCUT_OBJECT} ?objectMap .' \
                                         f'     OPTIONAL {{ ?objectMap ?object_term ?objectValue }} . }}'

            output_mappings.update(remove_data_property_query)

        inherit_object_properties_query = f' SELECT DISTINCT ?object_property WHERE {{' \
                                          f'     ?object_property  {RDF_TYPE} {OWL_OBJECT_PROPERTY}.' \
                                          f'     ?object_property {RDFS_DOMAIN} <{super_class}>, <{sub_class}>. }} '
        for results in ontology.query(inherit_object_properties_query):
            object_property = results["object_property"]
            remove_object_property_query = f' PREFIX {R2RML_PREFIX}: <{R2RML_URI}>' \
                                           f' PREFIX {RML_PREFIX}: <{RML_URI}>' \
                                           f' DELETE {{' \
                                           f'     ?triplesMap {R2RML_PREDICATE_OBJECT_MAP} ?pom.' \
                                           f'     ?pom {R2RML_SHORTCUT_PREDICATE} <{object_property}> .' \
                                           f'     ?pom {R2RML_OBJECT} ?objectMap.' \
                                           f'     ?objectMap {R2RML_PARENT_TRIPLESMAP} ?parentTriplesMap . ' \
                                           f'     ?objectMap {R2RML_JOIN_CONDITION} ?joinConditions . ' \
                                           f'     ?joinConditions ?conditions ?condition_values }} . ' \
                                           f' WHERE {{' \
                                           f'     ?triplesMap {R2RML_SUBJECT} ?subjectMap.' \
                                           f'     ?subjectMap {R2RML_CLASS} <{sub_class}> . ' \
                                           f'     ?triplesMap {R2RML_PREDICATE_OBJECT_MAP} ?pom .' \
                                           f'     ?pom {R2RML_SHORTCUT_PREDICATE} <{object_property}> .' \
                                           f'     ?pom {R2RML_OBJECT} ?objectMap .' \
                                           f'     ?objectMap {R2RML_PARENT_TRIPLESMAP} ?parentTriplesMap .' \
                                           f'     OPTIONAL {{ ?objectMap {R2RML_JOIN_CONDITION} ?joinConditions .' \
                                           f'                 ?joinConditions ?conditions ?condition_values . }} }}'

            output_mappings.update(remove_object_property_query)
        # ToDo Remove the object_properties where super_class is the range (i.e. RefObjectMap)


def add_object_property(change):
    """
       Adds an object property to the TriplesMap indicated in the domain.
       Args:
           change: the URI of the change which needs to be of the type addObjectProperty
       Returns:
           the output_mappings updated with the
    """
    query = f' SELECT DISTINCT ?domain ?property ?range WHERE {{ ' \
            f' <{change}> {OCH_ADD_OBJECT_PROPERTY_DOMAIN} ?domain .' \
            f' <{change}> {OCH_ADD_OBJECT_PROPERTY_PROPERTY} ?property .' \
            f' <{change}> {OCH_ADD_OBJECT_PROPERTY_RANGE} ?range .}}'

    for result in change_data.query(query):
        property_domain = result["domain"]
        property_predicate = result["property"]
        property_range = result["range"]

        insert_object_property_query = f' PREFIX {R2RML_PREFIX}: <{R2RML_URI}>' \
                                       f' PREFIX {RML_PREFIX}: <{RML_URI}>' \
                                       f' INSERT {{  ' \
                                       f'     ?triplesMap {R2RML_PREDICATE_OBJECT_MAP} [ ' \
                                       f'         {R2RML_PREDICATE} <{property_predicate}> ; ' \
                                       f'         {R2RML_OBJECT} [ ' \
                                       f'             {R2RML_PARENT_TRIPLESMAP} ?parent_triplesMap;' \
                                       f'             {R2RML_JOIN_CONDITION} [ ' \
                                       f'               {R2RML_CHILD} "XXXX"; {R2RML_PARENT} "XXXX" ' \
                                       f'          ] ] ]. }}' \
                                       f'  WHERE {{' \
                                       f'     ?triplesMap {R2RML_SUBJECT} ?subjectMap . ' \
                                       f'     ?subjectMap {R2RML_CLASS} <{property_domain}> .' \
                                       f'     ?parent_triplesMap {R2RML_SUBJECT} ?parent_subjectMap . ' \
                                       f'     ?parent_subjectMap {R2RML_CLASS} {property_range} }}'

        output_mappings.update(insert_object_property_query)


# --------------------------------------------------------------------------------------------------------------------------------------------------
def remove_object_property(change):
    """
        Removes the object property indicated in the change as property from its domain
        Args:
           change: the URI of the change which needs to be of the type addObjectProperty
        Returns:
           the output_mappings updated with the reference predicate object mapping removed
    """
    query = f' SELECT DISTINCT ?domain ?property WHERE {{ ' \
            f' <{change}> {OCH_REMOVE_OBJECT_PROPERTY_DOMAIN} ?domain.' \
            f' <{change}> {OCH_REMOVE_OBJECT_PROPERTY_DOMAIN} ?property. }}'

    for result in change_data.query(query):
        property_domain = result["domain"]
        property_predicate = result["property"]
        remove_object_property_query = f' PREFIX {R2RML_PREFIX}: <{R2RML_URI}>' \
                                       f' PREFIX {RML_PREFIX}: <{RML_URI}>' \
                                       f' DELETE {{' \
                                       f'     ?triplesMap {R2RML_PREDICATE_OBJECT_MAP} ?pom.' \
                                       f'     ?pom {R2RML_SHORTCUT_PREDICATE} <{property_predicate}> .' \
                                       f'     ?pom {R2RML_OBJECT} ?objectMap.' \
                                       f'     ?objectMap {R2RML_PARENT_TRIPLESMAP} ?parentTriplesMap . ' \
                                       f'     ?objectMap {R2RML_JOIN_CONDITION} ?joinConditions . ' \
                                       f'     ?joinConditions ?conditions ?condition_values }} . ' \
                                       f' WHERE {{' \
                                       f'     ?triplesMap {R2RML_SUBJECT} ?subjectMap.' \
                                       f'     ?subjectMap {R2RML_CLASS} <{property_domain}> . ' \
                                       f'     ?triplesMap {R2RML_PREDICATE_OBJECT_MAP} ?pom .' \
                                       f'     ?pom {R2RML_SHORTCUT_PREDICATE} <{property_predicate}> .' \
                                       f'     ?pom {R2RML_OBJECT} ?objectMap .' \
                                       f'     ?objectMap {R2RML_PARENT_TRIPLESMAP} ?parentTriplesMap .' \
                                       f'     OPTIONAL {{ ?objectMap {R2RML_JOIN_CONDITION} ?joinConditions .' \
                                       f'                 ?joinConditions ?conditions ?condition_values }} . }}'

        output_mappings.update(remove_object_property_query)


# -------------------------------------------------------------------------------------------------------------------------
def add_data_property(change):
    """
       Adds a data property to the TriplesMap indicated in the domain. Ragne is extracted from the input ontology
       Args:
           change: the URI of the change which needs to be of the type addObjectProperty
       Returns:
           the output_mappings updated with the new predicate object map with empty reference
    """
    query = f' SELECT DISTINCT ?domain ?property WHERE {{ ' \
            f' <{change}> {OCH_ADD_DATA_PROPERTY_DOMAIN} ?domain. ' \
            f' <{change}> {OCH_ADD_DATA_PROPERTY_PROPERTY} ?property. }}'

    for result in change_data.query(query):
        property_domain = result["domain"]
        property_predicate = result["property"]
        q2 = f' SELECT DISTINCT ?property_range WHERE {{ ' \
             f' <{property_predicate} {RDFS_RANGE} ?property_range. }}'
        property_range = None
        for results2 in ontology.query(q2):  # ToDo: removes references to the ontology
            property_range = results2["property_range"]

        if property_range:
            insert_data_property_query = f' PREFIX {R2RML_PREFIX}: <{R2RML_URI}>' \
                                         f' PREFIX {RML_PREFIX}: <{RML_URI}>' \
                                         f' INSERT {{  ' \
                                         f'     ?triplesMap {R2RML_PREDICATE_OBJECT_MAP} [ ' \
                                         f'         {R2RML_PREDICATE} <{property_predicate}> ; ' \
                                         f'         {R2RML_OBJECT} [ ' \
                                         f'             {RML_REFERENCE} "XXXX";' \
                                         f'             {R2RML_DATATYPE} <{property_range}>' \
                                         f'          ] ]. }}' \
                                         f'  WHERE {{' \
                                         f'     ?triplesMap {R2RML_SUBJECT} ?subjectMap . ' \
                                         f'     ?subjectMap {R2RML_CLASS} <{property_domain}> . }} '

        else:
            insert_data_property_query = f' PREFIX {R2RML_PREFIX}: <{R2RML_URI}>' \
                                         f' PREFIX {RML_PREFIX}: <{RML_URI}>' \
                                         f' INSERT {{  ' \
                                         f'     ?triplesMap {R2RML_PREDICATE_OBJECT_MAP} [ ' \
                                         f'         {R2RML_PREDICATE} <{property_predicate}> ; ' \
                                         f'         {R2RML_OBJECT} [ ' \
                                         f'             {RML_REFERENCE} "XXXX";' \
                                         f'          ] ]. }}' \
                                         f'  WHERE {{' \
                                         f'     ?triplesMap {R2RML_SUBJECT} ?subjectMap . ' \
                                         f'     ?subjectMap {R2RML_CLASS} <{property_domain}> . }} '

        output_mappings.update(insert_data_property_query)


# -----------------------------------------------------------------------------------------------------------------------------------
def remove_data_property(change):
    """
        Removes the data property indicated in the change as property from its domain
        Args:
           change: the URI of the change which needs to be of the type addObjectProperty
        Returns:
           the output_mappings updated with the predicate object mapping removed
    """
    query = f' SELECT DISTINCT ?domain ?property WHERE {{ ' \
            f' <{change}> {OCH_REMOVE_DATA_PROPERTY_DOMAIN} ?domain.' \
            f' <{change}> {OCH_REMOVE_DATA_PROPERTY_PROPERTY} ?property.'

    for result in change_data.query(query):
        property_domain = result["domain"]
        property_predicate = result["property"]

        remove_data_property_query = f' PREFIX {R2RML_PREFIX}: <{R2RML_URI}>' \
                                     f' PREFIX {RML_PREFIX}: <{RML_URI}>' \
                                     f' DELETE {{' \
                                     f'     ?triplesMap {R2RML_PREDICATE_OBJECT_MAP} ?pom.' \
                                     f'     ?pom {R2RML_SHORTCUT_PREDICATE} <{property_predicate}> .' \
                                     f'     ?pom ?object_property ?objectMap.' \
                                     f'     ?objectMap ?object_term ?objectValue .}}' \
                                     f' WHERE {{' \
                                     f'     ?triplesMap {R2RML_SUBJECT} ?subjectMap.' \
                                     f'     ?subjectMap {R2RML_CLASS} <{property_domain}> . ' \
                                     f'     ?triplesMap {R2RML_PREDICATE_OBJECT_MAP} ?pom .' \
                                     f'     ?pom {R2RML_SHORTCUT_PREDICATE} <{property_predicate}> .' \
                                     f'     ?pom {R2RML_OBJECT}|{R2RML_SHORTCUT_OBJECT} ?objectMap .' \
                                     f'     OPTIONAL {{ ?objectMap ?object_term ?objectValue }} . }}'

        output_mappings.update(remove_data_property_query)


# -------------------------------------------------------------------------------------------------------------


def define_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--changes_kg_path", required=True, help="Change KG following the Change Ontology")
    parser.add_argument("-m", "--old_mapping_path", required=True, help="Old version of the mappings in RML")
    parser.add_argument("-o", "--ontology_path", required=False, help="New version of the ontology")
    parser.add_argument("-n", "--new_mappings_path", required=True, help="Output path for the generated mapping")
    parser.add_argument("-y", "--yarrrml", nargs=argparse.OPTIONAL, required=False, help="Mappings are also converted into YARRRML")
    return parser


if __name__ == "__main__":
    logger.info("Starting the propagation of changes over the mapping rules")
    args = define_args().parse_args()
    change_data = Graph().parse(args.changes_kg_path, format="ttl")

    if args.old_mapping_path.endswith(".yml") or args.old_mapping_path.endswith(".yaml"):
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
    yarrrml_content = yatter.inverse_translation(output_mappings)
    with open(args.new_mappings_path.replace(".ttl", ".yml"), "wb") as f:
        yaml = YAML()
        yaml.default_flow_style = False
        yaml.width = 3000
        yaml.dump(yarrrml_content, f)
