# OCP2KG: Ontology Change Propagation to Knowledge Graphs
OCP2KG is a tool for propagating ontology changes to declarative mappings. The tool requires as input the updated 
version of the ontology in OWL, the outdated mappings in RML, and the change data. The change data has to be in 
RDF following the [OWL Change Ontology Extension](https://github.com/DiegoCondeHerreros/OWLChangeExtension) model.  
The "updated_mappings.ttl" output is generated in the src folder with the updated mappings for the newer version 
of the ontology. More details regarding the implementation and evaluation of the tool ca be seen in
"Propagating Ontology Changes to Declarative Mappings in Construction of Knowledge Graphs". 

# How to run it?

```bash
python3 -m pip install -r requirements
python3 -c evol_kg.py path_to_change_kg.nt -m path_to_old_mapping.rml.ttl -o path_to_new_ontology.ttl -n path_output_mappings.rml.ttl
```

# Architecture
![OCP2KG Architecture](figures/arqui.jpg?raw=true "OCP2KG Architecture")

# Issues

# Contact
For any doubts regarding usage of the tool please contact us via email to diego.conde.herreros@upm.es


# Authors
- Diego Conde Herreros (OEG-UPM)
- David Chaves-Fraga (CiTIUS-USC)