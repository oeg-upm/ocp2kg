from rdflib import Variable
from .constants import *


# ---------------------------------------------------------------------------------------------------------------------------

def add_class(change, change_data, output_mappings):
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
def remove_class(change,change_data, output_mappings, review_mappings, ontology):
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

def add_super_class(change,change_data, output_mappings):
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
        print(insert_super_class_query)
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
def remove_super_class(change,change_data, output_mappings):
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
                                   f' WHERE {{ ' \
                                   f'       ?triplesMap {R2RML_SUBJECT} ?subjectMap . ' \
                                   f'       ?subjectMap {R2RML_CLASS} <{super_class}>, <{sub_class}> .}}'
        print(delete_super_class_query)
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

def add_object_property(change,change_data, output_mappings):
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
def remove_object_property(change, change_data, output_mappings):
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
def add_data_property(change,change_data, output_mappings):
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
    print(query)
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
        print(insert_data_property_query)
        output_mappings.update(insert_data_property_query)


# -----------------------------------------------------------------------------------------------------------------------------------
def remove_data_property(change,change_data, output_mappings):
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
    print(query)
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
        print(remove_data_property_query)
        output_mappings.update(remove_data_property_query)



# -------------------------------------------------------------------------------------------------------------
