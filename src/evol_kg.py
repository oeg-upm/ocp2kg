from rdflib import Graph, URIRef, Variable
import sys
import yatter
from constants import *
from ruamel.yaml import YAML

# ---------------------------------------------------------------------------------------------------------------------------

def AddClass(change):
    """
    Adds a class defined in the change to the output_mappings
    Args:
        change: the URI of the change which needs to be of the type AddClass
    Returns:
        the output_mappings updated with a new class
    """
    select_change = f' SELECT DISTINCT ?class WHERE {{' \
                    f'<{change}> omv:addedClass ?class .}} '

    results = change_data.query(select_change)
    added_class = results.bindings[0][Variable('class')]

    insert_class_query = f' INSERT DATA {{' \
                         f'{added_class} a {R2RML_TRIPLES_MAP}; ' \
                         f'{RML_LOGICAL_SOURCE} [ ' \
                         f'   {RML_SOURCE} "XXXX"; ' \
                         f'   {RML_REFERENCE_FORMULATION} "XXXX" ' \
                         f'];	    ' \
                         f'{R2RML_SUBJECT} [ ' \
                         f'   {R2RML_TEMPLATE} "XXXX"; ' \
                         f'   {R2RML_CLASS} <{added_class}> ' \
                         f']. }} '
    output_mappings.update(insert_class_query)


# ---------------------------------------------------------------------------------------------------------------------------
def RemoveClass(change):
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

def AddSubClass(change):
    q = """
    SELECT DISTINCT ?parent ?child
    WHERE {
        <""" + change + """> omv:subAddSubClass ?child.
        <""" + change + """> omv:objAddSubClass ?parent.
    }
    """
    for r in change_data.query(q):
        child = r["child"]
        parent = r["parent"]
        # Adds %SUPERCLASS% to the %SUBCLASS%. This change triggers the second and third query, which add DATAPROPERTY and OBJECTPROPERTY where the domain is SUPERCLASS.
        q1 = """
   PREFIX rr: <http://www.w3.org/ns/r2rml#>

   INSERT {  
      ?subjectMap rr:class <""" + parent + """>.
   }
   WHERE {
      ?triplesmap rr:subjectMap ?subjectMap.
      ?subjectMap rr:class <""" + child + """>.
   }
   """
        output_mappings.update(q1)
        q2 = """
   SELECT DISTINCT ?dataproperty ?range
   WHERE {
      ?dataproperty  a owl:DatatypeProperty;
                     rdfs:domain <""" + parent + """>;
                     rdfs:range ?range.
   } 
   """
    for r in ontology.query(q2):
        dataprop = r["dataproperty"]
        range = r["range"]
        # Adds %DATAPROPERTIES% where their domain are %SUPERCLASS%. This runs after the first query.
        # Needs to be run for each DATAPROPERTY of %SUBCLASS%
        q3 = """
   INSERT {  
    ?triplesmap rr:predicateObjectMap [
        rr:predicate <""" + dataprop + """>;
        rr:objectMap [
            rml:reference "XXXX";
            rr:datatype <""" + range + """>
        ]
    ].
   }
   WHERE {
      ?triplesmap rr:subjectMap ?subjectMap .
      ?subjectMap rr:class <""" + child + """>, <""" + parent + """> .
   }
   """
        output_mappings.update(q3)
    q4 = """
      SELECT DISTINCT ?objectproperty ?range
      WHERE {
         ?objectproperty  a owl:ObjectProperty;
                        rdfs:domain <""" + parent + """>;
                        rdfs:range ?range.
      }    
      """
    for r in ontology.query(q4):
        objprop = r["objectproperty"]
        range = r["range"]
        # Adds %OBJECTPROPERTY% where their domain are %SUPERCLASS% and the RANGE is %RANGECLASS%. This runs after the first query.
        # Needs to be run for each OBJECTPROPERTY of %SUPERCLASS%
        q5 = """
      INSERT {  
         ?triplesmap rr:predicateObjectMap [
            rr:predicate <""" + objprop + """>;
            rr:objectMap [
                  rr:parentTriplesMap ?parent_tm;
                  rr:joinCondition [
                     rr:child "XXXX";
                     rr:parent "XXXX"
                  ]
            ]
         ].
      }
      WHERE {
         ?triplesmap rr:subjectMap ?subjectMap .
         ?subjectMap rr:class <""" + child + """>, <""" + parent + """> .

         ?parent_tm rr:subjectMap ?parent_subjectMap .
         ?parent_subjectMap rr:class <""" + range + """> .
      }
      """
        output_mappings.update(q5)


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
def AddObjectProperty(change):
    # Adds %OBJECT_PROPERTY% to %CLASS%. The ?parent_tm are the TriplesMap(s) which create instances of the class %RANGE_CLASS% which is the range of %OBJECT_PROPERTY%.
    q = """
    SELECT DISTINCT ?domain ?property ?range
    WHERE {
        <""" + change + """> omv:domainAddObjectProperty ?domain.
        <""" + change + """> omv:propertyAddObjectProperty ?property.
        <""" + change + """> omv:rangeAddObjectProperty ?range.

    }
    """
    for r in change_data.query(q):
        domain = r["domain"]
        predicate = r["property"]
        range = r["range"]
    q1 = """
   INSERT { 
      ?triplesmap rr:predicateObjectMap [
         rr:predicate <""" + predicate + """>;
         rr:objectMap [
            rr:parentTriplesMap ?parent_tm;
            rr:joinCondition [
               rr:child "XXXX";
               rr:parent "XXXX"
            ]
         ]
      ].
   }
   WHERE {
      ?triplesmap rr:subjectMap ?subjectMap .
      ?subjectMap rr:class <""" + domain + """> .

      ?parent_tm rr:subjectMap ?parent_subjectMap .
      ?parent_subjectMap rr:class <""" + range + """> .     
   }
   """
    output_mappings.update(q1)


# --------------------------------------------------------------------------------------------------------------------------------------------------
def RemoveObjectProperty(change):
    q = """
    SELECT DISTINCT ?domain ?property ?range
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
    SELECT DISTINCT ?domain ?property ?range
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
        for r in ontology.query(q2):
            range = r["range"]
        q1 = """
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
        output_mappings.update(q1)


# -----------------------------------------------------------------------------------------------------------------------------------
def RemoveDataProperty(change):
    q = """
    SELECT DISTINCT ?domain ?property ?range
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


if __name__ == "__main__":
    # Change data that follows the OWL change ontology specification.
    change_data = Graph().parse(sys.argv[1], format="turtle")
    # Outdated mappings to be updated.
    output_mappings = Graph().parse(sys.argv[2], format="turtle")
    # The current ontology to check for info
    ontology = Graph().parse(sys.argv[3])
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
            print("AddClass")
            AddClass(r["change"])
        elif r["type"] == URIRef("http://omv.ontoware.org/2009/09/OWLChanges#RemoveClass"):
            print("RemoveClass")
            RemoveClass(r["change"])
        elif r["type"] == URIRef("http://omv.ontoware.org/2009/09/OWLChanges#AddSubClass"):
            print("AddSubClass")
            AddSubClass(r["change"])
        elif r["type"] == URIRef("http://omv.ontoware.org/2009/09/OWLChanges#RemoveSubClass"):
            print("RemoveSubClass")
            RemoveSubClass(r["change"])
        elif r["type"] == URIRef("http://omv.ontoware.org/2009/09/OWLChanges#AddObjectProperty"):
            print("AddObjectProperty")
            AddObjectProperty(r["change"])
        elif r["type"] == URIRef("http://omv.ontoware.org/2009/09/OWLChanges#RemoveObjectProperty"):
            print("RemoveObjectProperty")
            RemoveObjectProperty(r["change"])
        elif r["type"] == URIRef("http://omv.ontoware.org/2009/09/OWLChanges#AddDataProperty"):
            print("AddDataProperty")
            AddDataProperty(r["change"])
        elif r["type"] == URIRef("http://omv.ontoware.org/2009/09/OWLChanges#RemoveDataProperty"):
            print("RemoveDataProperty")
            RemoveDataProperty(r["change"])
    output_mappings.serialize(destination="updated_mappings.ttl")
    yarrrml_content = yatter.inverse_translation(output_mappings)
    with open("updated_mappings.yaml", "wb") as f:
        yaml = YAML()
        yaml.default_flow_style = False
        yaml.dump(yarrrml_content, f)
