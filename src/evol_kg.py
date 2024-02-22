from rdflib import Graph
#Here we have the list of the different change operations that are called from the main method
def AddClass(change):
   return None

def RemoveClass(change):
   return None

def AddSubClass(change):
   return None

def RemoveSubClass(change):
   return None

def AddObjectProperty(change):
   return None

def RemoveObjectProperty(change):
   return None

def AddDataProperty(change):
   return None

def RemoveDataProperty(change):
   return None


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