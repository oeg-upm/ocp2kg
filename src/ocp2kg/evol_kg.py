from rdflib import URIRef, Variable
from .constants import *
import os


# ---------------------------------------------------------------------------------------------------------------------------

def add_class_rml(change, change_data, output_mappings):
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
                             f'     <{EXAMPLE_URI}{triples_map_id}> {RDF_TYPE} {R2RML_TRIPLES_MAP}; ' \
                             f'        {RML_LOGICAL_SOURCE} [ ' \
                             f'             {RML_SOURCE} "XXX"; ' \
                             f'             {RML_REFERENCE_FORMULATION} "XXX" ' \
                             f'         ]; ' \
                             f'         {R2RML_SUBJECT} [ ' \
                             f'             {R2RML_TEMPLATE} "XXX"; ' \
                             f'             {R2RML_CLASS} <{added_class}> ' \
                             f'         ]. }} '
        output_mappings.update(insert_class_query)
    else:
        print(f'The input mappings already has rules to create instances of {added_class}.')


# ---------------------------------------------------------------------------------------------------------------------------
def remove_class_rml(change,change_data, output_mappings, review_mappings, ontology):
    """
        Remove a class defined in the change KG into the output_mappings.
        If there is a TriplesMap that creates instances of that class, the TriplesMap and associated POM are removed.
        Referenced TriplesMaps POMs are also removed.
        When the removed class is the sbclass of another class then the deleted PredicateObjectMaps are inserted into a different 
        document so that the KGE can review it, and move those to the parent class.  
        Args:
            change: the URI of the change which needs to be of the type AddClass
        Returns:
            the output_mappings updated with the data
        """
    query = f' SELECT DISTINCT ?class_name WHERE {{ ' \
            f'      <{change}> {OCH_DELETED_CLASS} ?class_name . }}'

    for result in change_data.query(query):
        class_name = result["class_name"]
        query = f' ASK {{<{class_name}> {RDFS_SUBCLASS} ?parent}} '
        for result in ontology.query(query):
            if result is True:
                query = f' PREFIX {R2RML_PREFIX}: <{R2RML_URI}>' \
                    f' PREFIX {RML_PREFIX}: <{RML_URI}>' \
                    f' CONSTRUCT {{' \
                    f'      ?triples_map {RDF_TYPE} {R2RML_TRIPLES_MAP}.' \
                    f'      ?triples_map {R2RML_SUBJECT} ?subject.' \
                    f'      ?subject ?subject_term ?subject_value .' \
                    f'      ?subject {R2RML_CLASS} <{class_name}> .' \
                    f'      ?triples_map {RML_LOGICAL_SOURCE} ?logical_source .' \
                    f'      ?logical_source ?logical_source_term ?logical_source_value .' \
                    f'      ?triples_map {R2RML_PREDICATE_OBJECT_MAP} ?pom. ' \
                    f'      ?pom  {R2RML_SHORTCUT_PREDICATE} ?predicate . ' \
                    f'      ?pom {R2RML_PREDICATE} ?predicate_bn . ' \
                    f'      ?predicate_bn ?predicate_term ?predicate_value . ' \
                    f'      ?pom {R2RML_SHORTCUT_OBJECT} ?object. ' \
                    f'      ?pom {R2RML_OBJECT} ?object_bn . ' \
                    f'      ?object_bn ?object_term ?object_value.' \
                    f'      ?object_bn {R2RML_PARENT_TRIPLESMAP} ?parent_tm . ' \
                    f'      ?object_bn {R2RML_JOIN_CONDITION} ?join_condition . ' \
                    f'      ?join_condition ?condition_term ?condition_value . ' \
                    f'      ?parent_triples_map {R2RML_PREDICATE_OBJECT_MAP} ?parent_pom . ' \
                    f'      ?parent_pom {R2RML_SHORTCUT_PREDICATE} ?parent_predicate .' \
                    f'      ?parent_pom {R2RML_PREDICATE} ?parent_predicate_bn .' \
                    f'      ?parent_predicate_bn ?parent_predicate_term ?parent_predicate_value .' \
                    f'      ?parent_pom {R2RML_OBJECT} ?parent_object . ' \
                    f'      ?parent_object {R2RML_PARENT_TRIPLESMAP} ?triples_map . ' \
                    f'      ?parent_object {R2RML_JOIN_CONDITION} ?parent_join_conditions . ' \
                    f'      ?parent_join_conditions ?parent_condition_term ?parent_conditions_value .}} ' \
                    f' WHERE {{ ' \
                    f'      ?triples_map {RDF_TYPE} {R2RML_TRIPLES_MAP}.' \
                    f'      ?triples_map {R2RML_SUBJECT} ?subject.' \
                    f'      ?subject ?subject_term ?subject_value .' \
                    f'      ?subject {R2RML_CLASS} <{class_name}> .' \
                    f'      ?triples_map {RML_LOGICAL_SOURCE} ?logical_source .' \
                    f'      ?logical_source ?logical_source_term ?logical_source_value .' \
                    f'      OPTIONAL {{ ' \
                    f'          ?triples_map {R2RML_PREDICATE_OBJECT_MAP} ?pom.' \
                    f'          OPTIONAL {{?pom {R2RML_SHORTCUT_PREDICATE} ?predicate . }}' \
                    f'          OPTIONAL {{   ?pom {R2RML_PREDICATE} ?predicate_bn.'\
                    f'                        ?predicate_bn ?predicate_term ?predicate_value . }}' \
                    f'          OPTIONAL {{?pom {R2RML_SHORTCUT_OBJECT} ?object .}}' \
                    f'          OPTIONAL {{?pom {R2RML_OBJECT} ?object_bn .' \
                    f'                      ?object_bn ?object_term ?object_value. }}' \
                    f'          OPTIONAL {{' \
                    f'              ?object_bn {R2RML_PARENT_TRIPLESMAP} ?parent_tm .' \
                    f'              OPTIONAL {{ ' \
                    f'                  ?object_bn {R2RML_JOIN_CONDITION} ?join_condition . ' \
                    f'                  ?join_condition ?condition_term ?condition_value .' \
                    f'              }}' \
                    f'          }}' \
                    f'    }}' \
                    f'      OPTIONAL {{ ' \
                    f'          ?parent_triples_map {R2RML_PREDICATE_OBJECT_MAP} ?parent_pom.' \
                    f'          OPTIONAL {{?parent_pom {R2RML_SHORTCUT_PREDICATE} ?parent_predicate .}}' \
                    f'          OPTIONAL {{     ?parent_pom {R2RML_PREDICATE} ?parent_predicate_bn.'\
                    f'                          ?parent_predicate_bn ?parent_predicate_term ?parent_predicate_value . }}' \
                    f'          ?parent_pom {R2RML_OBJECT} ?parent_object .' \
                    f'          ?parent_object {R2RML_PARENT_TRIPLESMAP} ?triples_map .' \
                    f'          OPTIONAL {{ ' \
                    f'              ?parent_object {R2RML_JOIN_CONDITION} ?parent_join_conditions . ' \
                    f'              ?parent_join_conditions ?parent_condition_term ?parent_conditions_value .' \
                    f'          }}' \
                    f'      }} ' \
                    f'  }}'
                hola=output_mappings.query(query)
                for row in hola:
                    review_mappings.add(row)

            query = f' PREFIX {R2RML_PREFIX}: <{R2RML_URI}>' \
                    f' PREFIX {RML_PREFIX}: <{RML_URI}>' \
                    f' DELETE {{' \
                    f'      ?triples_map {RDF_TYPE} {R2RML_TRIPLES_MAP}.' \
                    f'      ?triples_map {R2RML_SUBJECT} ?subject.' \
                    f'      ?subject ?subject_term ?subject_value .' \
                    f'      ?subject {R2RML_CLASS} <{class_name}> .' \
                    f'      ?triples_map {RML_LOGICAL_SOURCE} ?logical_source .' \
                    f'      ?logical_source ?logical_source_term ?logical_source_value .' \
                    f'      ?triples_map {R2RML_PREDICATE_OBJECT_MAP} ?pom. ' \
                    f'      ?pom  {R2RML_SHORTCUT_PREDICATE} ?predicate . ' \
                    f'      ?pom {R2RML_PREDICATE} ?predicate_bn . ' \
                    f'      ?predicate_bn ?predicate_term ?predicate_value . ' \
                    f'      ?pom {R2RML_SHORTCUT_OBJECT} ?object. ' \
                    f'      ?pom {R2RML_OBJECT} ?object_bn . ' \
                    f'      ?object_bn ?object_term ?object_value.' \
                    f'      ?object_bn {R2RML_PARENT_TRIPLESMAP} ?parent_tm . ' \
                    f'      ?object_bn {R2RML_JOIN_CONDITION} ?join_condition . ' \
                    f'      ?join_condition ?condition_term ?condition_value . ' \
                    f'      ?parent_triples_map {R2RML_PREDICATE_OBJECT_MAP} ?parent_pom . ' \
                    f'      ?parent_pom {R2RML_SHORTCUT_PREDICATE} ?parent_predicate .' \
                    f'      ?parent_pom {R2RML_PREDICATE} ?parent_predicate_bn .' \
                    f'      ?parent_predicate_bn ?parent_predicate_term ?parent_predicate_value .' \
                    f'      ?parent_pom {R2RML_OBJECT} ?parent_object . ' \
                    f'      ?parent_object {R2RML_PARENT_TRIPLESMAP} ?triples_map . ' \
                    f'      ?parent_object {R2RML_JOIN_CONDITION} ?parent_join_conditions . ' \
                    f'      ?parent_join_conditions ?parent_condition_term ?parent_conditions_value .}} ' \
                    f' WHERE {{ ' \
                    f'      ?triples_map {RDF_TYPE} {R2RML_TRIPLES_MAP}.' \
                    f'      ?triples_map {R2RML_SUBJECT} ?subject.' \
                    f'      ?subject ?subject_term ?subject_value .' \
                    f'      ?subject {R2RML_CLASS} <{class_name}> .' \
                    f'      ?triples_map {RML_LOGICAL_SOURCE} ?logical_source .' \
                    f'      ?logical_source ?logical_source_term ?logical_source_value .' \
                    f'      OPTIONAL {{ ' \
                    f'          ?triples_map {R2RML_PREDICATE_OBJECT_MAP} ?pom.' \
                    f'          OPTIONAL {{?pom {R2RML_SHORTCUT_PREDICATE} ?predicate . }}' \
                    f'          OPTIONAL {{   ?pom {R2RML_PREDICATE} ?predicate_bn.'\
                    f'                        ?predicate_bn ?predicate_term ?predicate_value . }}' \
                    f'          OPTIONAL {{?pom {R2RML_SHORTCUT_OBJECT} ?object .}}' \
                    f'          OPTIONAL {{?pom {R2RML_OBJECT} ?object_bn .' \
                    f'                      ?object_bn ?object_term ?object_value. }}' \
                    f'          OPTIONAL {{' \
                    f'              ?object_bn {R2RML_PARENT_TRIPLESMAP} ?parent_tm .' \
                    f'              OPTIONAL {{ ' \
                    f'                  ?object_bn {R2RML_JOIN_CONDITION} ?join_condition . ' \
                    f'                  ?join_condition ?condition_term ?condition_value .' \
                    f'              }}' \
                    f'          }}' \
                    f'    }}' \
                    f'      OPTIONAL {{ ' \
                    f'          ?parent_triples_map {R2RML_PREDICATE_OBJECT_MAP} ?parent_pom.' \
                    f'          OPTIONAL {{?parent_pom {R2RML_SHORTCUT_PREDICATE} ?parent_predicate .}}' \
                    f'          OPTIONAL {{     ?parent_pom {R2RML_PREDICATE} ?parent_predicate_bn.'\
                    f'                          ?parent_predicate_bn ?parent_predicate_term ?parent_predicate_value . }}' \
                    f'          ?parent_pom {R2RML_OBJECT} ?parent_object .' \
                    f'          ?parent_object {R2RML_PARENT_TRIPLESMAP} ?triples_map .' \
                    f'          OPTIONAL {{ ' \
                    f'              ?parent_object {R2RML_JOIN_CONDITION} ?parent_join_conditions . ' \
                    f'              ?parent_join_conditions ?parent_condition_term ?parent_conditions_value .' \
                    f'          }}' \
                    f'      }} ' \
                    f'  }}'
            output_mappings.update(query)

# ---------------------------------------------------------------------------------------------------------------------------------

def add_super_class_rml(change,change_data, output_mappings):
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
            f'      <{change}> {OCH_ADD_SUBCLASS_SOURCE} ?sub_class. ' \
            f'      <{change}> {OCH_ADD_SUBCLASS_TARGET} ?super_class. }}'

    for result in change_data.query(query):
        sub_class = result["sub_class"]
        super_class = result["super_class"]
        insert_super_class_query = f' PREFIX {R2RML_PREFIX}: <{R2RML_URI}>' \
                                   f' PREFIX {RML_PREFIX}: <{RML_URI}>' \
                                   f' INSERT {{ ?subjectMap {R2RML_CLASS} <{super_class}>. }}' \
                                   f' WHERE {{' \
                                   f'     ?triplesMap {R2RML_SUBJECT} ?subjectMap. ' \
                                   f'     ?subjectMap {R2RML_CLASS} <{sub_class}>. }}'
        #print(insert_super_class_query)
        output_mappings.update(insert_super_class_query)

    # Query that takes the Predicate Object Maps from the parent class triples map and inserts them into the child triples map.
    """"
    insert_super_class_pom_query =  f' PREFIX {R2RML_PREFIX}: <{R2RML_URI}>' \
                                    f' PREFIX {RML_PREFIX}: <{RML_URI}>' \
                                    f' INSERT {{' \
                                    f'      ?subclass_triples_map {R2RML_PREDICATE_OBJECT_MAP} ?pom. ' \
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
                                    f'      ?parent_object {R2RML_JOIN_CONDITION} ?parent_join_conditions.'\
                                    f'      ?parent_join_conditions ?parent_condition_term ?parent_conditions_value .}} '\
                                    f' WHERE {{ ' \
                                    f'      ?subclass_triples_map {R2RML_SUBJECT} ?subclass_subject.' \
                                    f'      ?subclass_subject {R2RML_CLASS} <{sub_class}>.' \
                                    f'      ?triples_map {R2RML_SUBJECT} ?subject.' \
                                    f'      ?subject {R2RML_CLASS} <{super_class}> .' \
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
                                        f'      }} ' \
                                        f'  }}'
        print(insert_super_class_pom_query)
        output_mappings.update(insert_super_class_pom_query)
"""

# --------------------------------------------------------------------------------------------------------------
def remove_super_class_rml(change,change_data, output_mappings):
    """
       Removes superclass and its properties from the TriplesMap that instantiate the subclass .
       Args:
           change: the URI of the change which needs to be of the type remove_sub_class
       Returns:
           the output_mappings updated with the TriplesMap of child removing the parent class and its properties
    """
    # When removing the subclass relationship between two classes the child one loses the parent in the rr:class part.
    query = f'SELECT DISTINCT ?super_class ?sub_class WHERE {{ ' \
            f' <{change}> {OCH_REMOVE_SUBCLASS_SOURCE} ?sub_class.' \
            f' <{change}> {OCH_REMOVE_SUBCLASS_TARGET} ?super_class. }}'

    for result in change_data.query(query):
        super_class = result["super_class"]
        sub_class = result["sub_class"]
        delete_super_class_query = f' PREFIX {R2RML_PREFIX}: <{R2RML_URI}>' \
                                   f' PREFIX {RML_PREFIX}: <{RML_URI}>' \
                                   f' DELETE {{ ?subjectMap {R2RML_CLASS} <{super_class}> }}' \
                                   f' WHERE {{' \
                                   f'       ?triplesMap {R2RML_SUBJECT} ?subjectMap . ' \
                                   f'       ?subjectMap {R2RML_CLASS} <{super_class}>, <{sub_class}> .}}'
        #print(delete_super_class_query)
        output_mappings.update(delete_super_class_query)

        #Query that takes the Predicate Object Maps from the parent class triples map and inserts them into the child triples map.
        """
        remove_super_class_pom_query =  f' PREFIX {R2RML_PREFIX}: <{R2RML_URI}>' \
                                        f' PREFIX {RML_PREFIX}: <{RML_URI}>' \
                                        f' DELETE {{' \
                                        f'      ?subclass_triples_map {R2RML_PREDICATE_OBJECT_MAP} ?pom. ' \
                                        f'      ?pom {R2RML_SHORTCUT_PREDICATE} ?parent_predicate . ' \
                                        f'      ?pom {R2RML_PREDICATE} ?predicate_bn . ' \
                                        f'      ?predicate_bn ?parent_predicate_term ?parent_predicate_value . ' \
                                        f'      ?pom {R2RML_SHORTCUT_OBJECT} ?parent_object. ' \
                                        f'      ?pom {R2RML_OBJECT} ?object_bn . ' \
                                        f'      ?object_bn ?parent_object_term ?parent_object_value.' \
                                        f'      ?object_bn {R2RML_PARENT_TRIPLESMAP} ?parent_tm . ' \
                                        f'      ?object_bn {R2RML_JOIN_CONDITION} ?join_condition . ' \
                                        f'      ?join_condition ?parent_condition_term ?parent_condition_value . }} ' \
                                        f' WHERE {{ ' \
                                        f'      ?subclass_triples_map {R2RML_SUBJECT} ?subclass_subject.' \
                                        f'      ?subclass_subject {R2RML_CLASS} <{sub_class}>.' \
                                        f'      ?parent_triples_map {R2RML_SUBJECT} ?parent_subject.' \
                                        f'      ?parent_subject {R2RML_CLASS} <{super_class}> .' \
                                        f'      OPTIONAL {{ ' \
                                        f'          ?subclass_triples_map {R2RML_PREDICATE_OBJECT_MAP} ?pom.' \
                                        f'          OPTIONAL {{?pom {R2RML_SHORTCUT_PREDICATE} ?parent_predicate }}' \
                                        f'          OPTIONAL {{ '\
                                        f'                    ?pom {R2RML_PREDICATE} ?predicate_bn . ' \
                                        f'                    ?predicate_bn ?parent_predicate_term ?parent_predicate_value . }}' \
                                        f'          OPTIONAL {{?pom {R2RML_SHORTCUT_OBJECT} ?parent_object }}' \
                                        f'          OPTIONAL {{ '\
                                        f'                     ?pom {R2RML_OBJECT} ?object_bn . ' \
                                        f'                     ?object_bn ?parent_object_term ?parent_object_value. ' \
                                        f'                      OPTIONAL {{' \
                                        f'                          ?object_bn {R2RML_PARENT_TRIPLESMAP} ?parent_tm .' \
                                        f'                          OPTIONAL {{ ' \
                                        f'                              ?object_bn {R2RML_JOIN_CONDITION} ?join_condition . ' \
                                        f'                              ?join_condition ?parent_condition_term ?parent_condition_value .' \
                                        f'                          }}' \
                                        f'                      }}' \
                                        f'          }} ' \
                                        f'      }} ' \
                                        f'      OPTIONAL {{ ' \
                                        f'          ?parent_triples_map {R2RML_PREDICATE_OBJECT_MAP} ?parent_pom.' \
                                        f'          OPTIONAL {{?parent_pom {R2RML_SHORTCUT_PREDICATE} ?parent_predicate }}' \
                                        f'          OPTIONAL {{ '\
                                        f'                    ?parent_pom {R2RML_PREDICATE} ?parent_predicate_bn . ' \
                                        f'                    ?parent_predicate_bn ?parent_predicate_term ?parent_predicate_value . }}' \
                                        f'          OPTIONAL {{?parent_pom {R2RML_SHORTCUT_OBJECT} ?parent_object }}' \
                                        f'          OPTIONAL {{ '\
                                        f'                     ?parent_pom {R2RML_OBJECT} ?parent_object_bn . ' \
                                        f'                     ?parent_object_bn ?parent_object_term ?parent_object_value. ' \
                                        f'                      OPTIONAL {{' \
                                        f'                          ?parent_object_bn {R2RML_PARENT_TRIPLESMAP} ?parent_tm .' \
                                        f'                          OPTIONAL {{ ' \
                                        f'                              ?object_bn_bn {R2RML_JOIN_CONDITION} ?parent_join_condition . ' \
                                        f'                              ?parent_join_condition ?parent_condition_term ?parent_condition_value .' \
                                        f'                          }}' \
                                        f'                      }}' \
                                        f'          }} ' \
                                        f'      }} ' \
                                        f'  }}'
        print(remove_super_class_pom_query)
        output_mappings.update(remove_super_class_pom_query)
    """

def add_object_property_rml(change,change_data, output_mappings):
    """
       Adds an object property to the TriplesMap indicated in the domain. For a change in the predicate object map the domain, property and range additions are needed.  
       Args:
           change: the URI of the change which needs to be of the type addObjectProperty
       Returns:
           the output_mappings updated with the added predicate object maps. 
    """
    query = f' SELECT DISTINCT ?domain ?property ?range WHERE {{ ' \
            f' <{change}> {OCH_ADDED_OBJECT_PROPERTY} ?property .' \
            f' ?domainchange {OCH_ADDED_DOMAIN_TO_PROPERTY} ?property.' \
            f' ?domainchange {OCH_ADDED_DOMAIN} ?domain.' \
            f' ?rangechange {OCH_ADDED_RANGE_TO_PROPERTY} ?property.' \
            f' ?rangechange {OCH_ADDED_OBJECT_RANGE} ?range. }}'

    for result in change_data.query(query):
        property_domain = result["domain"]
        property_predicate = result["property"]
        property_range = result["range"]

        insert_object_property_query = f' PREFIX {R2RML_PREFIX}: <{R2RML_URI}>' \
                                       f' PREFIX {RML_PREFIX}: <{RML_URI}>' \
                                       f' INSERT {{  ' \
                                       f'     ?triplesMap {R2RML_PREDICATE_OBJECT_MAP} [ ' \
                                       f'         {R2RML_SHORTCUT_PREDICATE} <{property_predicate}> ; ' \
                                       f'         {R2RML_OBJECT} [ ' \
                                       f'             {R2RML_PARENT_TRIPLESMAP} ?parent_triplesMap;' \
                                       f'             {R2RML_JOIN_CONDITION} [ ' \
                                       f'               {R2RML_CHILD} "XXX"; {R2RML_PARENT} "XXX" ' \
                                       f'          ] ] ]. }}' \
                                       f'  WHERE {{' \
                                       f'     ?triplesMap {R2RML_SUBJECT} ?subjectMap . ' \
                                       f'     ?subjectMap {R2RML_CLASS} <{property_domain}> .' \
                                       f'     ?parent_triplesMap {R2RML_SUBJECT} ?parent_subjectMap . ' \
                                       f'     ?parent_subjectMap {R2RML_CLASS} <{property_range}> }}'
        output_mappings.update(insert_object_property_query)


# --------------------------------------------------------------------------------------------------------------------------------------------------
def remove_object_property_rml(change, change_data, output_mappings):
    """
        Removes the object property indicated in the change as property from its domain. For a change in the predicate object map the domain, property and range additions are needed.
        Args:
           change: the URI of the change which needs to be of the type addObjectProperty
        Returns:
           the output_mappings updated with the reference predicate object mapping removed
    """
    query = f' SELECT DISTINCT ?domain ?property ?range WHERE {{ ' \
            f' <{change}> {OCH_REMOVED_OBJECT_PROPERTY} ?property .' \
            f' ?domainchange {OCH_REMOVED_DOMAIN_TO_PROPERTY} ?property.' \
            f' ?domainchange {OCH_REMOVED_DOMAIN} ?domain.' \
            f' ?rangechange {OCH_REMOVED_RANGE_TO_PROPERTY} ?property.' \
            f' ?rangechange {OCH_REMOVED_OBJECT_RANGE} ?range. }}'

    #print(query)        
    for result in change_data.query(query):
        property_domain = result["domain"]
        property_predicate = result["property"]
        property_range = result["range"]
        remove_object_property_query = f' PREFIX {R2RML_PREFIX}: <{R2RML_URI}>' \
                                       f' PREFIX {RML_PREFIX}: <{RML_URI}>' \
                                       f' DELETE {{' \
                                       f'     ?triplesMap {R2RML_PREDICATE_OBJECT_MAP} ?pom.' \
                                       f'     ?pom {R2RML_SHORTCUT_PREDICATE} <{property_predicate}> .' \
                                       f'     ?pom {R2RML_OBJECT} ?objectMap.' \
                                       f'     ?objectMap {R2RML_PARENT_TRIPLESMAP} ?parentTriplesMap . ' \
                                       f'     ?objectMap {R2RML_JOIN_CONDITION} ?joinConditions . ' \
                                       f'     ?joinConditions ?conditions ?condition_values }}  ' \
                                       f' WHERE {{' \
                                       f'     ?triplesMap {R2RML_SUBJECT} ?subjectMap.' \
                                       f'     ?subjectMap {R2RML_CLASS} <{property_domain}> . ' \
                                       f'     ?triplesMap {R2RML_PREDICATE_OBJECT_MAP} ?pom .' \
                                       f'     ?pom {R2RML_SHORTCUT_PREDICATE} <{property_predicate}> .' \
                                       f'     ?pom {R2RML_OBJECT} ?objectMap .' \
                                       f'     ?objectMap {R2RML_PARENT_TRIPLESMAP} ?parentTriplesMap .' \
                                       f'     ?parent_triplesMap {R2RML_SUBJECT} ?parent_subjectMap . ' \
                                       f'     ?parent_subjectMap {R2RML_CLASS} <{property_range}> ' \
                                       f'     OPTIONAL {{ ?objectMap {R2RML_JOIN_CONDITION} ?joinConditions .' \
                                       f'                 ?joinConditions ?conditions ?condition_values }} . }}'
        #print(remove_object_property_query)
        output_mappings.update(remove_object_property_query)


# -------------------------------------------------------------------------------------------------------------------------
def add_data_property_rml(change,change_data, output_mappings):
    """
       Adds a data property to the TriplesMap indicated in the domain. For a change in the predicate object map the domain, property and range additions are needed.
       Args:
           change: the URI of the change which needs to be of the type addObjectProperty
       Returns:
           the output_mappings updated with the new predicate object map with empty reference
    """
    query = f' SELECT DISTINCT ?domain ?property ?range WHERE {{ ' \
            f' <{change}> {OCH_ADDED_DATA_PROPERTY} ?property .' \
            f' ?domainchange {OCH_ADDED_DOMAIN_TO_PROPERTY} ?property.' \
            f' ?domainchange {OCH_ADDED_DOMAIN} ?domain.' \
            f' ?rangechange {OCH_ADDED_RANGE_TO_PROPERTY} ?property.' \
            f' ?rangechange {OCH_ADDED_DATA_RANGE} ?range. }}'
    #print(query)
    for result in change_data.query(query):
        property_domain = result["domain"]
        property_predicate = result["property"]
        property_range = result["range"]
        insert_data_property_query = f' PREFIX {R2RML_PREFIX}: <{R2RML_URI}>' \
                                     f' PREFIX {RML_PREFIX}: <{RML_URI}>' \
                                     f' INSERT {{  ' \
                                     f'     ?triplesMap {R2RML_PREDICATE_OBJECT_MAP} [ ' \
                                     f'         {R2RML_SHORTCUT_PREDICATE} <{property_predicate}> ; ' \
                                     f'         {R2RML_OBJECT} [ ' \
                                     f'             {RML_REFERENCE} "XXX";' \
                                     f'             {R2RML_DATATYPE} <{property_range}>' \
                                     f'          ] ]. }}' \
                                     f'  WHERE {{' \
                                     f'     ?triplesMap {R2RML_SUBJECT} ?subjectMap . ' \
                                     f'     ?subjectMap {R2RML_CLASS} <{property_domain}> . }} '
        #print(insert_data_property_query)
        output_mappings.update(insert_data_property_query)


# -----------------------------------------------------------------------------------------------------------------------------------
def remove_data_property_rml(change,change_data, output_mappings):
    """
        Removes the data property indicated in the change as property from its domain. For a change in the predicate object map the domain, property and range additions are needed.
        Args:
           change: the URI of the change which needs to be of the type addObjectProperty
        Returns:
           the output_mappings updated with the predicate object mapping removed
    """
    query = f' SELECT DISTINCT ?domain ?property ?range WHERE {{ ' \
            f' <{change}> {OCH_REMOVED_DATA_PROPERTY} ?property .' \
            f' ?domainchange {OCH_REMOVED_DOMAIN_TO_PROPERTY} ?property.' \
            f' ?domainchange {OCH_REMOVED_DOMAIN} ?domain.' \
            f' ?rangechange {OCH_REMOVED_RANGE_TO_PROPERTY} ?property.' \
            f' ?rangechange {OCH_REMOVED_DATA_RANGE} ?range. }}'
    #print(query)
    for result in change_data.query(query):
        property_domain = result["domain"]
        property_predicate = result["property"]
        property_range = result["range"]

        remove_data_property_query = f' PREFIX {R2RML_PREFIX}: <{R2RML_URI}>' \
                                     f' PREFIX {RML_PREFIX}: <{RML_URI}>' \
                                     f' DELETE {{' \
                                     f'     ?triplesMap {R2RML_PREDICATE_OBJECT_MAP} ?pom.' \
                                     f'     ?pom {R2RML_SHORTCUT_PREDICATE} <{property_predicate}> .' \
                                     f'     ?pom {R2RML_SHORTCUT_OBJECT} ?object.' \
                                     f'     ?pom {R2RML_OBJECT} ?objectMap.' \
                                     f'     ?objectMap ?object_term ?objectValue .}}' \
                                     f' WHERE {{' \
                                     f'     ?triplesMap {R2RML_SUBJECT} ?subjectMap.' \
                                     f'     ?subjectMap {R2RML_CLASS} <{property_domain}> . ' \
                                     f'     ?triplesMap {R2RML_PREDICATE_OBJECT_MAP} ?pom .' \
                                     f'     ?pom {R2RML_SHORTCUT_PREDICATE} <{property_predicate}> .' \
                                     f'     OPTIONAL {{?pom {R2RML_SHORTCUT_OBJECT} ?object .}}' \
                                     f'     OPTIONAL {{ '\
                                     f'         ?pom {R2RML_OBJECT} ?objectMap .' \
                                     f'         ?objectMap ?object_term ?objectValue.' \
                                     f'     OPTIONAL {{ ?objectMap {R2RML_DATATYPE} <{property_range}>}}  }} . }}'
        #print(remove_data_property_query)
        output_mappings.update(remove_data_property_query)



# -------------------------------------------------------------------------------------------------------------

def deprecate_entity_rml(change,change_data, output_mappings, deprecated_mappings,ontology):
    """
       Deprecates an entity in the knowledge graph by removing its triples map and its subject.
       Args:
           change: the URI of the change which needs to be of the type deprecate_entity 
    """
    query = f' SELECT DISTINCT ?entity WHERE {{ ' \
            f' <{change}> {OCH_DEPRECATED_ENTITY} ?entity. }}'
    #print(query)
    for result in change_data.query(query):
        entity = result["entity"]
        query = f' SELECT DISTINCT ?type WHERE {{ ' \
                f' <{entity}> {RDF_TYPE} ?type. }}'
        #print(query)
        for result in ontology.query(query):
            entity_type = result["type"]
            #print(f'Entity type: {entity_type}')
            if entity_type == URIRef(OWL_CLASS_URI):
                # Remove the triples map for the class entity
                query = f' PREFIX {R2RML_PREFIX}: <{R2RML_URI}>' \
                        f' PREFIX {RML_PREFIX}: <{RML_URI}>' \
                        f' CONSTRUCT {{' \
                        f'      ?triples_map {RDF_TYPE} {R2RML_TRIPLES_MAP}.' \
                        f'      ?triples_map {R2RML_SUBJECT} ?subject.' \
                        f'      ?subject ?subject_term ?subject_value .' \
                        f'      ?subject {R2RML_CLASS} <{entity}> .' \
                        f'      ?triples_map {RML_LOGICAL_SOURCE} ?logical_source .' \
                        f'      ?logical_source ?logical_source_term ?logical_source_value .' \
                        f'      ?triples_map {R2RML_PREDICATE_OBJECT_MAP} ?pom. ' \
                        f'      ?pom  {R2RML_SHORTCUT_PREDICATE} ?predicate . ' \
                        f'      ?pom {R2RML_PREDICATE} ?predicate_bn . ' \
                        f'      ?predicate_bn ?predicate_term ?predicate_value . ' \
                        f'      ?pom {R2RML_SHORTCUT_OBJECT} ?object. ' \
                        f'      ?pom {R2RML_OBJECT} ?object_bn . ' \
                        f'      ?object_bn ?object_term ?object_value.' \
                        f'      ?object_bn {R2RML_PARENT_TRIPLESMAP} ?parent_tm . ' \
                        f'      ?object_bn {R2RML_JOIN_CONDITION} ?join_condition . ' \
                        f'      ?join_condition ?condition_term ?condition_value . ' \
                        f'      ?parent_triples_map {R2RML_PREDICATE_OBJECT_MAP} ?parent_pom . ' \
                        f'      ?parent_pom {R2RML_SHORTCUT_PREDICATE} ?parent_predicate .' \
                        f'      ?parent_pom {R2RML_PREDICATE} ?parent_predicate_bn .' \
                        f'      ?parent_predicate_bn ?parent_predicate_term ?parent_predicate_value .' \
                        f'      ?parent_pom {R2RML_OBJECT} ?parent_object . ' \
                        f'      ?parent_object {R2RML_PARENT_TRIPLESMAP} ?parent_triples_map . ' \
                        f'      ?parent_object {R2RML_JOIN_CONDITION} ?parent_join_conditions . ' \
                        f'      ?parent_join_conditions ?parent_condition_term ?parent_conditions_value .}} ' \
                        f' WHERE {{ ' \
                        f'      ?triples_map {RDF_TYPE} {R2RML_TRIPLES_MAP}.' \
                        f'      ?triples_map {R2RML_SUBJECT} ?subject.' \
                        f'      ?subject ?subject_term ?subject_value .' \
                        f'      ?subject {R2RML_CLASS} <{entity}> .' \
                        f'      ?triples_map {RML_LOGICAL_SOURCE} ?logical_source .' \
                        f'      ?logical_source ?logical_source_term ?logical_source_value .' \
                        f'      OPTIONAL {{ ' \
                        f'          ?triples_map {R2RML_PREDICATE_OBJECT_MAP} ?pom.' \
                        f'          OPTIONAL {{?pom {R2RML_SHORTCUT_PREDICATE} ?predicate . }}' \
                        f'          OPTIONAL {{   ?pom {R2RML_PREDICATE} ?predicate_bn.'\
                        f'                        ?predicate_bn ?predicate_term ?predicate_value . }}' \
                        f'          OPTIONAL {{?pom {R2RML_SHORTCUT_OBJECT} ?object .}}' \
                        f'          OPTIONAL {{?pom {R2RML_OBJECT} ?object_bn .' \
                        f'                      ?object_bn ?object_term ?object_value. }}' \
                        f'          OPTIONAL {{' \
                        f'              ?object_bn {R2RML_PARENT_TRIPLESMAP} ?parent_tm .' \
                        f'              OPTIONAL {{ ' \
                        f'                  ?object_bn {R2RML_JOIN_CONDITION} ?join_condition . ' \
                        f'                  ?join_condition ?condition_term ?condition_value .' \
                        f'              }}' \
                        f'          }}' \
                        f'    }}' \
                        f'      OPTIONAL {{ ' \
                        f'          ?parent_triples_map {R2RML_PREDICATE_OBJECT_MAP} ?parent_pom.' \
                        f'          OPTIONAL {{?parent_pom {R2RML_SHORTCUT_PREDICATE} ?parent_predicate .}}' \
                        f'          OPTIONAL {{     ?parent_pom {R2RML_PREDICATE} ?parent_predicate_bn.'\
                        f'                          ?parent_predicate_bn ?parent_predicate_term ?parent_predicate_value . }}' \
                        f'          ?parent_pom {R2RML_OBJECT} ?parent_object .' \
                        f'          ?parent_object {R2RML_PARENT_TRIPLESMAP} ?parent_triples_map .' \
                        f'          OPTIONAL {{ ' \
                        f'              ?parent_object {R2RML_JOIN_CONDITION} ?parent_join_conditions . ' \
                        f'              ?parent_join_conditions ?parent_condition_term ?parent_conditions_value .' \
                        f'          }}' \
                        f'      }} ' \
                        f'  }}'
                #print(query)
                deprecated_triples=output_mappings.query(query)
                for row in deprecated_triples:
                    deprecated_mappings.add(row)
                query = f' PREFIX {R2RML_PREFIX}: <{R2RML_URI}>' \
                        f' PREFIX {RML_PREFIX}: <{RML_URI}>' \
                        f' DELETE {{' \
                        f'      ?triples_map {RDF_TYPE} {R2RML_TRIPLES_MAP}.' \
                        f'      ?triples_map {R2RML_SUBJECT} ?subject.' \
                        f'      ?subject ?subject_term ?subject_value .' \
                        f'      ?subject {R2RML_CLASS} <{entity}> .' \
                        f'      ?triples_map {RML_LOGICAL_SOURCE} ?logical_source .' \
                        f'      ?logical_source ?logical_source_term ?logical_source_value .' \
                        f'      ?triples_map {R2RML_PREDICATE_OBJECT_MAP} ?pom. ' \
                        f'      ?pom  {R2RML_SHORTCUT_PREDICATE} ?predicate . ' \
                        f'      ?pom {R2RML_PREDICATE} ?predicate_bn . ' \
                        f'      ?predicate_bn ?predicate_term ?predicate_value . ' \
                        f'      ?pom {R2RML_SHORTCUT_OBJECT} ?object. ' \
                        f'      ?pom {R2RML_OBJECT} ?object_bn . ' \
                        f'      ?object_bn ?object_term ?object_value.' \
                        f'      ?object_bn {R2RML_PARENT_TRIPLESMAP} ?parent_tm . ' \
                        f'      ?object_bn {R2RML_JOIN_CONDITION} ?join_condition . ' \
                        f'      ?join_condition ?condition_term ?condition_value . ' \
                        f'      ?parent_triples_map {R2RML_PREDICATE_OBJECT_MAP} ?parent_pom . ' \
                        f'      ?parent_pom {R2RML_SHORTCUT_PREDICATE} ?parent_predicate .' \
                        f'      ?parent_pom {R2RML_PREDICATE} ?parent_predicate_bn .' \
                        f'      ?parent_predicate_bn ?parent_predicate_term ?parent_predicate_value .' \
                        f'      ?parent_pom {R2RML_OBJECT} ?parent_object . ' \
                        f'      ?parent_object {R2RML_PARENT_TRIPLESMAP} ?triples_map . ' \
                        f'      ?parent_object {R2RML_JOIN_CONDITION} ?parent_join_conditions . ' \
                        f'      ?parent_join_conditions ?parent_condition_term ?parent_conditions_value .}} ' \
                        f' WHERE {{ ' \
                        f'      ?triples_map {RDF_TYPE} {R2RML_TRIPLES_MAP}.' \
                        f'      ?triples_map {R2RML_SUBJECT} ?subject.' \
                        f'      ?subject ?subject_term ?subject_value .' \
                        f'      ?subject {R2RML_CLASS} <{entity}> .' \
                        f'      ?triples_map {RML_LOGICAL_SOURCE} ?logical_source .' \
                        f'      ?logical_source ?logical_source_term ?logical_source_value .' \
                        f'      OPTIONAL {{ ' \
                        f'          ?triples_map {R2RML_PREDICATE_OBJECT_MAP} ?pom.' \
                        f'          OPTIONAL {{?pom {R2RML_SHORTCUT_PREDICATE} ?predicate . }}' \
                        f'          OPTIONAL {{   ?pom {R2RML_PREDICATE} ?predicate_bn.'\
                        f'                        ?predicate_bn ?predicate_term ?predicate_value . }}' \
                        f'          OPTIONAL {{?pom {R2RML_SHORTCUT_OBJECT} ?object .}}' \
                        f'          OPTIONAL {{?pom {R2RML_OBJECT} ?object_bn .' \
                        f'                      ?object_bn ?object_term ?object_value. }}' \
                        f'          OPTIONAL {{' \
                        f'              ?object_bn {R2RML_PARENT_TRIPLESMAP} ?parent_tm .' \
                        f'              OPTIONAL {{ ' \
                        f'                  ?object_bn {R2RML_JOIN_CONDITION} ?join_condition . ' \
                        f'                  ?join_condition ?condition_term ?condition_value .' \
                        f'              }}' \
                        f'          }}' \
                        f'    }}' \
                        f'      OPTIONAL {{ ' \
                        f'          ?parent_triples_map {R2RML_PREDICATE_OBJECT_MAP} ?parent_pom.' \
                        f'          OPTIONAL {{?parent_pom {R2RML_SHORTCUT_PREDICATE} ?parent_predicate .}}' \
                        f'          OPTIONAL {{     ?parent_pom {R2RML_PREDICATE} ?parent_predicate_bn.'\
                        f'                          ?parent_predicate_bn ?parent_predicate_term ?parent_predicate_value . }}' \
                        f'          ?parent_pom {R2RML_OBJECT} ?parent_object .' \
                        f'          ?parent_object {R2RML_PARENT_TRIPLESMAP} ?triples_map .' \
                        f'          OPTIONAL {{ ' \
                        f'              ?parent_object {R2RML_JOIN_CONDITION} ?parent_join_conditions . ' \
                        f'              ?parent_join_conditions ?parent_condition_term ?parent_conditions_value .' \
                        f'          }}' \
                        f'      }} ' \
                        f'  }}'
                #print(query)
                output_mappings.update(query)

            elif entity_type == URIRef(OWL_OBJECT_PROPERTY_URI):
                # Remove all predicate-object maps using this object property
                query = f' PREFIX {R2RML_PREFIX}: <{R2RML_URI}>' \
                        f' PREFIX {RML_PREFIX}: <{RML_URI}>' \
                        f' CONSTRUCT {{' \
                        f'     ?triplesMap {R2RML_PREDICATE_OBJECT_MAP} ?pom.' \
                        f'     ?pom {R2RML_SHORTCUT_PREDICATE} <{entity}> .' \
                        f'     ?pom {R2RML_OBJECT} ?objectMap.' \
                        f'     ?objectMap {R2RML_PARENT_TRIPLESMAP} ?parentTriplesMap . ' \
                        f'     ?objectMap {R2RML_JOIN_CONDITION} ?joinConditions . ' \
                        f'     ?joinConditions ?conditions ?condition_values }}  ' \
                        f' WHERE {{' \
                        f'     ?triplesMap {R2RML_SUBJECT} ?subjectMap.' \
                        f'     ?subjectMap {R2RML_CLASS} ?domain . ' \
                        f'     ?triplesMap {R2RML_PREDICATE_OBJECT_MAP} ?pom .' \
                        f'     ?pom {R2RML_SHORTCUT_PREDICATE} <{entity}> .' \
                        f'     ?pom {R2RML_OBJECT} ?objectMap .' \
                        f'     ?objectMap {R2RML_PARENT_TRIPLESMAP} ?parentTriplesMap .' \
                        f'     ?parent_triplesMap {R2RML_SUBJECT} ?parent_subjectMap . ' \
                        f'     ?parent_subjectMap {R2RML_CLASS} ?range. ' \
                        f'     OPTIONAL {{ ?objectMap {R2RML_JOIN_CONDITION} ?joinConditions .' \
                        f'                 ?joinConditions ?conditions ?condition_values }} . }}'
                #print(query)
                deprecated_triples=output_mappings.query(query)
                for row in deprecated_triples:
                    deprecated_mappings.add(row)
                query=  f' PREFIX {R2RML_PREFIX}: <{R2RML_URI}>' \
                        f' PREFIX {RML_PREFIX}: <{RML_URI}>' \
                        f' DELETE {{' \
                        f'     ?triplesMap {R2RML_PREDICATE_OBJECT_MAP} ?pom.' \
                        f'     ?pom {R2RML_SHORTCUT_PREDICATE} <{entity}> .' \
                        f'     ?pom {R2RML_OBJECT} ?objectMap.' \
                        f'     ?objectMap {R2RML_PARENT_TRIPLESMAP} ?parentTriplesMap . ' \
                        f'     ?objectMap {R2RML_JOIN_CONDITION} ?joinConditions . ' \
                        f'     ?joinConditions ?conditions ?condition_values }}  ' \
                        f' WHERE {{' \
                        f'     ?triplesMap {R2RML_SUBJECT} ?subjectMap.' \
                        f'     ?subjectMap {R2RML_CLASS} ?domain . ' \
                        f'     ?triplesMap {R2RML_PREDICATE_OBJECT_MAP} ?pom .' \
                        f'     ?pom {R2RML_SHORTCUT_PREDICATE} <{entity}> .' \
                        f'     ?pom {R2RML_OBJECT} ?objectMap .' \
                        f'     ?objectMap {R2RML_PARENT_TRIPLESMAP} ?parentTriplesMap .' \
                        f'     ?parent_triplesMap {R2RML_SUBJECT} ?parent_subjectMap . ' \
                        f'     ?parent_subjectMap {R2RML_CLASS} ?range. ' \
                        f'     OPTIONAL {{ ?objectMap {R2RML_JOIN_CONDITION} ?joinConditions .' \
                        f'                 ?joinConditions ?conditions ?condition_values }} . }}'
                #print(query)
                output_mappings.update(query)
        
            elif entity_type == URIRef(OWL_DATA_PROPERTY_URI):
                # Remove all predicate-object maps using this data property
                query = f' PREFIX {R2RML_PREFIX}: <{R2RML_URI}>' \
                        f' PREFIX {RML_PREFIX}: <{RML_URI}>' \
                        f' CONSTRUCT {{' \
                        f'     ?triplesMap {R2RML_PREDICATE_OBJECT_MAP} ?pom.' \
                        f'     ?pom {R2RML_SHORTCUT_PREDICATE} <{entity}> .' \
                        f'     ?pom {R2RML_SHORTCUT_OBJECT} ?object.' \
                        f'     ?pom {R2RML_OBJECT} ?objectMap.' \
                        f'     ?objectMap ?object_term ?objectValue .}}' \
                        f' WHERE {{' \
                        f'     ?triplesMap {R2RML_SUBJECT} ?subjectMap.' \
                        f'     ?subjectMap {R2RML_CLASS} ?domain . ' \
                        f'     ?triplesMap {R2RML_PREDICATE_OBJECT_MAP} ?pom .' \
                        f'     ?pom {R2RML_SHORTCUT_PREDICATE} <{entity}> .' \
                        f'     OPTIONAL {{?pom {R2RML_SHORTCUT_OBJECT} ?object .}}' \
                        f'     OPTIONAL {{ '\
                        f'         ?pom {R2RML_OBJECT} ?objectMap .' \
                        f'         ?objectMap ?object_term ?objectValue.' \
                        f'     OPTIONAL {{ ?objectMap {R2RML_DATATYPE} ?range}}  }} . }}'
                deprecated_triples=output_mappings.query(query)
                for row in deprecated_triples:
                    deprecated_mappings.add(row)
                query = f' PREFIX {R2RML_PREFIX}: <{R2RML_URI}>' \
                        f' PREFIX {RML_PREFIX}: <{RML_URI}>' \
                        f' DELETE {{' \
                        f'     ?triplesMap {R2RML_PREDICATE_OBJECT_MAP} ?pom.' \
                        f'     ?pom {R2RML_SHORTCUT_PREDICATE} <{entity}> .' \
                        f'     ?pom {R2RML_SHORTCUT_OBJECT} ?object.' \
                        f'     ?pom {R2RML_OBJECT} ?objectMap.' \
                        f'     ?objectMap ?object_term ?objectValue .}}' \
                        f' WHERE {{' \
                        f'     ?triplesMap {R2RML_SUBJECT} ?subjectMap.' \
                        f'     ?subjectMap {R2RML_CLASS} ?domain . ' \
                        f'     ?triplesMap {R2RML_PREDICATE_OBJECT_MAP} ?pom .' \
                        f'     ?pom {R2RML_SHORTCUT_PREDICATE} <{entity}> .' \
                        f'     OPTIONAL {{?pom {R2RML_SHORTCUT_OBJECT} ?object .}}' \
                        f'     OPTIONAL {{ '\
                        f'         ?pom {R2RML_OBJECT} ?objectMap .' \
                        f'         ?objectMap ?object_term ?objectValue.' \
                        f'     OPTIONAL {{ ?objectMap {R2RML_DATATYPE} ?range}}  }} . }}'
                output_mappings.update(query)

def revoke_deprecate_entity_rml(change, change_data, output_mappings, deprecated_mappings, ontology):
    """
       Reverts the deprecation of an entity in the knowledge graph by restoring its triples map and its subject from deprecated_mappings.
       Args:
           change: the URI of the change which needs to be of the type revoke_deprecate_entity 
    """
    query = f' SELECT DISTINCT ?entity WHERE {{ ' \
            f' <{change}> {OCH_UNDEPRECATED_ELEMENT} ?entity. }}'
    #print(query)
    for result in change_data.query(query):
        entity = result["entity"]
        query = f' SELECT DISTINCT ?type WHERE {{ ' \
                f' <{entity}> {RDF_TYPE} ?type. }}'
        #print(query)
        for result in ontology.query(query):
            entity_type = result["type"]
            #print(f'Entity type: {entity_type}')
            if entity_type == URIRef(OWL_CLASS_URI):
            # Restore the triples map for the class entity from deprecated_mappings to output_mappings
                query = f' PREFIX {R2RML_PREFIX}: <{R2RML_URI}>' \
                        f' PREFIX {RML_PREFIX}: <{RML_URI}>' \
                        f' CONSTRUCT {{' \
                        f'      ?triples_map {RDF_TYPE} {R2RML_TRIPLES_MAP}.' \
                        f'      ?triples_map {R2RML_SUBJECT} ?subject.' \
                        f'      ?subject ?subject_term ?subject_value .' \
                        f'      ?subject {R2RML_CLASS} <{entity}> .' \
                        f'      ?triples_map {RML_LOGICAL_SOURCE} ?logical_source .' \
                        f'      ?logical_source ?logical_source_term ?logical_source_value .' \
                        f'      ?triples_map {R2RML_PREDICATE_OBJECT_MAP} ?pom. ' \
                        f'      ?pom  {R2RML_SHORTCUT_PREDICATE} ?predicate . ' \
                        f'      ?pom {R2RML_PREDICATE} ?predicate_bn . ' \
                        f'      ?predicate_bn ?predicate_term ?predicate_value . ' \
                        f'      ?pom {R2RML_SHORTCUT_OBJECT} ?object. ' \
                        f'      ?pom {R2RML_OBJECT} ?object_bn . ' \
                        f'      ?object_bn ?object_term ?object_value.' \
                        f'      ?object_bn {R2RML_PARENT_TRIPLESMAP} ?parent_tm . ' \
                        f'      ?object_bn {R2RML_JOIN_CONDITION} ?join_condition . ' \
                        f'      ?join_condition ?condition_term ?condition_value . ' \
                        f'      ?parent_triples_map {R2RML_PREDICATE_OBJECT_MAP} ?parent_pom . ' \
                        f'      ?parent_pom {R2RML_SHORTCUT_PREDICATE} ?parent_predicate .' \
                        f'      ?parent_pom {R2RML_PREDICATE} ?parent_predicate_bn .' \
                        f'      ?parent_predicate_bn ?parent_predicate_term ?parent_predicate_value .' \
                        f'      ?parent_pom {R2RML_OBJECT} ?parent_object . ' \
                        f'      ?parent_object {R2RML_PARENT_TRIPLESMAP} ?triples_map . ' \
                        f'      ?parent_object {R2RML_JOIN_CONDITION} ?parent_join_conditions . ' \
                        f'      ?parent_join_conditions ?parent_condition_term ?parent_conditions_value .}} ' \
                        f' WHERE {{ ' \
                        f'      ?triples_map {RDF_TYPE} {R2RML_TRIPLES_MAP}.' \
                        f'      ?triples_map {R2RML_SUBJECT} ?subject.' \
                        f'      ?subject ?subject_term ?subject_value .' \
                        f'      ?subject {R2RML_CLASS} <{entity}> .' \
                        f'      ?triples_map {RML_LOGICAL_SOURCE} ?logical_source .' \
                        f'      ?logical_source ?logical_source_term ?logical_source_value .' \
                        f'      OPTIONAL {{ ' \
                        f'          ?triples_map {R2RML_PREDICATE_OBJECT_MAP} ?pom.' \
                        f'          OPTIONAL {{?pom {R2RML_SHORTCUT_PREDICATE} ?predicate . }}' \
                        f'          OPTIONAL {{   ?pom {R2RML_PREDICATE} ?predicate_bn.'\
                        f'                        ?predicate_bn ?predicate_term ?predicate_value . }}' \
                        f'          OPTIONAL {{?pom {R2RML_SHORTCUT_OBJECT} ?object .}}' \
                        f'          OPTIONAL {{?pom {R2RML_OBJECT} ?object_bn .' \
                        f'                      ?object_bn ?object_term ?object_value. }}' \
                        f'          OPTIONAL {{' \
                        f'              ?object_bn {R2RML_PARENT_TRIPLESMAP} ?parent_tm .' \
                        f'              OPTIONAL {{ ' \
                        f'                  ?object_bn {R2RML_JOIN_CONDITION} ?join_condition . ' \
                        f'                  ?join_condition ?condition_term ?condition_value .' \
                        f'              }}' \
                        f'          }}' \
                        f'    }}' \
                        f'      OPTIONAL {{ ' \
                        f'          ?parent_triples_map {R2RML_PREDICATE_OBJECT_MAP} ?parent_pom.' \
                        f'          OPTIONAL {{?parent_pom {R2RML_SHORTCUT_PREDICATE} ?parent_predicate .}}' \
                        f'          OPTIONAL {{     ?parent_pom {R2RML_PREDICATE} ?parent_predicate_bn.'\
                        f'                          ?parent_predicate_bn ?parent_predicate_term ?parent_predicate_value . }}' \
                        f'          ?parent_pom {R2RML_OBJECT} ?parent_object .' \
                        f'          ?parent_object {R2RML_PARENT_TRIPLESMAP} ?triples_map .' \
                        f'          OPTIONAL {{ ' \
                        f'              ?parent_object {R2RML_JOIN_CONDITION} ?parent_join_conditions . ' \
                        f'              ?parent_join_conditions ?parent_condition_term ?parent_conditions_value .' \
                        f'          }}' \
                        f'      }} ' \
                        f'  }}'
                #print(query)
                restored_triples = deprecated_mappings.query(query)
                for row in restored_triples:
                    output_mappings.add(row)
                # Remove from deprecated_mappings
                deprecated_mappings.update(query.replace("CONSTRUCT", "DELETE", 1))
            elif entity_type == URIRef(OWL_OBJECT_PROPERTY_URI):
            # Restore all predicate-object maps using this object property
                query = f' PREFIX {R2RML_PREFIX}: <{R2RML_URI}>' \
                    f' PREFIX {RML_PREFIX}: <{RML_URI}>' \
                    f' CONSTRUCT {{' \
                    f'     ?triplesMap {R2RML_PREDICATE_OBJECT_MAP} ?pom.' \
                    f'     ?pom {R2RML_SHORTCUT_PREDICATE} <{entity}> .' \
                    f'     ?pom {R2RML_OBJECT} ?objectMap.' \
                    f'     ?objectMap {R2RML_PARENT_TRIPLESMAP} ?parentTriplesMap . ' \
                    f'     ?objectMap {R2RML_JOIN_CONDITION} ?joinConditions . ' \
                    f'     ?joinConditions ?conditions ?condition_values }}  ' \
                    f' WHERE {{' \
                    f'     ?triplesMap {R2RML_PREDICATE_OBJECT_MAP} ?pom .' \
                    f'     ?pom {R2RML_SHORTCUT_PREDICATE} <{entity}> .' \
                    f'     ?pom {R2RML_OBJECT} ?objectMap .' \
                    f'     ?objectMap {R2RML_PARENT_TRIPLESMAP} ?parentTriplesMap .' \
                    f'     OPTIONAL {{ ?objectMap {R2RML_JOIN_CONDITION} ?joinConditions .' \
                    f'                 ?joinConditions ?conditions ?condition_values }} . }}'
                #print(query)
                restored_triples = deprecated_mappings.query(query)
                for row in restored_triples:
                    output_mappings.add(row)
                deprecated_mappings.update(query.replace("CONSTRUCT", "DELETE", 1))
            elif entity_type == URIRef(OWL_DATA_PROPERTY_URI):
            # Restore all predicate-object maps using this data property
                query = f' PREFIX {R2RML_PREFIX}: <{R2RML_URI}>' \
                    f' PREFIX {RML_PREFIX}: <{RML_URI}>' \
                    f' CONSTRUCT {{' \
                    f'     ?triplesMap {R2RML_PREDICATE_OBJECT_MAP} ?pom.' \
                    f'     ?pom {R2RML_SHORTCUT_PREDICATE} <{entity}> .' \
                    f'     ?pom {R2RML_SHORTCUT_OBJECT} ?object.' \
                    f'     ?pom {R2RML_OBJECT} ?objectMap.' \
                    f'     ?objectMap ?object_term ?objectValue .}}' \
                    f' WHERE {{' \
                    f'     ?triplesMap {R2RML_PREDICATE_OBJECT_MAP} ?pom .' \
                    f'     ?pom {R2RML_SHORTCUT_PREDICATE} <{entity}> .' \
                    f'     OPTIONAL {{?pom {R2RML_SHORTCUT_OBJECT} ?object .}}' \
                    f'     OPTIONAL {{ '\
                    f'         ?pom {R2RML_OBJECT} ?objectMap .' \
                    f'         ?objectMap ?object_term ?objectValue.' \
                    f'     OPTIONAL {{ ?objectMap {R2RML_DATATYPE} ?range}}  }} . }}'
                #print(query)
                restored_triples = deprecated_mappings.query(query)
                for row in restored_triples:
                    output_mappings.add(row)
                deprecated_mappings.update(query.replace("CONSTRUCT", "DELETE", 1))

def rename_entity(change, change_data, output_mappings):
    """
    Renames a term (class, property, etc.) in the output_mappings.
    Args:
       change: the URI of the change which needs to be of the type RenameEntity
    """
    query = f'SELECT DISTINCT ?old_entity ?new_entity WHERE {{ ' \
            f'<{change}> {OCH_OLD_NAME} ?old_entity. ' \
            f'<{change}> {OCH_NEW_NAME} ?new_entity. }}'
    for result in change_data.query(query):
        old_entity = result["old_entity"]
        new_entity = result["new_entity"]
        # Update all triples where old_entity appears as subject, predicate, or object
        update_query =  f' DELETE {{ ?s ?p ?o. }} ' \
                        f' INSERT {{ ?s_new ?p_new ?o_new. }} ' \
                        f' WHERE {{ ' \
                        f'   ?s ?p ?o. ' \
                        f'   BIND(IF(?s = <{old_entity}>, <{new_entity}>, ?s) AS ?s_new) ' \
                        f'   BIND(IF(?p = <{old_entity}>, <{new_entity}>, ?p) AS ?p_new) ' \
                        f'   BIND(IF(?o = <{old_entity}>, <{new_entity}>, ?o) AS ?o_new) ' \
                        f'   FILTER(?s != ?s_new || ?p != ?p_new || ?o != ?o_new) ' \
                        f' }}'
        output_mappings.update(update_query)

#---------------------------------------SHACL CHANGES-------------------------------------------------------------


def deprecate_entity_shacl(change,change_data,output_shacl): 
    """
       Deprecates an entity in the SHACL shape by adding the "sh:deactivated true" to the corresponding shape.
       Args:
           change: the URI of the change which needs to be of the type deprecate_entity 
    """
    query = f' SELECT DISTINCT ?entity WHERE {{ ' \
            f' <{change}> {OCH_DEPRECATED_ENTITY} ?entity. }}'
    #print(query)
    for result in change_data.query(query):
        entity = result["entity"]
        query = (
            f' PREFIX {SHACL_PREFIX}: <{SHACL_URI}> '
            f' INSERT {{ '
            f'     ?shape {SHACL_DEACTIVATED} true . '
            f' }} '
            f' WHERE {{ '
            f'     {{ '
            f'         ?shape a {SHACL_NODE_SHAPE} ; '
            f'                {SHACL_TARGET_CLASS} <{entity}> . '
            f'     }} '
            f'     UNION '
            f'     {{ '
            f'         ?shape {SHACL_PATH} <{entity}> . '
            f'     }} '
            f'     FILTER NOT EXISTS {{ ?shape {SHACL_DEACTIVATED} true }} '
            f' }}'
        )
        #print(query)
        output_shacl.update(query)

#-----------------------------------------------------------------------------------------------------------------

def revoke_deprecate_entity_shacl(change,change_data,output_shacl): 
    """
       Revokes the deprecation of an entity in the SHACL shape by removing the "sh:deactivated true" from the corresponding shape.
       Args:
           change: the URI of the change which needs to be of the type revoke_deprecate_entity 
    """
    query = f' SELECT DISTINCT ?entity WHERE {{ ' \
            f' <{change}> {OCH_UNDEPRECATED_ELEMENT} ?entity. }}'
    #print(query)
    for result in change_data.query(query):
        entity = result["entity"]
        query = (
            f' PREFIX {SHACL_PREFIX}: <{SHACL_URI}> '
            f' DELETE {{ '
            f'     ?shape {SHACL_DEACTIVATED} true . '
            f' }} '
            f' WHERE {{ '
            f'     {{ '
            f'         ?shape a {SHACL_NODE_SHAPE} ; '
            f'                {SHACL_TARGET_CLASS} <{entity}> . '
            f'     }} '
            f'     UNION '
            f'     {{ '
            f'         ?shape {SHACL_PATH} <{entity}> . '
            f'     }} '
            f' }}'
        )
        #print(query)
        output_shacl.update(query)

#-----------------------------------------------------------------------------------------------------------------

def add_class_shacl(change, change_data, output_shapes):
    """
    Adds a class defined in the change KG into the shacl shape. This takes the form of adding NodeShape with the class as targetClass.
    Args:
        change: the URI of the change which needs to be of the type AddClass
    Returns:
        the output_shapes updated with a new class
    """
    select_change = f' SELECT DISTINCT ?class WHERE {{' \
                    f' <{change}> {OCH_ADDED_CLASS} ?class .}} '

    for result in change_data.query(select_change):
        added_class = result["class"]
        if "#" in added_class:
            class_local = added_class.split("#")[-1]
        elif "/" in added_class:
            class_local = added_class.split("/")[-1]
        else:
            class_local = added_class
        insert_class_query = (
            f' PREFIX {SHACL_PREFIX}: <{SHACL_URI}>'
            f' INSERT DATA {{ '
            f'   <{EXAMPLE_URI}{class_local}Shape> '
            f'     a {SHACL_NODE_SHAPE} ; '
            f'     {SHACL_TARGET_CLASS} <{added_class}> ; '
            f' }}'
        )
        #print(insert_class_query)
        output_shapes.update(insert_class_query)

def remove_class_shacl(change, change_data, output_mappings):
    """
    Removes a class defined in the change KG from the SHACL shape. This deletes the NodeShape with the class as targetClass and all related property shapes and nested shapes.
    Args:
        change: the URI of the change which needs to be of the type RemoveClass
    Returns:
        the output_shapes updated with the class and its related shapes removed
    """
    select_change = f' SELECT DISTINCT ?class WHERE {{' \
                    f' <{change}> {OCH_DELETED_CLASS} ?class .}} '
    
    for result in change_data.query(select_change):
        removed_class = result["class"]
        delete_class_query = (
            f' PREFIX {SHACL_PREFIX}: <{SHACL_URI}>\n'
            f' PREFIX {RDF_PREFIX}: <{RDF_URI}>\n'
            f' DELETE {{\n'
            f'   ?shape ?p ?o .\n'
            f'   ?propShape ?pp ?po .\n'
            f'   ?list ?lp ?lo .\n'
            f'   ?listItem ?listItemP ?listItemO .\n'
            f'   ?restNode ?restP ?restO .\n'
            f' }}\n'
            f' WHERE {{\n'
            f'   ?shape a {SHACL_NODE_SHAPE} ;\n'
            f'          {SHACL_TARGET_CLASS} <{removed_class}> ;\n'
            f'          ?p ?o .\n'
            f'   OPTIONAL {{\n'
            f'     ?shape {SHACL_PROPERTY_SHAPE} ?propShape .\n'
            f'     FILTER (isBlank(?propShape))\n'
            f'     ?propShape ?pp ?po .\n'
            f'     OPTIONAL {{\n'
            f'       ?propShape ?listPred ?list .\n'
            f'       FILTER(?listPred IN ({SHACL_IN}, {SHACL_OR}, {SHACL_AND}, {SHACL_XONE}))\n'
            f'       ?list {RDF_REST}*/{RDF_FIRST} ?listItem .\n'
            f'       ?list ?lp ?lo .\n'
            f'       OPTIONAL {{ ?listItem ?listItemP ?listItemO . }}\n'
            f'       ?list {RDF_REST}* ?restNode .\n'
            f'       ?restNode ?restP ?restO .\n'
            f'     }}\n'
            f'   }}\n'
            f' }}'
        )
        #print(delete_class_query)
        output_mappings.update(delete_class_query)


def add_super_class_shacl(change, change_data, output_shapes):
    """
    Adds a subclass to the SHACL NodeShape of the superclass by inserting the subclas as an additional sh:targetClass.
    Args:
        change: the URI of the change which needs to be of the type add_sub_class
    Returns:
        The output_shapes updated with the NodeShape of the superclass including the subclass as targetClass.
    """
    query = (
        f' SELECT DISTINCT ?super_class ?sub_class WHERE {{ '
        f'   <{change}> {OCH_ADD_SUBCLASS_SOURCE} ?sub_class. '
        f'   <{change}> {OCH_ADD_SUBCLASS_TARGET} ?super_class. }}'
    )
    for result in change_data.query(query):
        sub_class = result["sub_class"]
        super_class = result["super_class"]
        insert_super_class_query = (
            f' PREFIX {SHACL_PREFIX}: <{SHACL_URI}>'
            f' INSERT {{ '
            f'   ?shape {SHACL_TARGET_CLASS} <{sub_class}> . '
            f' }} '
            f' WHERE {{ '
            f'   ?shape a {SHACL_NODE_SHAPE} ; '
            f'          {SHACL_TARGET_CLASS} <{super_class}> . '
            f'   FILTER NOT EXISTS {{ ?shape {SHACL_TARGET_CLASS} <{sub_class}> }} '
            f' }}'
        )
        output_shapes.update(insert_super_class_query)

def remove_super_class_shacl(change, change_data, output_shapes):
    """
    Removes a subclass from the SHACL NodeShape of the superclass by deleting the subclass from sh:targetClass.
    Args:
        change: the URI of the change which needs to be of the type add_sub_class
    Returns:
        The output_shapes updated with the NodeShape of the superclass not including the subclass as targetClass.
    """
    query = (
        f' SELECT DISTINCT ?super_class ?sub_class WHERE {{ '
        f'   <{change}> {OCH_REMOVE_SUBCLASS_SOURCE} ?sub_class. '
        f'   <{change}> {OCH_REMOVE_SUBCLASS_TARGET} ?super_class. }}'
    )
    for result in change_data.query(query):
        sub_class = result["sub_class"]
        super_class = result["super_class"]
        remove_super_class_query = (
            f' PREFIX {SHACL_PREFIX}: <{SHACL_URI}>'
            f' DELETE {{ '
            f'   ?shape {SHACL_TARGET_CLASS} <{sub_class}> . '
            f' }} '
            f' WHERE {{ '
            f'   ?shape a {SHACL_NODE_SHAPE} ; '
            f'          {SHACL_TARGET_CLASS} <{super_class}>, <{sub_class}> . '
            f' }}'
        )
        output_shapes.update(remove_super_class_query)

def add_equivalent_class_shacl(change, change_data, output_shapes):
    """
    Adds an equivalent class to the SHACL NodeShape of the class by inserting the equivalent class as an additional sh:targetClass.
    Args:
        change: the URI of the change which needs to be of the type add_equivalent_class
    Returns:
        The output_shapes updated with the NodeShape of the class including the equivalent class as targetClass.
    """
    query = (
        f' SELECT DISTINCT ?source_class ?target_class WHERE {{ '
        f'   <{change}> {OCH_ADD_EQUIVALENT_CLASS_SOURCE} ?source_class. '
        f'   <{change}> {OCH_ADD_EQUIVALENT_CLASS_TARGET} ?target_class. }}'
    )
    for result in change_data.query(query):
        source_class = result["source_class"]
        target_class = result["target_class"]
        insert_equivalent_class_query = (
            f' PREFIX {SHACL_PREFIX}: <{SHACL_URI}>'
            f' PREFIX {PROV_PREFIX}: <{PROV_URI}>'
            f' INSERT {{ '
            f'   ?shape {SHACL_TARGET_CLASS} ?otherClass . '
            f'   ?shape {PROV_WAS_DERIVED_FROM} ?originalClass . '
            f' }} '
            f' WHERE {{ '
            f'   ?shape a {SHACL_NODE_SHAPE} ; '
            f'          {SHACL_TARGET_CLASS} ?originalClass . '
            f'     VALUES (?originalClass ?otherClass) {{ '
            f'         (<{source_class}> <{target_class}>) '
            f'         (<{target_class}> <{source_class}>) '
            f'     }} '
            f'   FILTER NOT EXISTS {{ ?shape {SHACL_TARGET_CLASS} ?otherClass }} '
            f' }}'
        )
        #print(insert_equivalent_class_query)
        output_shapes.update(insert_equivalent_class_query)

def remove_equivalent_class_shacl(change, change_data, output_shapes):
    """
    Removes an equivalent class from the SHACL NodeShape of the class by deleting the equivalent class from the sh:targetClass.
    Args:
        change: the URI of the change which needs to be of the type remove_equivalent_class
    Returns:
        The output_shapes updated with the NodeShape of the class excluding the equivalent class as targetClass.
    """
    query = (
        f' SELECT DISTINCT ?source_class ?target_class WHERE {{ '
        f'   <{change}> {OCH_REMOVE_EQUIVALENT_CLASS_SOURCE} ?source_class. '
        f'   <{change}> {OCH_REMOVE_EQUIVALENT_CLASS_TARGET} ?target_class. }}'
    )
    for result in change_data.query(query):
        source_class = result["source_class"]
        target_class = result["target_class"]
        delete_equivalent_class_query = (
            f' PREFIX {SHACL_PREFIX}: <{SHACL_URI}>\n'
            f' PREFIX {PROV_PREFIX}: <{PROV_URI}>\n'
            f' DELETE {{\n'
            f'   ?shape {SHACL_TARGET_CLASS} ?otherClass .\n'
            f'   ?shape {PROV_WAS_DERIVED_FROM} ?originalClass .\n'
            f' }}\n'
            f' WHERE {{\n'
            f'   ?shape a {SHACL_NODE_SHAPE} ;\n'
            f'          {SHACL_TARGET_CLASS} ?originalClass, ?otherClass ;\n'
            f'          {PROV_WAS_DERIVED_FROM} ?originalClass .\n'
            f'   VALUES (?originalClass ?otherClass) {{\n'
            f'     (<{source_class}> <{target_class}>)\n'
            f'     (<{target_class}> <{source_class}>)\n'
            f'   }}\n'
            f' }}'
        )
        #print(delete_equivalent_class_query)
        output_shapes.update(delete_equivalent_class_query)


def add_disjoint_class_shacl(change, change_data, output_shapes):
    """
    Adds a disjoint class restriction to the SHACL NodeShape via SHACL-SPARQL query.
    Args:
        change: the URI of the change which needs to be of the type add_disjoint_class
    Returns:
        The output_shapes updated with the constraints that enforce the disjointness of the classes.
    """
    query = (
        f' SELECT DISTINCT ?source_class ?target_class WHERE {{ '
        f'   <{change}> {OCH_ADD_DISJOINT_CLASS_SOURCE} ?source_class. '
        f'   <{change}> {OCH_ADD_DISJOINT_CLASS_TARGET} ?target_class. }}'
    )
    for result in change_data.query(query):
        source_class = result["source_class"]
        target_class = result["target_class"]
        add_disjoint_class_query = (
            f' PREFIX {SHACL_PREFIX}: <{SHACL_URI}>\n'
            f' INSERT {{\n'
            f'    ?sourceShape {SHACL_NOT} [ {SHACL_CLASS} <{target_class}> ] .\n'
            f'    ?targetShape {SHACL_NOT} [ {SHACL_CLASS} <{source_class}> ] .\n'
            f' }}\n'
            f' WHERE {{\n'
            f'   ?sourceShape a {SHACL_NODE_SHAPE} ;\n'
            f'     {SHACL_TARGET_CLASS} <{source_class}> .\n'
            f'   ?targetShape a {SHACL_NODE_SHAPE} ;\n'
            f'     {SHACL_TARGET_CLASS} <{target_class}> .\n'
            f'}}'
        )
        print(add_disjoint_class_query)
        output_shapes.update(add_disjoint_class_query)

def remove_disjoint_class_shacl(change, change_data, output_shapes):
    """
    Removes a disjoint class restriction from the SHACL NodeShape via SHACL-SPARQL query.
    Args:
        change: the URI of the change which needs to be of the type remove_disjoint_class
    Returns:
        The output_shapes updated without the constraints that enforce the disjointness of the classes.
    """
    query = (
        f' SELECT DISTINCT ?source_class ?target_class WHERE {{ '
        f'   <{change}> {OCH_REMOVE_DISJOINT_CLASS_SOURCE} ?source_class. '
        f'   <{change}> {OCH_REMOVE_DISJOINT_CLASS_TARGET} ?target_class. }}'
    )
    for result in change_data.query(query):
        source_class = result["source_class"]
        target_class = result["target_class"]
        remove_disjoint_class_query = (
            f' PREFIX {SHACL_PREFIX}: <{SHACL_URI}>\n'
            f' DELETE {{\n'
            f'    ?sourceShape {SHACL_NOT} ?propertyShapeSource.\n'
            f'    ?propertyShapeSource {SHACL_CLASS} <{target_class}>.\n'
            f'    ?targetShape {SHACL_NOT} ?propertyShapeTarget. \n'
            f'    ?propertyShapeTarget {SHACL_CLASS} <{source_class}>.\n'
            f' }}\n'
            f' WHERE {{\n'
            f'   ?sourceShape a {SHACL_NODE_SHAPE} ;\n'
            f'     {SHACL_TARGET_CLASS} <{source_class}> .\n'
            f'   ?targetShape a {SHACL_NODE_SHAPE} ;\n'
            f'     {SHACL_TARGET_CLASS} <{target_class}> .\n'
            f'    ?sourceShape {SHACL_NOT} ?propertyShapeSource.\n'
            f'    ?propertyShapeSource {SHACL_CLASS} <{target_class}>.\n'
            f'    ?targetShape {SHACL_NOT} ?propertyShapeTarget. \n'
            f'    ?propertyShapeTarget {SHACL_CLASS} <{source_class}>.\n'
            f'}}'
        )
        #print(remove_disjoint_class_query)
        output_shapes.update(remove_disjoint_class_query)

def add_object_property_shacl(change,change_data, output_shapes):
    """
       Adds an object property to the NodeShape indicated in the domain. For a full change in the Property Shape the domain, property and range additions are needed.  
       Args:
           change: the URI of the change which needs to be of the type addObjectProperty
       Returns:
           the output_shapes updated with the added predicate object maps. 
    """
    query = f' SELECT DISTINCT ?domain ?property ?range WHERE {{ ' \
            f' <{change}> {OCH_ADDED_OBJECT_PROPERTY} ?property .' \
            f' ?domainchange {OCH_ADDED_DOMAIN_TO_PROPERTY} ?property.' \
            f' ?domainchange {OCH_ADDED_DOMAIN} ?domain.' \
            f' ?rangechange {OCH_ADDED_RANGE_TO_PROPERTY} ?property.' \
            f' ?rangechange {OCH_ADDED_OBJECT_RANGE} ?range. }}'

    for result in change_data.query(query):
        property_domain = result["domain"]
        property_predicate = result["property"]
        property_range = result["range"]
        if "#" in property_predicate:
            property_local = property_predicate.split("#")[-1]
        elif "/" in property_predicate:
            property_local = property_predicate.split("/")[-1]
        else:
            property_local = property_predicate
        insert_object_property_query = (
            f' PREFIX {SHACL_PREFIX}: <{SHACL_URI}>'
            f' PREFIX {EXAMPLE_PREFIX}: <{EXAMPLE_URI}>'
            f' INSERT {{ '
            f'   ?nodeShape {SHACL_PROPERTY} {EXAMPLE_PREFIX}:{property_local}Shape . '
            f'   {EXAMPLE_PREFIX}:{property_local}Shape  {SHACL_PATH} <{property_predicate}> ; '
            f'     {SHACL_CLASS} <{property_range}> . '
            f' }} '
            f' WHERE {{ '
            f'   ?nodeShape a {SHACL_NODE_SHAPE} ; '
            f'             {SHACL_TARGET_CLASS} <{property_domain}> . '
            f' }}'
        )
        #print(insert_object_property_query)
        output_shapes.update(insert_object_property_query)

def remove_object_property_shacl(change, change_data, output_shapes):
    """
       Removes an object property from the NodeShape indicated in the domain. For a full change in the Property Shape the domain, property and range removals are needed.
       Args:
           change: the URI of the change which needs to be of the type removeObjectProperty
       Returns:
           the output_shapes updated with the property shape removed.
    """
    query = f' SELECT DISTINCT ?domain ?property ?range WHERE {{ ' \
            f' <{change}> {OCH_REMOVED_OBJECT_PROPERTY} ?property .' \
            f' ?domainchange {OCH_REMOVED_DOMAIN_TO_PROPERTY} ?property.' \
            f' ?domainchange {OCH_REMOVED_DOMAIN} ?domain.' \
            f' ?rangechange {OCH_REMOVED_RANGE_TO_PROPERTY} ?property.' \
            f' ?rangechange {OCH_REMOVED_OBJECT_RANGE} ?range. }}'

    for result in change_data.query(query):
        property_domain = result["domain"]
        property_predicate = result["property"]
        property_range = result["range"]

        # Remove property shape whether it is a blank node (sh:property) or a full PropertyShape (URI)
        delete_object_property_query = (
            f' PREFIX {SHACL_PREFIX}: <{SHACL_URI}>\n'
            f' DELETE {{\n'
            f'   ?nodeShape {SHACL_PROPERTY} ?propertyShape .\n'
            f'   ?propertyShape {SHACL_PATH} <{property_predicate}> ;\n'
            f'                 {SHACL_CLASS} <{property_range}> .\n'
            f'   ?propertyShape ?pp ?po .\n'
            f'   ?list ?lp ?lo .\n'
            f'   ?listItem ?listItemP ?listItemO .\n'
            f'   ?restNode ?restP ?restO .\n'
            f' }}\n'
            f' WHERE {{\n'
            f'   ?nodeShape a {SHACL_NODE_SHAPE} ;\n'
            f'             {SHACL_TARGET_CLASS} <{property_domain}> ;\n'
            f'             {SHACL_PROPERTY} ?propertyShape .\n'
            f'   ?propertyShape {SHACL_PATH} <{property_predicate}> ;\n'
            f'                 {SHACL_CLASS} <{property_range}> .\n'
            f'   OPTIONAL {{ ?propertyShape ?pp ?po .\n'
            f'   OPTIONAL {{\n'
            f'       ?propertyShape ?listPred ?list .\n'
            f'       FILTER(?listPred IN ({SHACL_IN}, {SHACL_OR}, {SHACL_AND}, {SHACL_XONE}))\n'
            f'       ?list {RDF_REST}*/{RDF_FIRST} ?listItem .\n'
            f'       ?list ?lp ?lo .\n'
            f'       OPTIONAL {{ ?listItem ?listItemP ?listItemO . }}\n'
            f'       ?list {RDF_REST}* ?restNode .\n'
            f'       ?restNode ?restP ?restO .\n'
            f'     }}\n'
            f' }}\n'
            f'}}'
        )
        #print(delete_object_property_query)
        output_shapes.update(delete_object_property_query)

def add_data_property_shacl(change, change_data, output_shapes):
    """
       Adds a data property to the NodeShape indicated in the domain. For a full change in the Property Shape the domain, property and range additions are needed.
       Args:
           change: the URI of the change which needs to be of the type addDataProperty
       Returns:
           the output_shapes updated with the added data property shape.
    """
    query = f' SELECT DISTINCT ?domain ?property ?range WHERE {{ ' \
            f' <{change}> {OCH_ADDED_DATA_PROPERTY} ?property .' \
            f' ?domainchange {OCH_ADDED_DOMAIN_TO_PROPERTY} ?property.' \
            f' ?domainchange {OCH_ADDED_DOMAIN} ?domain.' \
            f' ?rangechange {OCH_ADDED_RANGE_TO_PROPERTY} ?property.' \
            f' ?rangechange {OCH_ADDED_DATA_RANGE} ?range. }}'

    for result in change_data.query(query):
        property_domain = result["domain"]
        property_predicate = result["property"]
        property_range = result["range"]
        if "#" in property_predicate:
            property_local = property_predicate.split("#")[-1]
        elif "/" in property_predicate:
            property_local = property_predicate.split("/")[-1]
        else:
            property_local = property_predicate
        insert_data_property_query = (
            f' PREFIX {SHACL_PREFIX}: <{SHACL_URI}>'
            f' PREFIX {EXAMPLE_PREFIX}: <{EXAMPLE_URI}>'
            f' INSERT {{ '
            f'   ?nodeShape {SHACL_PROPERTY} {EXAMPLE_PREFIX}:{property_local}Shape . '
            f'   {EXAMPLE_PREFIX}:{property_local}Shape  {SHACL_PATH} <{property_predicate}> ; '
            f'     {SHACL_DATATYPE} <{property_range}> . '
            f' }} '
            f' WHERE {{ '
            f'   ?nodeShape a {SHACL_NODE_SHAPE} ; '
            f'             {SHACL_TARGET_CLASS} <{property_domain}> . '
            f' }}'
        )
        print(insert_data_property_query)
        output_shapes.update(insert_data_property_query)

def remove_data_property_shacl(change, change_data, output_shapes):
    """
       Removes a data property from the NodeShape indicated in the domain. For a full change in the Property Shape the domain, property and range removals are needed.
       Args:
           change: the URI of the change which needs to be of the type removeDataProperty
       Returns:
           the output_shapes updated with the data property shape removed.
    """
    query = f' SELECT DISTINCT ?domain ?property ?range WHERE {{ ' \
            f' <{change}> {OCH_REMOVED_DATA_PROPERTY} ?property .' \
            f' ?domainchange {OCH_REMOVED_DOMAIN_TO_PROPERTY} ?property.' \
            f' ?domainchange {OCH_REMOVED_DOMAIN} ?domain.' \
            f' ?rangechange {OCH_REMOVED_RANGE_TO_PROPERTY} ?property.' \
            f' ?rangechange {OCH_REMOVED_DATA_RANGE} ?range. }}'

    for result in change_data.query(query):
        property_domain = result["domain"]
        property_predicate = result["property"]
        property_range = result["range"]

        delete_data_property_query = (
            f' PREFIX {SHACL_PREFIX}: <{SHACL_URI}>\n'
            f' DELETE {{\n'
            f'   ?nodeShape {SHACL_PROPERTY} ?propertyShape .\n'
            f'   ?propertyShape {SHACL_PATH} <{property_predicate}> ;\n'
            f'                 {SHACL_DATATYPE} <{property_range}> .\n'
            f'   ?propertyShape ?pp ?po .\n'
            f'   ?list ?lp ?lo .\n'
            f'   ?listItem ?listItemP ?listItemO .\n'
            f'   ?restNode ?restP ?restO .\n'
            f' }}\n'
            f' WHERE {{\n'
            f'   ?nodeShape a {SHACL_NODE_SHAPE} ;\n'
            f'             {SHACL_TARGET_CLASS} <{property_domain}> ;\n'
            f'             {SHACL_PROPERTY} ?propertyShape .\n'
            f'   ?propertyShape {SHACL_PATH} <{property_predicate}> ;\n'
            f'                 {SHACL_DATATYPE} <{property_range}> .\n'
            f'   OPTIONAL {{ ?propertyShape ?pp ?po .\n'
            f'   OPTIONAL {{\n'
            f'       ?propertyShape ?listPred ?list .\n'
            f'       FILTER(?listPred IN ({SHACL_IN}, {SHACL_OR}, {SHACL_AND}, {SHACL_XONE}))\n'
            f'       ?list {RDF_REST}*/{RDF_FIRST} ?listItem .\n'
            f'       ?list ?lp ?lo .\n'
            f'       OPTIONAL {{ ?listItem ?listItemP ?listItemO . }}\n'
            f'       ?list {RDF_REST}* ?restNode .\n'
            f'       ?restNode ?restP ?restO .\n'
            f'     }}\n'
            f' }}\n'
            f'}}'
        )
        print(delete_data_property_query)
        output_shapes.update(delete_data_property_query)

def add_characteristic_shacl(change, change_data, output_shapes):
    """
       Modifies the property shape corresponding to a given property to add restrictions based on the added characteristic.
       Args:
           change: the URI of the change which needs to be of the type addCharacteristic
       Returns:
           the output_shapes updated with the data property shape modified.
    """
    print("Entra en la función add_characteristic_shacl")
    query = f' SELECT DISTINCT ?property ?characteristic WHERE {{ ' \
            f' <{change}> {OCH_ADDED_CHARACTERISTIC_TO_PROPERTY} ?property ;' \
            f'            {OCH_ADDED_CHARACTERISTIC} ?characteristic }}'
    print(query)
    for result in change_data.query(query):
        property = result["property"]
        characteristic = result["characteristic"]
        print(f"Property: {property}, Characteristic: {characteristic}")
        # Add SHACL restrictions for property characteristics
        if characteristic == URIRef(OWL_FUNCTIONAL_PROPERTY_URI):
            #print("Entra en la condición de OWL_FUNCTIONAL_PROPERTY")
            # Functional property: sh:maxCount 1
            insert_characteristic_query = (
            f' PREFIX {SHACL_PREFIX}: <{SHACL_URI}>'
            f' INSERT {{ ?propertyShape {SHACL_MAX_COUNT} 1 }}'
            f' WHERE {{ ?propertyShape {SHACL_PATH} <{property}> }}'
            )
            print(insert_characteristic_query)
            output_shapes.update(insert_characteristic_query)
        elif characteristic == URIRef(OWL_SYMMETRIC_PROPERTY_URI):
            # Symmetric property: custom SHACL-SPARQL constraint
            insert_characteristic_query = (
            f' PREFIX {SHACL_PREFIX}: <{SHACL_URI}>'
            f' INSERT {{ ?propertyShape {SHACL_SPARQL} [ a {SHACL_SPARQL_CONSTRAINT} ; {SHACL_SPARQL_SELECT} "SELECT $this WHERE {{ $this <{property}> ?v . FILTER NOT EXISTS {{ ?v <{property}> $this }} }}" ] }}'
            f' WHERE {{ ?propertyShape {SHACL_PATH} <{property}> }}'
            )
            print(insert_characteristic_query)
            output_shapes.update(insert_characteristic_query)
        elif characteristic == URIRef(OWL_ASYMMETRIC_PROPERTY_URI):
            # Asymmetric property: custom SHACL-SPARQL constraint
            insert_characteristic_query = (
            f' PREFIX {SHACL_PREFIX}: <{SHACL_URI}>'
            f' INSERT {{ ?propertyShape {SHACL_SPARQL} [ a {SHACL_SPARQL_CONSTRAINT} ; {SHACL_SPARQL_SELECT} "SELECT $this WHERE {{ $this <{property}> ?v . FILTER EXISTS {{ ?v <{property}> $this }} }}" ] }}'
            f' WHERE {{ ?propertyShape {SHACL_PATH} <{property}> }}'
            )
            print(insert_characteristic_query)
            output_shapes.update(insert_characteristic_query)
        elif characteristic == URIRef(OWL_REFLEXIVE_PROPERTY_URI):
            # Reflexive property: custom SHACL-SPARQL constraint
            insert_characteristic_query = (
            f' PREFIX {SHACL_PREFIX}: <{SHACL_URI}>'
            f' INSERT {{ ?propertyShape {SHACL_SPARQL} [ a {SHACL_SPARQL_CONSTRAINT} ; {SHACL_SPARQL_SELECT} "SELECT $this WHERE {{ FILTER NOT EXISTS {{ $this <{property}> $this }} }}" ] }}'
            f' WHERE {{ ?propertyShape {SHACL_PATH} <{property}> }}'
            )
            print(insert_characteristic_query)
            output_shapes.update(insert_characteristic_query)
        elif characteristic == URIRef(OWL_IRREFLEXIVE_PROPERTY_URI):
            # Irreflexive property: custom SHACL-SPARQL constraint
            insert_characteristic_query = (
            f' PREFIX {SHACL_PREFIX}: <{SHACL_URI}>'
            f' INSERT {{ ?propertyShape {SHACL_SPARQL} [ a {SHACL_SPARQL_CONSTRAINT} ; {SHACL_SPARQL_SELECT} "SELECT $this WHERE {{ $this <{property}> $this }}" ] }}'
            f' WHERE {{ ?propertyShape {SHACL_PATH} <{property}> }}'
            )
            print(insert_characteristic_query)
            output_shapes.update(insert_characteristic_query)
        elif characteristic == URIRef(OWL_INVERSE_FUNCTIONAL_PROPERTY_URI):
            # Inverse functional property: sh:maxCount 1 on inverse path
            # Use a blank node for the property shape and avoid using a URI for the shape
            if "#" in property:
                property_local = property.split("#")[-1]
            elif "/" in property:
                property_local = property.split("/")[-1]
            else:
                property_local = property
            insert_characteristic_query = (
                f' PREFIX {SHACL_PREFIX}: <{SHACL_URI}>'
                f' PREFIX {EXAMPLE_PREFIX}: <{EXAMPLE_URI}>'
                f' INSERT DATA {{ '
                f'   {EXAMPLE_PREFIX}:{property_local}InvFunctShape a {SHACL_PROPERTY_SHAPE} ; '
                f'      {SHACL_PATH} [ {SHACL_INVERSE_PATH} <{property}> ] ; '
                f'      {SHACL_MAX_COUNT} 1 . '
                f' }} '
            )
            print(insert_characteristic_query)
            output_shapes.update(insert_characteristic_query)
        elif characteristic == OWL_TRANSITIVE_PROPERTY:
            # Transitive property: custom SHACL-SPARQL constraint
            insert_characteristic_query = (
            f' PREFIX {SHACL_PREFIX}: <{SHACL_URI}>'
            f' INSERT {{ ?propertyShape {SHACL_SPARQL} [ a {SHACL_SPARQL_CONSTRAINT} ; {SHACL_SPARQL_SELECT} "SELECT $this WHERE {{ $this <{property}> ?v1 . ?v1 <{property}> ?v2 . FILTER NOT EXISTS {{ $this <{property}> ?v2 }} }}" ] }}'
            f' WHERE {{ ?propertyShape {SHACL_PATH} <{property}> }}'
            )
            output_shapes.update(insert_characteristic_query)

def remove_characteristic_shacl(change, change_data, output_shapes):
    #print("Entra en la función remove_characteristic_shacl")
    """
       Modifies the property shape corresponding to a given property to remove restrictions based on the removed characteristic.
       Args:
           change: the URI of the change which needs to be of the type removeCharacteristic
       Returns:
           the output_shapes updated with the data property shape modified.
    """
    query = f' SELECT DISTINCT ?property ?characteristic WHERE {{ ' \
            f' <{change}> {OCH_REMOVED_CHARACTERISTIC_FROM_PROPERTY} ?property ;' \
            f'            {OCH_REMOVED_CHARACTERISTIC} ?characteristic }}'
    print(query)
    for result in change_data.query(query):
        property = result["property"]
        characteristic = result["characteristic"]
        print(f"Property: {property}, Characteristic: {characteristic}")
        # Remove SHACL restrictions for property characteristics
        if characteristic == URIRef(OWL_FUNCTIONAL_PROPERTY_URI):
            #print("Entra en la condición de OWL_FUNCTIONAL_PROPERTY")
            # Functional property: sh:maxCount 1
            delete_characteristic_query = (
                f' PREFIX {SHACL_PREFIX}: <{SHACL_URI}>'
                f' DELETE {{ ?propertyShape {SHACL_MAX_COUNT} 1 }}'
                f' WHERE {{ ?propertyShape {SHACL_PATH} <{property}> }}'
            )
            print(delete_characteristic_query)
            output_shapes.update(delete_characteristic_query)
        elif characteristic == URIRef(OWL_SYMMETRIC_PROPERTY_URI):
            print(f"Entra en la condición de remove OWL_SYMMETRIC_PROPERTY: {property}")
            # Symmetric property: custom SHACL-SPARQL constraint
            delete_characteristic_query = (
                f' PREFIX {SHACL_PREFIX}: <{SHACL_URI}>'
                f' DELETE {{ ?propertyShape {SHACL_SPARQL} ?constraintNode .'                
                f' ?constraintNode a {SHACL_SPARQL_CONSTRAINT} ; '
                f' {SHACL_SPARQL_SELECT} "SELECT $this WHERE {{ $this <{property}> ?v . FILTER NOT EXISTS {{ ?v <{property}> $this }} }}" }}'
                f' WHERE {{ ?propertyShape {SHACL_PATH} <{property}> . '
                f' ?propertyShape {SHACL_SPARQL} ?constraintNode . '
                f' ?constraintNode a {SHACL_SPARQL_CONSTRAINT} ; '
                f' {SHACL_SPARQL_SELECT} "SELECT $this WHERE {{ $this <{property}> ?v . FILTER NOT EXISTS {{ ?v <{property}> $this }} }}" }}'
            )
            print(delete_characteristic_query)
            output_shapes.update(delete_characteristic_query)
        elif characteristic == URIRef(OWL_ASYMMETRIC_PROPERTY_URI):
            # Asymmetric property: custom SHACL-SPARQL constraint
            #print(f"Entra en la condición de remove OWL_ASYMMETRIC_PROPERTY: {property}")
            delete_characteristic_query = (
                f' PREFIX {SHACL_PREFIX}: <{SHACL_URI}>'
                f' DELETE {{ ?propertyShape {SHACL_SPARQL} ?constraintNode .'
                f' ?constraintNode a {SHACL_SPARQL_CONSTRAINT} ; '
                f' {SHACL_SPARQL_SELECT} "SELECT $this WHERE {{ $this <{property}> ?v . FILTER EXISTS {{ ?v <{property}> $this }} }}" }}'
                f' WHERE {{ ?propertyShape {SHACL_PATH} <{property}> . '
                f' ?propertyShape {SHACL_SPARQL} ?constraintNode . '
                f' ?constraintNode a {SHACL_SPARQL_CONSTRAINT} ; '
                f' {SHACL_SPARQL_SELECT} "SELECT $this WHERE {{ $this <{property}> ?v . FILTER EXISTS {{ ?v <{property}> $this }} }}" }}'
            )
            print(delete_characteristic_query)
            output_shapes.update(delete_characteristic_query)
        elif characteristic == URIRef(OWL_REFLEXIVE_PROPERTY_URI):
            # Reflexive property: custom SHACL-SPARQL constraint
            delete_characteristic_query = (
                f' PREFIX {SHACL_PREFIX}: <{SHACL_URI}>'
                f' DELETE {{ ?propertyShape {SHACL_SPARQL} ?constraintNode .'
                f' ?constraintNode a {SHACL_SPARQL_CONSTRAINT} ; '
                f' {SHACL_SPARQL_SELECT} "SELECT $this WHERE {{ FILTER NOT EXISTS {{ $this <{property}> $this }} }}" }}'
                f' WHERE {{ ?propertyShape {SHACL_PATH} <{property}> . '
                f' ?propertyShape {SHACL_SPARQL} ?constraintNode . '
                f' ?constraintNode a {SHACL_SPARQL_CONSTRAINT} ; '
                f' {SHACL_SPARQL_SELECT} "SELECT $this WHERE {{ FILTER NOT EXISTS {{ $this <{property}> $this }} }}" }}'
            )
            print(delete_characteristic_query)
            output_shapes.update(delete_characteristic_query)
        elif characteristic == URIRef(OWL_IRREFLEXIVE_PROPERTY_URI):
            # Irreflexive property: custom SHACL-SPARQL constraint
            delete_characteristic_query = (
                f' PREFIX {SHACL_PREFIX}: <{SHACL_URI}>'
                f' DELETE {{ ?propertyShape {SHACL_SPARQL} ?constraintNode .'
                f' ?constraintNode a {SHACL_SPARQL_CONSTRAINT} ; '
                f' {SHACL_SPARQL_SELECT} "SELECT $this WHERE {{ $this <{property}> $this }}" }}'
                f' WHERE {{ ?propertyShape {SHACL_PATH} <{property}> . '
                f' ?propertyShape {SHACL_SPARQL} ?constraintNode . '
                f' ?constraintNode a {SHACL_SPARQL_CONSTRAINT} ; '
                f' {SHACL_SPARQL_SELECT} "SELECT $this WHERE {{ $this <{property}> $this }}" }}'
            )
            print(delete_characteristic_query)
            output_shapes.update(delete_characteristic_query)
        elif characteristic == URIRef(OWL_INVERSE_FUNCTIONAL_PROPERTY_URI):
            # Inverse functional property: sh:uniqueLang or custom constraint
            delete_characteristic_query = (
                f' PREFIX {SHACL_PREFIX}: <{SHACL_URI}>'
                f' PREFIX {EXAMPLE_PREFIX}: <{EXAMPLE_URI}>'
                f' DELETE {{ '
                f'    ?shape a {SHACL_PROPERTY_SHAPE} ; '
                f'      {SHACL_PATH} ?pathbnode . '
                f'      ?pathbnode {SHACL_INVERSE_PATH} <{property}> . '
                f'      ?shape {SHACL_MAX_COUNT} 1 . '
                f' }} '
                f' WHERE {{ ?shape a {SHACL_PROPERTY_SHAPE} ; '
                f'      {SHACL_PATH} ?pathbnode . '
                f'      ?pathbnode {SHACL_INVERSE_PATH} <{property}> . '
                f'      ?shape {SHACL_MAX_COUNT} 1 . '
                f' }}'
            )
            print(delete_characteristic_query)
            output_shapes.update(delete_characteristic_query)
        elif characteristic == OWL_TRANSITIVE_PROPERTY:
            # Transitive property: custom SHACL-SPARQL constraint
            delete_characteristic_query = (
                f' PREFIX {SHACL_PREFIX}: <{SHACL_URI}>'
                f' DELETE {{ ?propertyShape {SHACL_SPARQL} ?constraintNode }}'
                f' WHERE {{ ?propertyShape {SHACL_PATH} <{property}> . '
                f' ?propertyShape {SHACL_SPARQL} ?constraintNode . '
                f' ?constraintNode a {SHACL_SPARQL_CONSTRAINT} ; '
                f' {SHACL_SPARQL_SELECT} "SELECT $this WHERE {{ $this <{property}> ?v1 . ?v1 <{property}> ?v2 . FILTER NOT EXISTS {{ $this <{property}> ?v2 }} }}" }}'
            )
            output_shapes.update(delete_characteristic_query)