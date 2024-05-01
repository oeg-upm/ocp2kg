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
    check_query = f'ASK {{  ?class {RDF_TYPE} {R2RML_TRIPLES_MAP} .' \
                  f'        ?class {R2RML_SUBJECT} ?subject . ' \
                  f'        ?subject {R2RML_CLASS} <{added_class}> }}'

    check_res = output_mappings.query(check_query)
    if not check_res.askAnswer:
        insert_class_query = f' PREFIX {R2RML_PREFIX}: <{R2RML_URI}>' \
                             f' PREFIX {RML_PREFIX}: <{RML_URI}>' \
                             f' INSERT DATA {{' \
                             f'     <{added_class}> {RDF_TYPE} {R2RML_TRIPLES_MAP}; ' \
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
    # First we query the change data to obtain the class to be deleted.
    q = """
    SELECT DISTINCT ?fullname
    WHERE {
        <""" + change + """> omv:deletedClass ?fullname .
    }
    """
    for r in change_data.query(q):
        full_name = r["fullname"]
    ##CHECK wether this class is a subclass from another one for different treatments.
    q = """
   ASK { <""" + full_name + """> rdfs:subClassOf ?x}
    """
    answer = ontology.query(q)
    # CASE 1:  If C is not subclass remove all TriplesMap that instanciate entities of the class C and the POM where the parentTriplesMap in the RefObjectMap is the 4
    # identifier of those TriplesMaps.
    # The following query Removes the TriplesMap from that class, POMs that contain it as a rr:template, and those that contain it as a join condition.
    # The deleted triples are added to a file so that the user can correct any incorrect asumptions
    # The assumption is that the appearances of the term are deleted in all classes, they could be replaced by superclass and that's why is added to review file.
    if (answer == True):
        qaux = """
    PREFIX rr: <http://www.w3.org/ns/r2rml#>
   PREFIX rml: <http://semweb.mmlab.be/ns/rml#>

   CONSTRUCT { 
      ?triplesmap rr:subjectMap ?subject.
      ?subject ?subject_term ?subject_value .
      ?subject rr:class <""" + full_name + """> .

      ?triplesmap rr:logicalSource ?logicalSource .
      ?logicalSource ?logicalSource_term ?logicalSource_value .

      #POM
      ?triplesmap rr:predicateObjectMap ?pom.
      ?pom ?predicate_property ?predicate .
      ?predicate ?predicate_term ?predicate_value .
      ?pom ?object_property ?object.
      ?object ?oject_term ?object_value.
   
      #JOINS
      ?triplesmap rr:predicateObjectMap ?pom2.
      ?pom2 ?predicate_property2 ?predicate2 .
      ?predicate2 ?predicate_term2 ?predicate_value2 .
      ?pom2 rr:objectMap ?object2.
      ?object2 rr:parentTriplesMap ?parent_tm .
      ?object2 rr:joinCondition ?join_condition .
      ?join_condition ?conditions ?condition_values .
      
      #DELETION OF JOINS WHERE TM IS USED
      ?parent_triplesMap rr:predicateObjectMap ?parent_pom.
      ?parent_pom rr:objectMap ?parent_object.
      ?parent_object rr:parentTriplesMap ?triplesmap.
      ?parent_object rr:joinConditions ?parent_joinConditions .
      ?parent_joinConditions ?parent_conditions ?parent_conditions_values . 
   } 

   WHERE{ 
      ?triplesmap rr:subjectMap ?subject.
      ?subject ?subject_term ?subject_value .
      ?subject rr:class <""" + full_name + """> .

      ?triplesmap rr:logicalSource ?logicalSource .
      ?logicalSource ?logicalSource_term ?logicalSource_value .

      #POM
      OPTIONAL{
         ?triplesmap rr:predicateObjectMap ?pom.
         ?pom rr:predicate|rr:predicateMap ?predicate .
         OPTIONAL {?predicate ?predicate_term ?predicate_value .}
         ?pom rr:objectMap|rr:object ?object.
         OPTIONAL {?object ?oject_term ?object_value.}
      }
      #REFOBJECTMAP
      OPTIONAL{
         ?triplesmap rr:predicateObjectMap ?pom2.
         ?pom2 rr:predicate|rr:predicateMap ?predicate2 .
         OPTIONAL { ?predicate2 ?predicate_term2 ?predicate_value2 .}
         ?pom2 rr:objectMap ?object2.
         ?object2 rr:parentTriplesMap ?parent_tm .
         OPTIONAL {
            ?object2 rr:joinCondition ?join_condition .
            ?join_condition ?conditions ?condition_values .
         }
      }
      #DELETION OF JOINS
      OPTIONAL{
         ?parent_triplesMap rr:predicateObjectMap ?parent_pom.
         ?parent_pom rr:objectMap ?parent_object.
         ?parent_object rr:parentTriplesMap ?triplesmap.
         OPTIONAL {
            ?parent_object rr:joinConditions ?parent_joinConditions .
            ?parent_joinConditions ?parent_conditions ?parent_conditions_values .
         }
      }
   }     """
        triples_to_be_checked = output_mappings.query(qaux)
        for trip in triples_to_be_checked:
            review_mappings.add(trip)
    # Removes all rules that create instances and properties of %CLASS%.
    q1 = """
   PREFIX rr: <http://www.w3.org/ns/r2rml#>
   PREFIX rml: <http://semweb.mmlab.be/ns/rml#>

   DELETE { 
      ?triplesmap rr:subjectMap ?subject.
      ?subject ?subject_term ?subject_value .
      ?subject rr:class <""" + full_name + """> .

      ?triplesmap rr:logicalSource ?logicalSource .
      ?logicalSource ?logicalSource_term ?logicalSource_value .

      #POM
      ?triplesmap rr:predicateObjectMap ?pom.
      ?pom ?predicate_property ?predicate .
      ?predicate ?predicate_term ?predicate_value .
      ?pom ?object_property ?object.
      ?object ?oject_term ?object_value.
   
      #JOINS
      ?triplesmap rr:predicateObjectMap ?pom2.
      ?pom2 ?predicate_property2 ?predicate2 .
      ?predicate2 ?predicate_term2 ?predicate_value2 .
      ?pom2 rr:objectMap ?object2.
      ?object2 rr:parentTriplesMap ?parent_tm .
      ?object2 rr:joinCondition ?join_condition .
      ?join_condition ?conditions ?condition_values .
      
      #DELETION OF JOINS WHERE TM IS USED
      ?parent_triplesMap rr:predicateObjectMap ?parent_pom.
      ?parent_pom rr:objectMap ?parent_object.
      ?parent_object rr:parentTriplesMap ?triplesmap.
      ?parent_object rr:joinConditions ?parent_joinConditions .
      ?parent_joinConditions ?parent_conditions ?parent_conditions_values . 
   } 

   WHERE{ 
      ?triplesmap rr:subjectMap ?subject.
      ?subject ?subject_term ?subject_value .
      ?subject rr:class <""" + full_name + """> .

      ?triplesmap rr:logicalSource ?logicalSource .
      ?logicalSource ?logicalSource_term ?logicalSource_value .

      #POM
      OPTIONAL{
         ?triplesmap rr:predicateObjectMap ?pom.
         ?pom rr:predicate|rr:predicateMap ?predicate .
         OPTIONAL {?predicate ?predicate_term ?predicate_value .}
         ?pom rr:objectMap|rr:object ?object.
         OPTIONAL {?object ?oject_term ?object_value.}
      }
      #REFOBJECTMAP
      OPTIONAL{
         ?triplesmap rr:predicateObjectMap ?pom2.
         ?pom2 rr:predicate|rr:predicateMap ?predicate2 .
         OPTIONAL { ?predicate2 ?predicate_term2 ?predicate_value2 .}
         ?pom2 rr:objectMap ?object2.
         ?object2 rr:parentTriplesMap ?parent_tm .
         OPTIONAL {
            ?object2 rr:joinCondition ?join_condition .
            ?join_condition ?conditions ?condition_values .
         }
      }
      #DELETION OF JOINS
      OPTIONAL{
         ?parent_triplesMap rr:predicateObjectMap ?parent_pom.
         ?parent_pom rr:objectMap ?parent_object.
         ?parent_object rr:parentTriplesMap ?triplesmap.
         OPTIONAL {
            ?parent_object rr:joinConditions ?parent_joinConditions .
            ?parent_joinConditions ?parent_conditions ?parent_conditions_values .
         }
      }
   }
         """
    output_mappings.update(q1)


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

        for result in ontology.query(query_data_properties):
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

        for result in ontology.query(query_object_properties):
            object_property = result["objectproperty"]
            property_range = result["range"]

            insert_object_property_query = f' PREFIX {R2RML_PREFIX}: <{R2RML_URI}>' \
                                           f' PREFIX {RML_PREFIX}: <{RML_URI}>' \
                                           f' INSERT {{  ' \
                                           f'     ?triplesMap {R2RML_PREDICATE_OBJECT_MAP} [ ' \
                                           f'         {R2RML_PREDICATE} <{object_property}> ; ' \
                                           f'         {R2RML_OBJECT} [ ' \
                                           f'             {R2RML_PARENT_TRIPLESMAP} ?parent_triplesMap;' \
                                           f'             {R2RML_JOIN_CONITION} [ ' \
                                           f'               {R2RML_CHILD} "XXXX"; {R2RML_PARENT} "XXXX" ' \
                                           f'          ] ] ]. }}' \
                                           f'  WHERE {{' \
                                           f'     ?triplesMap {R2RML_SUBJECT} ?subjectMap . ' \
                                           f'     ?subjectMap {R2RML_CLASS} <{super_class}>, <{sub_class}> .' \
                                           f'     ?parent_triplesMap {R2RML_SUBJECT} ?parent_subjectMap . ' \
                                           f'     ?parent_subjectMap {R2RML_CLASS} {property_range} }}'

            output_mappings.update(insert_object_property_query)


# --------------------------------------------------------------------------------------------------------------
def RemoveSubClass(change):
    # When removing the subclass relationship between two classes the child one loses the parent in the rr:class part.
    q = """
    SELECT DISTINCT ?parent ?child
    WHERE {
        <""" + change + """> omv:subRemoveSubClass ?child.
        <""" + change + """> omv:objRemoveSubClass ?parent.
    }
    """
    for r in change_data.query(q):
        parent = r["parent"]
        child = r["child"]
    q1 = """
      PREFIX rr: <http://www.w3.org/ns/r2rml#>
      PREFIX rml: <http://semweb.mmlab.be/ns/rml#>

      DELETE {   
         ?subjectMap rr:class <""" + parent + """>.
      }
      WHERE {
         ?triplesmap rr:subjectMap ?subjectMap.
         ?subjectMap rr:class <""" + parent + """>, <""" + child + """>.
      }
   """""
    output_mappings.update(q1)
    # Query to obtain those Data Properties from the father that the child class has inherited.
    q2 = """
   SELECT DISTINCT ?dataproperty 
   WHERE {
      ?dataproperty  a owl:DatatypeProperty;
                     rdfs:domain <""" + parent + """>, <""" + child + """>.
   } 
   """
    for r in ontology.query(q2):
        dataprop = r["dataproperty"]
        # This triggers:
        # Remove DataProperties where %DATAPROPERTY% has as domain %SUBCLASS%
        # For each DATAPROPERTY of %SUBCLASS%:
        # Run RemoveDataProperty.rq with %CLASS% = %SUPERCLASS% .
        q3 = """
           PREFIX rr: <http://www.w3.org/ns/r2rml#>
            PREFIX rml: <http://semweb.mmlab.be/ns/rml#>


   DELETE { 
      ?triplesmap rr:predicateObjectMap ?pom.
      ?pom rr:predicate <""" + dataprop + """> . #if comes from the ontology, it's going to be always constant

      ?pom rr:objectMap|rr:object ?objectMap. #either rr:objectMap or rr:object
      ?objectMap ?object_term ?objectValue . #removes everything under objectMap (including language, datatype or termType)
   }
   WHERE {
      ?triplesmap  rr:subjectMap ?subjectMap.
      ?subjectMap rr:class <""" + child + """>.

      ?triplesmap rr:predicateObjectMap ?pom.
         ?pom rr:predicate <""" + dataprop + """> . #if comes from the ontology, it's going to be always constant

      ?pom rr:objectMap|rr:object ?objectMap.
      OPTIONAL { ?objectMap ?object_term ?objectValue }.
         
   }
   """
        output_mappings.update(q3)
    # Remove ObjectProperties where %OBJECTPROPERTY% has as domain %SUBCLASS%
    # For each OBJECTPROPERTY of %SUBCLASS%:
    # Run RemoveObjectProperty.rq with %CLASS% = %SUPERCLASS% .
    q4 = """
   SELECT DISTINCT ?objectproperty 
   WHERE {
      ?objectproperty  a owl:ObjectProperty;
                     rdfs:domain <""" + parent + """>, <""" + child + """>.
   } 
   """
    for r in ontology.query(q4):
        objprop = r["objectproperty"]
        q5 = """
           PREFIX rr: <http://www.w3.org/ns/r2rml#>
            PREFIX rml: <http://semweb.mmlab.be/ns/rml#>

   DELETE { 
      ?triplesmap rr:predicateObjectMap ?pom.
      ?pom rr:predicate <""" + objprop + """> . #if comes from the ontology, it's going to be always constant

      ?pom rr:objectMap ?objectMap.
      ?objectMap rr:parentTriplesMap ?parent_tm .
      ?objectMap rr:joinCondition ?join_condition .
      ?join_condition ?conditions ?condition_values .
   }
   WHERE {
      ?triplesmap  rr:subjectMap ?subjectMap.
      ?subjectMap rr:class <""" + child + """>.

      ?triplesmap rr:predicateObjectMap ?pom.
      ?pom rr:predicate <""" + objprop + """> . #if comes from the ontology, it's going to be always constant

      ?pom rr:objectMap ?objectMap.
      ?objectMap rr:parentTriplesMap ?parent_tm .
      ?objectMap rr:joinCondition ?join_condition .
      ?join_condition ?conditions ?condition_values .
   }
   """
        output_mappings.update(q5)

        # Remove ObjectProperties where %OBJECTPROPERTY% has as range %SUBCLASS%.
        # For each OBJECTPROPERTY:
        q6 = """
           PREFIX rr: <http://www.w3.org/ns/r2rml#>
           PREFIX rml: <http://semweb.mmlab.be/ns/rml#>

            DELETE {
               ?parent_triplesMap rr:predicateObjectMap <%OBJECTPROPERTY%>.
               ?parent_pom rr:objectMap ?parent_object.
               ?parent_object rr:parentTriplesMap ?triplesmap.
               ?parent_object rr:joinConditions ?parent_joinConditions .
               ?parent_joinConditions ?parent_conditions ?parent_conditions_values . 
            }
            WHERE {   
               ?parent_triplesMap rr:predicateObjectMap <%OBJECTPROPERTY%>.
               ?parent_pom rr:objectMap ?parent_object.
               ?parent_object rr:parentTriplesMap ?triplesmap.
               OPTIONAL {
                  ?parent_object rr:joinConditions ?parent_joinConditions .
                  ?parent_joinConditions ?parent_conditions ?parent_conditions_values .
               } 
            }
         """
        output_mappings.update(q6)


# ---------------------------------------------------------------------------------------------------------------
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
            f' <{change}> {OCH_ADD_OBJECT_PROPERTY_PROPERTY} ?property .'\
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
                                       f'             {R2RML_JOIN_CONITION} [ ' \
                                       f'               {R2RML_CHILD} "XXXX"; {R2RML_PARENT} "XXXX" ' \
                                       f'          ] ] ]. }}' \
                                       f'  WHERE {{' \
                                       f'     ?triplesMap {R2RML_SUBJECT} ?subjectMap . ' \
                                       f'     ?subjectMap {R2RML_CLASS} <{property_domain}> .' \
                                       f'     ?parent_triplesMap {R2RML_SUBJECT} ?parent_subjectMap . ' \
                                       f'     ?parent_subjectMap {R2RML_CLASS} {property_range} }}'

        output_mappings.update(insert_object_property_query)


# --------------------------------------------------------------------------------------------------------------------------------------------------
def RemoveObjectProperty(change):
    q = """
    SELECT DISTINCT ?domain ?property 
    WHERE {
        <""" + change + """> omv:domainRemoveObjectProperty ?domain.
        <""" + change + """> omv:propertyRemoveObjectProperty ?property.
    }
    """
    for r in change_data.query(q):
        domain = r["domain"]
        predicate = r["property"]
    # Removes %OBJECTPROPERTY% from %CLASS%. Extended version is also provided
    q1 = """
       PREFIX rr: <http://www.w3.org/ns/r2rml#>
      PREFIX rml: <http://semweb.mmlab.be/ns/rml#>

   DELETE { 
      ?triplesmap rr:predicateObjectMap ?pom.
      ?pom rr:predicate <""" + predicate + """> . #if comes from the ontology, it's going to be always constant

      ?pom rr:objectMap ?objectMap.
      ?objectMap rr:parentTriplesMap ?parent_tm .
      ?objectMap rr:joinCondition ?join_condition .
      ?join_condition ?conditions ?condition_values .
   }
   WHERE {
      ?triplesmap  rr:subjectMap ?subjectMap.
      ?subjectMap rr:class <""" + domain + """>.

      ?triplesmap rr:predicateObjectMap ?pom.
      ?pom rr:predicate <""" + predicate + """> . #if comes from the ontology, it's going to be always constant

      ?pom rr:objectMap ?objectMap.
      ?objectMap rr:parentTriplesMap ?parent_tm .
      ?objectMap rr:joinCondition ?join_condition .
      ?join_condition ?conditions ?condition_values .
         
   }
   """
    output_mappings.update(q1)


# -------------------------------------------------------------------------------------------------------------------------
def AddDataProperty(change):
    # Adds %DATA_PROPERTY% to %CLASS% with datatype %RANGE_DATA_PROPERTY% extracted from the range of %DATA_PROPERTY%. By defaylt, reference is used for the data.
    q = """
    SELECT DISTINCT ?domain ?property 
    WHERE {
        <""" + change + """> omv:domainAddDataProperty ?domain.
        <""" + change + """> omv:propertyAddDataProperty ?property.
    }
    """
    for r in change_data.query(q):
        domain = r["domain"]
        predicate = r["property"]
        q2 = """
   SELECT DISTINCT ?range
    WHERE {
        <""" + predicate + """> rdfs:range ?range.
    }
   """
        range = ""
        for r in ontology.query(q2):
            range = r["range"]
        if range != "":
            q1 = """
            PREFIX rr: <http://www.w3.org/ns/r2rml#>
            PREFIX rml: <http://semweb.mmlab.be/ns/rml#>

            INSERT { 
               ?triplesmap rr:predicateObjectMap [
                  rr:predicate <""" + predicate + """>;
                  rr:objectMap [
                     rml:reference "XXXX";
                     rr:datatype <""" + range + """>
                  ]
               ].
            }
            WHERE {
               ?triplesmap rr:subjectMap ?subjectMap .
               ?subjectMap rr:class <""" + domain + """> .
            }
            """
        if range == "":
            q1 = """
            PREFIX rr: <http://www.w3.org/ns/r2rml#>
            PREFIX rml: <http://semweb.mmlab.be/ns/rml#>

            INSERT { 
               ?triplesmap rr:predicateObjectMap [
                  rr:predicate <""" + predicate + """>;
                  rr:objectMap [
                     rml:reference "XXXX";
                  ]
               ].
            }
            WHERE {
               ?triplesmap rr:subjectMap ?subjectMap .
               ?subjectMap rr:class <""" + domain + """> .
            }
            """
        output_mappings.update(q1)


# -----------------------------------------------------------------------------------------------------------------------------------
def RemoveDataProperty(change):
    q = """
    SELECT DISTINCT ?domain ?property
    WHERE {
        <""" + change + """> omv:domainRemoveDataProperty ?domain.
        <""" + change + """> omv:propertyRemoveDataProperty ?property.
    }
    """
    for r in change_data.query(q):
        domain = r["domain"]
        predicate = r["property"]
    # Removes %DATAPROPERTY% from %CLASS%. Extended version is also provided
    q1 = """
   PREFIX rr: <http://www.w3.org/ns/r2rml#>
   PREFIX rml: <http://semweb.mmlab.be/ns/rml#>
   
   DELETE { 
      ?triplesmap rr:predicateObjectMap ?pom.
      ?pom rr:predicate <""" + predicate + """> . #if comes from the ontology, it's going to be always constant
      
      ?pom ?object_property ?objectMap. #either rr:objectMap or rr:object
      ?objectMap ?object_term ?objectValue . #removes everything under objectMap (including language, datatype or termType)
   }
   WHERE {
      ?triplesmap  rr:subjectMap ?subjectMap.
      ?subjectMap rr:class <""" + domain + """>.

      ?triplesmap rr:predicateObjectMap ?pom.
         ?pom rr:predicate <""" + predicate + """> . #if comes from the ontology, it's going to be always constant

      ?pom rr:objectMap|rr:object ?objectMap.
      OPTIONAL { ?objectMap ?object_term ?objectValue }.
         
   }
   """
    output_mappings.update(q1)


# -------------------------------------------------------------------------------------------------------------


def define_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--changes_kg_path", required=False, help="Change KG following the Change Ontology")
    parser.add_argument("-m", "--old_mapping_path", required=False, help="Old version of the mappings in RML")
    parser.add_argument("-o", "--ontology_path", required=False, help="New version of the ontology")
    parser.add_argument("-n", "--new_mappings_path", required=False, help="Output path for the generated mapping")
    return parser


if __name__ == "__main__":
    args = define_args().parse_args()
    # Change data that follows the OWL change ontology specification.
    change_data = Graph().parse(args.changes_kg_path, format="turtle")
    # Outdated mappings to be updated.
    output_mappings = Graph().parse(args.old_mapping_path, format="turtle")
    # The current ontology to check for info
    ontology = Graph().parse(args.ontology_path)
    # We create an additional graph for introducing those elements from the mappings that require reviewing.
    review_mappings = Graph()
    # We query the data to find all the changes
    q = """
    SELECT DISTINCT ?change ?type
    WHERE {
        ?change rdf:type ?type .
    }
    """
    # Execute query and iterate through the changes to modify accordingly to the change.
    for r in change_data.query(q):
        if r.type == URIRef("http://omv.ontoware.org/2009/09/OWLChanges#AddClass"):
            add_class(r["change"])
        elif r["type"] == URIRef("http://omv.ontoware.org/2009/09/OWLChanges#RemoveClass"):
            remove_class(r["change"])
        elif r["type"] == URIRef("http://omv.ontoware.org/2009/09/OWLChanges#AddSubClass"):
            add_super_class(r["change"])
        elif r["type"] == URIRef("http://omv.ontoware.org/2009/09/OWLChanges#RemoveSubClass"):
            RemoveSubClass(r["change"])
        elif r["type"] == URIRef("http://omv.ontoware.org/2009/09/OWLChanges#AddObjectProperty"):
            add_object_property(r["change"])
        elif r["type"] == URIRef("http://omv.ontoware.org/2009/09/OWLChanges#RemoveObjectProperty"):
            RemoveObjectProperty(r["change"])
        elif r["type"] == URIRef("http://omv.ontoware.org/2009/09/OWLChanges#AddDataProperty"):
            AddDataProperty(r["change"])
        elif r["type"] == URIRef("http://omv.ontoware.org/2009/09/OWLChanges#RemoveDataProperty"):
            RemoveDataProperty(r["change"])
    output_mappings.serialize(destination=args.new_mappings_path)
    yarrrml_content = yatter.inverse_translation(output_mappings)
    with open(args.new_mappings_path.replace(".ttl", ".yml"), "wb") as f:
        yaml = YAML()
        yaml.default_flow_style = False
        yaml.width = 3000
        yaml.dump(yarrrml_content, f)
