from rdflib import Graph
#Here we have the list of the different change operations that are called from the main method
# When adding something to the mappings the tool adds suggestions following the notation XXXX, when deleting ontological terms we will
# follow certain assumptions that are indicated in their methos and in the documentation. 
#---------------------------------------------------------------------------------------------------------------------------
def AddClass(change):
    #The query obtains from the change data the name of the class to be added, both the short version for the triplesmap, and the full IRI. 
    q = """
    SELECT ?fullname, ?class
    WHERE {
        ?"""+change+""" omv:addedClass ?class .
        ?"""+change+""" omv:addedClass_full ?fullname .
    }
    """
    name = change_data.query(q)["class"]
    full_name = name["?fullname"]
    #Second query adds the triples map with a template version of the logical source and the subject maps as it requires user input.
    # ASSUMPTION: 
    q1 = """
      INSERT DATA { 
      
      <"""+full_name+"""> a rr:TriplesMap;
                                          rml:logicalSource 
      [  rml:source "XXXX";
               rml:referenceFormulation "XXXX"];	   
         rr:subjectMap [
         rr:template "XXXX";
         rr:class """+full_name+"""].
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
 #TODO: Si es sublcase, que introduzca los TriplesMap y POM en otro documento para que revise.
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
 #The DELETE query is split in three for clarity sake.   
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
 ##TODO: Revisar query, como ponemos en negrita este término a modo de sugerencia????????? Está esto bien????
 q1 = """"
    INSERT { 
      rr:class """+parent+"""
      }
      WHERE {
         ?triplesmap a rr:TriplesMap; 
         rr:subjectMap [
         rr:template ?template
         rr:class """+child+"""
         ];
      }
"""
 output_mappings.update(q1)
   
#--------------------------------------------------------------------------------------------------------------
def RemoveSubClass(change):
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
    DELETE { 
      rr:class """+parent+"""
      }
      WHERE {
         ?triplesmap a rr:TriplesMap; 
         rr:subjectMap [
         rr:template "XXXX";
         rr:class """+child+""","""+parent+"""
         ];
      }
 """
 output_mappings.update(q1)

#---------------------------------------------------------------------------------------------------------------
def AddObjectProperty(change):
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
 #TODO: Respecto al object hay forma de indicar cual es el tipo del predicado en RML sin crear un subject map nuevo.
 object = queryres["?range"]
 q1 = """"
    INSERT { 
   rr:predicateObjectMap [
      rr:predicate """+predicate+""";
      rr:objectMap [
         rr:template "XXXX"
      ]
   ]
   }
      WHERE {
         ?triplesmap a rr:TriplesMap; 
         rr:subjectMap [
         rr:template ?template
         rr:class """+domain+"""
         ];
      }
"""
 output_mappings.update(q1)
#-------------------------------------------------------------------------------------------------------------
#TODO Mismo problema que en el add.
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
 object = queryres["?range"]
 q1 = """"
   DELETE { 
   rr:predicateObjectMap [
      rr:predicate """+predicate+""";
      rr:objectMap [
         rr:template ?template
      ]
   ]
   }
      WHERE {
         ?triplesmap a rr:TriplesMap; 
         rr:subjectMap [
         rr:template ?template
         rr:class """+domain+"""
         ];
      }
"""
 output_mappings.update(q1)
#----------------------------------------------------------------------------------------------------------
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
   rr:predicateObjectMap [
      rr:predicate """+predicate+""";
      rr:objectMap [
         rr:reference "XXXX"
      ]
   ]
   }
      WHERE {
         ?triplesmap a rr:TriplesMap; 
         rr:subjectMap [
         rr:template ?template
         rr:class """+domain+"""
         ];
      }
"""
 output_mappings.update(q1)
#-------------------------------------------------------------------------------------------------------
def RemoveDataProperty(change):
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
   rr:predicateObjectMap [
      rr:predicate """+predicate+""";
      rr:objectMap [
         rr:reference ?reference
      ]
   ]
   }
      WHERE {
         ?triplesmap a rr:TriplesMap; 
         rr:subjectMap [
         rr:template ?template
         rr:class """+domain+"""
         ];
      }
"""
 output_mappings.update(q1)
#-------------------------------------------------------------------------------------------------------------


#Here we have the main method in the code
if __name__ == "__main__":
    #Fist we Open the data from the change data
    file_data = "../mappings/change_data.nt"
    change_data = Graph().parse(file_data)
    #Then we have the route of the mappings to update. 
    file_mapping = "../mappings/mappings.rml"
    #We create a graph which is to be the updated mappings.
    output_mappings = Graph.parse(file_mapping)
    #We have the current ontology to check for info
    ontology = Graph.parse("../mappings/input_onto.owl")
    #We create an additional rdf file for introducing those elements from the mappings that require reviewing. 
    review_mappings = Graph()
    # We query the data to find all the changes
    q = """
    SELECT ?change, ?type
    WHERE {
        ?change rdf:type ?type .
    }
    """
    #Execute query and iterate through the changes to modify accordingly to the change.
    for r in change_data.query(q):
     if r["type"] == "omv:AddClass":
        AddClass(r["change"]) 
     elif r["type"] == "omv:RemoveClass":
        RemoveClass(r["change"])
     elif r["type"] == "omv:AddSubClass":
        AddSubClass(r["change"])
     elif r["type"] == "omv:RemoveSubClass":
        RemoveSubClass(r["change"])
     elif r["type"] == "omv:AddObjectProperty":
        AddObjectProperty(r["change"])
     elif r["type"] == "omv:RemoveObjectProperty":
        RemoveObjectProperty(r["change"])
     elif r["type"] == "omv:AddDataProperty":
        AddDataProperty(r["change"])
     elif r["type"] == "omv:RemoveDataProperty":
        RemoveDataProperty(r["change"])
    output_mappings.serialize(destination="updated_mappings.ttl")