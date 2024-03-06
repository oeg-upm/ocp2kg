from rdflib import Graph, Literal, RDF, URIRef
#Here we have the list of the different change operations that are called from the main method
# When adding something to the mappings the tool adds suggestions following the notation XXXX, when deleting ontological terms we will
# follow certain assumptions that are indicated in their methos and in the documentation. 
#---------------------------------------------------------------------------------------------------------------------------
def AddClass(change):
    #The query obtains from the change data the name of the class to be added, both the short version for the triplesmap, and the full IRI. 
    q = """
    SELECT ?fullname ?class
    WHERE {
        <"""+change+"""> omv:addedClass ?class .
        <"""+change+"""> omv:addedClass_full ?fullname .
    }
    """
    for r in change_data.query(q):
      name = r["class"]
      full_name = r["fullname"]
    #Second query adds the triples map with a template version of the logical source and the subject maps as it requires user input.
    # ASSUMPTION: 
    q1 = """
      INSERT DATA { 
      
      <"""+name+"""> a rr:TriplesMap;
                                          rml:logicalSource 
      [  rml:source "XXXX";
               rml:referenceFormulation "XXXX"];	   
         rr:subjectMap [
         rr:template "XXXX";
         rr:class <"""+full_name+""">].
      }
      """
    output_mappings.update(q1)
#---------------------------------------------------------------------------------------------------------------------------    
def RemoveClass(change):
 #First we query the change data to obtain the class to be deleted. 
 q = """
    SELECT  ?fullname
    WHERE {
        ?"""+change+""" omv:deletedClass ?fullname .
    }
    """
 full_name = change_data.query(q)["?fullname"]
 ##CHECK wether this class is a subclass from another one for different treatments.
 q = """
   ASK { """+full_name+""" rdfs:subClassOf ?x}
 """
 answer=ontology.query(q)
 #CASE 1:  If C is not subclass remove all TriplesMap that instanciate entities of the class C and the POM where the parentTriplesMap in the RefObjectMap is the 4
 #identifier of those TriplesMaps.
 #The following query Removes the TriplesMap from that class, POMs that contain it as a rr:template, and those that contain it as a join condition.
 #The deleted triples are added to a file so that the user can correct any incorrect asumptions
 #The assumption is that the appearances of the term are deleted in all classes, they could be replaced by superclass and that's why is added to review file.
 if (answer==True): 
   qaux = """
   CONSTRUCT { 
      ?triplesmap a rr:TriplesMap.
      ?triplesmap ?prop ?bnodesubject.
      ?triplesmap ?prop1 ?obj.
      ?obj ?prop2 ?obj1.
      ?bnodesubject rr:class <"""+full_name+""">.
      #PART OF THE QUERY To DELETE POM WHEN ITS CONTAINED IN TEMPLATE
      ?triplesmap rr:subjectMap ?bnodesub.
      ?bnodesub rr:template ?urisub.
      ?anothertriplesmap rr:predicateObjectMap ?pombnode.
      ?pombnode rr:objectMap ?omnode.
      ?omnode rr:template ?urisub.
      ?pombnode ?pomprop ?pomobj.
      #DELETION OF JOINS
      ?yetanothertriplesmap rr:predicateObjectMap ?pomnode1.
      ?pomnode1 rr:objectMap ?obnode1.
      ?obnode1 rr:parentTriplesMap ?triplesmap.
      ?pomnode1 ?a ?b.
      
   }
      
   WHERE{ 
      ?triplesmap ?prop ?bnodesubject.
      ?triplesmap ?prop1 ?obj.
      ?obj ?prop2 ?obj1.
      ?bnodesubject rr:class <"""+full_name+""">. 
      #PART OF THE QUERY To DELETE POM WHEN ITS CONTAINED IN TEMPLATE
      OPTIONAL{
      ?triplesmap rr:subjectMap ?bnodesub.
      ?bnodesub rr:template ?urisub.
      ?anothertriplesmap rr:predicateObjectMap ?pombnode.
      ?pombnode rr:objectMap ?omnode.
      ?omnode rr:template ?urisub.
      ?pombnode ?pomprop ?pomobj.
      }
      #DELETION OF JOINS
      OPTIONAL{
      ?yetanothertriplesmap rr:predicateObjectMap ?pomnode1.
      ?pomnode1 rr:objectMap ?obnode1.
      ?obnode1 rr:parentTriplesMap ?triplesmap.
      ?pomnode1 ?a ?b.
      }
   }
         """
   triples_to_be_checked = output_mappings.query(qaux)
   for trip in triples_to_be_checked:
      review_mappings.add(trip)
 q1 = """
#Añadir condiciones que busquen y borren aquellos pom que contengan el template,o joins de la property.
DELETE { 
    ?triplesmap a rr:TriplesMap.
	?triplesmap ?prop ?bnodesubject.
    ?triplesmap ?prop1 ?obj.
    ?obj ?prop2 ?obj1.
    ?bnodesubject rr:class <"""+full_name+""">.
    #PART OF THE QUERY To DELETE POM WHEN ITS CONTAINED IN TEMPLATE
    ?triplesmap rr:subjectMap ?bnodesub.
    ?bnodesub rr:template ?urisub.
    ?anothertriplesmap rr:predicateObjectMap ?pombnode.
    ?pombnode rr:objectMap ?omnode.
    ?omnode rr:template ?urisub.
    ?pombnode ?pomprop ?pomobj.
    #DELETION OF JOINS
    ?yetanothertriplesmap rr:predicateObjectMap ?pomnode1.
    ?pomnode1 rr:objectMap ?obnode1.
    ?obnode1 rr:parentTriplesMap ?triplesmap.
    ?pomnode1 ?a ?b.
	
}
    
 WHERE{ 
    ?triplesmap ?prop ?bnodesubject.
    ?triplesmap ?prop1 ?obj.
    ?obj ?prop2 ?obj1.
    ?bnodesubject rr:class <"""+full_name+""">. 
    #PART OF THE QUERY To DELETE POM WHEN ITS CONTAINED IN TEMPLATE
    OPTIONAL{
    ?triplesmap rr:subjectMap ?bnodesub.
    ?bnodesub rr:template ?urisub.
    ?anothertriplesmap rr:predicateObjectMap ?pombnode.
    ?pombnode rr:objectMap ?omnode.
    ?omnode rr:template ?urisub.
    ?pombnode ?pomprop ?pomobj.
    }
    #DELETION OF JOINS
    OPTIONAL{
    ?yetanothertriplesmap rr:predicateObjectMap ?pomnode1.
    ?pomnode1 rr:objectMap ?obnode1.
    ?obnode1 rr:parentTriplesMap ?triplesmap.
    ?pomnode1 ?a ?b.
    }
}
      """
 output_mappings.update(q1)
 
  
#---------------------------------------------------------------------------------------------------------------------------------
 
def AddSubClass(change):
# When a subclass relationship is added (besides having the class added as an AddClass operation) what changes is that it has to be added as the rr:class of the child class SubjectMap
 q = """
    SELECT ?parent, ?child
    WHERE {
        ?"""+change+""" omv:subAddSubClass ?child.
        ?"""+change+""" omv:objAddSubClass ?parent.
    }
    """
 queryres = change_data.query(q)
 parent = queryres["?parent"]   
 child = queryres["?child"]
 q1 = """"
INSERT {  
    ?bnode rr:class <"""+parent+""">.
      }
      WHERE {
         ?triplesmap a rr:TriplesMap; 
         rr:subjectMap ?bnode.
        ?bnode rr:template ?template.
        ?bnode rr:class <"""+child+""">.
      }
"""
 output_mappings.update(q1)
   
#--------------------------------------------------------------------------------------------------------------
def RemoveSubClass(change):
 # When removing the subclass relationship between two classes the child one loses the parent in the rr:class part. 
 q = """
    SELECT ?parent, ?child
    WHERE {
        ?"""+change+""" omv:subRemoveSubClass ?child.
        ?"""+change+""" omv:objRemoveSubClass ?parent.
    }
    """
 queryres = change_data.query(q)
 parent = queryres["?parent"]   
 child = queryres["?child"]
 q1 = """"
   PREFIX rr: <http://www.w3.org/ns/r2rml#>
   DELETE {  
      ?bnode rr:class <"""+parent+""">.
         }
         WHERE {
            ?triplesmap a rr:TriplesMap; 
            rr:subjectMap ?bnode.
         ?bnode rr:template ?template.
         ?bnode rr:class <"""+child+""">.
         }
   """
 output_mappings.update(q1)

#---------------------------------------------------------------------------------------------------------------
def AddObjectProperty(change):
 #When adding a new Object Property with the domain, property and range a new PredicateObjectMap is added to a subject map that has the domain 
 # The property is added as rr:predicate and the template of the POM is left as XXX values so that it can be changed by user. 
 q = """
    SELECT ?domain, ?property, ?range
    WHERE {
        ?"""+change+""" omv:domainAddObjectProperty ?domain.
        ?"""+change+""" omv:propertyAddObjectProperty ?property.
        ?"""+change+""" omv:rangeAddObjectProperty ?range.
    }
    """
 queryres = change_data.query(q)
 domain = queryres["?domain"]   
 predicate = queryres["?predicate"]
 #object = queryres["?range"]
 q1 = """"
INSERT { 
    ?triplesmap rr:predicateObjectMap [
        rr:predicate <"""+predicate+""">;
        rr:objectMap [
        rr:template "XXXX"]].
}
   WHERE {
  		?triplesmap  rr:subjectMap ?subnode.
    	?subnode rr:class <"""+domain+""">.
   }
"""
 output_mappings.update(q1)
#--------------------------------------------------------------------------------------------------------------------------------------------------
#When Removing a new Object Property with the domain, property and range the PredicateObjectMap is removed from the subject map that has the domain. 
def RemoveObjectProperty(change):
 q = """
    SELECT ?domain, ?property, ?range
    WHERE {
        ?"""+change+""" omv:domainRemoveObjectProperty ?domain.
        ?"""+change+""" omv:propertyRemoveObjectProperty ?property.
        ?"""+change+""" omv:rangeRemoveObjectProperty ?range.
    }
    """
 queryres = change_data.query(q)
 domain = queryres["?domain"]   
 predicate = queryres["?predicate"]
# object = queryres["?range"]
 q1 = """"
   DELETE { 
      ?triplesmap rr:predicateObjectMap ?pomnode.
      ?pomnode rr:predicate <"""+predicate+""">;
            rr:objectMap ?onode.
      ?onode rr:template ?template.
   }
      WHERE {
         ?triplesmap rr:predicateObjectMap ?pomnode.
            ?pomnode rr:predicate <"""+predicate+""">;
               rr:objectMap ?onode.
            ?onode rr:template ?template.
         ?triplesmap  rr:subjectMap ?subnode.
         ?subnode rr:class <"""+domain+""">.
      }
   """
 output_mappings.update(q1)
#-------------------------------------------------------------------------------------------------------------------------
 #The same changes as ObjectProperty but with the main difference being the use of rr:reference instead of rr:template on the POM
def AddDataProperty(change):
 q = """
    SELECT ?domain, ?property, ?range
    WHERE {
        ?"""+change+""" omv:domainAddDataProperty ?domain.
        ?"""+change+""" omv:propertyAddDataProperty ?property.
    }
    """
 queryres = change_data.query(q)
 domain = queryres["?domain"]   
 predicate = queryres["?predicate"]
 q1 = """"
   INSERT { 
      ?triplesmap rr:predicateObjectMap [
         rr:predicate <"""+predicate+""">;
         rr:objectMap [
         rr:reference "XXXX"]].
   }
      WHERE {
         ?triplesmap  rr:subjectMap ?subnode.
         ?subnode rr:class <"""+domain+""">.
      }
   """
 output_mappings.update(q1)
#-----------------------------------------------------------------------------------------------------------------------------------
def RemoveDataProperty(change):
  #The same changes as ObjectProperty but with the main difference being the use of rr:reference instead of rr:template on the POM
 q = """
    SELECT ?domain, ?property, ?range
    WHERE {
        ?"""+change+""" omv:domainRemoveDataProperty ?domain.
        ?"""+change+""" omv:propertyRemoveDataProperty ?property.
    }
    """
 queryres = change_data.query(q)
 domain = queryres["?domain"]   
 predicate = queryres["?predicate"]
 q1 = """"
   DELETE { 
      ?triplesmap rr:predicateObjectMap ?pomnode.
      ?pomnode rr:predicate <"""+predicate+""">;
            rr:objectMap ?onode.
      ?onode rr:reference ?reference.
   }
      WHERE {
         ?triplesmap rr:predicateObjectMap ?pomnode.
            ?pomnode rr:predicate <"""+predicate+""">;
               rr:objectMap ?onode.
            ?onode rr:reference ?reference.
         ?triplesmap  rr:subjectMap ?subnode.
         ?subnode rr:class <"""+domain+""">.
      }
   """
 output_mappings.update(q1)
#-------------------------------------------------------------------------------------------------------------


#Here we have the main method in the code
if __name__ == "__main__":
    #Fist we Open the data from the change data
    file_data = "../test_data/test_change_data.ttl"
    change_data = Graph().parse(file_data, format="turtle")
    #Then we have the route of the mappings to update. 
    file_mapping = "../test_data/test_mappings.rml.ttl"
    #We create a graph which is to be the updated mappings.
    output_mappings = Graph().parse(file_mapping,format="turtle")
    #We have the current ontology to check for info
    #ontology = Graph().parse("../test_data/test_ontology.owl")
    #We create an additional rdf file for introducing those elements from the mappings that require reviewing. 
    review_mappings = Graph()
    # We query the data to find all the changes
    q = """
    SELECT ?change ?type
    WHERE {
        ?change rdf:type ?type .
    }
    """
    #Execute query and iterate through the changes to modify accordingly to the change.
    for r in change_data.query(q):
     if r.type == URIRef("http://omv.ontoware.org/2009/09/OWLChanges#AddClass"):
        AddClass(r["change"]) 
     elif r["type"] == URIRef("http://omv.ontoware.org/2009/09/OWLChanges#RemoveClass"):
        RemoveClass(r["change"])
     elif r["type"] == URIRef("http://omv.ontoware.org/2009/09/OWLChanges#AddSubClass"):
        AddSubClass(r["change"])
     elif r["type"] == URIRef("http://omv.ontoware.org/2009/09/OWLChanges#RemoveSubClass"):
        RemoveSubClass(r["change"])
     elif r["type"] == URIRef("http://omv.ontoware.org/2009/09/OWLChanges#AddObjectProperty"):
        AddObjectProperty(r["change"])
     elif r["type"] == URIRef("http://omv.ontoware.org/2009/09/OWLChanges#RemoveObjectProperty"):
        RemoveObjectProperty(r["change"])
     elif r["type"] == URIRef("http://omv.ontoware.org/2009/09/OWLChanges#AddDataProperty"):
        AddDataProperty(r["change"])
     elif r["type"] == URIRef("http://omv.ontoware.org/2009/09/OWLChanges#RemoveDataProperty"):
        RemoveDataProperty(r["change"])
    output_mappings.serialize(destination="updated_mappings.ttl")