from rdflib import Graph
#Here we have the list of the different change operations that are called from the main method
#---------------------------------------------------------------------------------------------------------------------------
def AddClass(change):
    q = """
    SELECT ?fullname, ?class
    WHERE {
        ?"""+change+""" omv:addedClass ?class .
        ?"""+change+""" omv:addedClass_full ?fullname .
    }
    """
    name = change_data.query(q)["class"]
    full_name = name["?fullname"]
    q1 = """
    INSERT DATA { 
    
    <"""+name+"""> a rr:TriplesMap;
    	rml:logicalSource [
		rml:source "XXXX";
		rml:referenceFormulation "XXXX"
	    ];
        
        rr:subjectMap [
        rr:template "XXXX";
        rr:class """+full_name+"""
        ];
    }
    """
    output_mappings.update(q1)
#---------------------------------------------------------------------------------------------------------------------------    
def RemoveClass(change):
 q = """
    SELECT  ?fullname
    WHERE {
        ?"""+change+""" omv:deletedClass ?fullname .
    }
    """
 full_name = change_data.query(q)["?fullname"]
 ##TODO: Revisa esta query.
 q1 = """
    DELETE DATA { 
    
    ?triplesmap a rr:TriplesMap;
    	rml:logicalSource [
		rml:source ?source;
		rml:referenceFormulation ?formulation
	    ];
      rr:subjectMap [
      rr:template ?templete;
      rr:class """+full_name+"""
      ];
      rr:predicateObjectMap [
         ?y ?z
      ];

      ....
      rr:predicateObjectMap [
         ?w ?o
      ];

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