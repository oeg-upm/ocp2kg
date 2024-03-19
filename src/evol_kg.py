from rdflib import Graph, Literal, RDF, URIRef
import sys
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
        <"""+change+"""> omv:deletedClass ?fullname .
    }
    """
 for r in change_data.query(q):
  full_name = r["fullname"]
 ##CHECK wether this class is a subclass from another one for different treatments.
 q = """
   ASK { <"""+full_name+"""> rdfs:subClassOf ?x}
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
    SELECT ?parent ?child
    WHERE {
        <"""+change+"""> omv:subAddSubClass ?child.
        <"""+change+"""> omv:objAddSubClass ?parent.
    }
    """
 for r in change_data.query(q):
   child = r["child"]
   parent = r["parent"]   
 q1 = """ 
   INSERT {  
    ?bnode rr:class <"""+parent+""">.
    ?triplesmap rr:predicateObjectMap [?s ?p].
	}
      WHERE {
        ?triplesmap a rr:TriplesMap; 
        rr:subjectMap ?bnode.
        ?bnode rr:class <"""+child+""">.
    	#POM 
      ?triplesmapparent a rr:TriplesMap;
    	rr:subjectMap ?bnodesub;
    	rr:predicateObjectMap ?bnodepom.
    	?bnodesub rr:class <"""+parent+""">.
    	?bnodepom ?s ?p. 
      }
   """
 output_mappings.update(q1)
   
#--------------------------------------------------------------------------------------------------------------
def RemoveSubClass(change):
 # When removing the subclass relationship between two classes the child one loses the parent in the rr:class part. 
 q = """
    SELECT ?parent ?child
    WHERE {
        <"""+change+"""> omv:subRemoveSubClass ?child.
        <"""+change+"""> omv:objRemoveSubClass ?parent.
    }
    """
 for r in  change_data.query(q):
   parent = r["parent"]   
   child = r["child"]
 q1 = """
   DELETE {  
    ?bnode rr:class <"""+parent+""">.
    ?triplesmap rr:predicateObjectMap ?bnodenuevo.
    ?bnodepomchild ?s ?p.
	}
      WHERE {
        ?triplesmap a rr:TriplesMap; 
        rr:subjectMap ?bnode.
        ?bnode rr:class <"""+child+""">.
        ?bnodepomchild ?s ?p.
    	#POM 
      ?triplesmapparent a rr:TriplesMap;
    	rr:subjectMap ?bnodesub;
    	rr:predicateObjectMap ?bnodepom.
    	?bnodesub rr:class <"""+parent+""">.
    	?bnodepom ?s ?p. 
      }
   """
 output_mappings.update(q1)

#---------------------------------------------------------------------------------------------------------------
def AddObjectProperty(change):
 #When adding a new Object Property with the domain, property and range a new PredicateObjectMap is added to a subject map that has the domain 
 # The property is added as rr:predicate and the template of the POM is left as XXX values so that it can be changed by user. 
 q = """
    SELECT ?domain ?property ?range
    WHERE {
        <"""+change+"""> omv:domainAddObjectProperty ?domain.
        <"""+change+"""> omv:propertyAddObjectProperty ?property.
         <"""+change+"""> omv:rangeAddObjectProperty ?range.

    }
    """
 for r in change_data.query(q):
   domain = r["domain"]   
   predicate = r["property"]
   range = r["range"]
 q1 = """
INSERT { 
    ?triplesmap rr:predicateObjectMap [
        rr:predicate <"""+predicate+""">;
        rr:objectMap [
        rr:parentTriplesMap ?othertriplesmap;
        rr:joinCondition [
        	rr:child "XXXX";
         rr:parent "XXXX"]]].
}
   WHERE {
  		?triplesmap  rr:subjectMap ?subnode.
    	?subnode rr:class <"""+domain+""">.
    ?othertriplesmap rr:subjectMap ?bnode.
    ?bnode rr:class <"""+range+""">.     
   }
"""
 output_mappings.update(q1)
#--------------------------------------------------------------------------------------------------------------------------------------------------
#When Removing a new Object Property with the domain, property and range the PredicateObjectMap is removed from the subject map that has the domain. 
def RemoveObjectProperty(change):
 q = """
    SELECT ?domain ?property ?range
    WHERE {
        <"""+change+"""> omv:domainRemoveObjectProperty ?domain.
        <"""+change+"""> omv:propertyRemoveObjectProperty ?property.
    }
    """
 for r in change_data.query(q):
   domain = r["domain"]   
   predicate = r["property"]
# object = queryres["?range"]
 q1 = """
   DELETE { 
      ?triplesmap rr:predicateObjectMap ?pomnode.
      ?pomnode rr:predicate <"""+predicate+""">;
            rr:objectMap ?onode.
   }
      WHERE {
         ?triplesmap rr:predicateObjectMap ?pomnode.
            ?pomnode rr:predicate <"""+predicate+""">;
               rr:objectMap ?onode.
         ?triplesmap  rr:subjectMap ?subnode.
         ?subnode rr:class <"""+domain+""">.
      }
   """
 output_mappings.update(q1)
#-------------------------------------------------------------------------------------------------------------------------
 #The same changes as ObjectProperty but with the main difference being the use of rr:reference instead of rr:template on the POM
def AddDataProperty(change):
 q = """
    SELECT ?domain ?property ?range
    WHERE {
        <"""+change+"""> omv:domainAddDataProperty ?domain.
        <"""+change+"""> omv:propertyAddDataProperty ?property.
    }
    """
 for r in change_data.query(q):
   domain = r["domain"]   
   predicate = r["property"]
 q1 = """
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
    SELECT ?domain ?property ?range
    WHERE {
        <"""+change+"""> omv:domainRemoveDataProperty ?domain.
        <"""+change+"""> omv:propertyRemoveDataProperty ?property.
    }
    """
 for r in change_data.query(q):
   domain = r["domain"]   
   predicate = r["property"]
 q1 = """
   DELETE { 
      ?triplesmap rr:predicateObjectMap ?pomnode.
      ?pomnode rr:predicate <"""+predicate+""">;
            rr:objectMap ?onode.
   }
      WHERE {
         ?triplesmap rr:predicateObjectMap ?pomnode.
            ?pomnode rr:predicate <"""+predicate+""">;
               rr:objectMap ?onode.
         ?triplesmap  rr:subjectMap ?subnode.
         ?subnode rr:class <"""+domain+""">.
      }
   """
 output_mappings.update(q1)
#-------------------------------------------------------------------------------------------------------------



if __name__ == "__main__":
    #Change data that follows the OWL change ontology specification.
    change_data = Graph().parse(sys.argv[1], format="turtle")
    #Outdated mappings to be updated. 
    output_mappings = Graph().parse(sys.argv[2],format="turtle")
    #The current ontology to check for info
    ontology = Graph().parse(sys.argv[3])
    #We create an additional graph for introducing those elements from the mappings that require reviewing. 
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