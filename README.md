# OntoRipple: A Tool to Propagate Changes to Semantic Artifacts.
![GitHub]![GitHub](https://img.shields.io/github/license/oeg-upm/ontoripple?style=flat)
[![DOI](https://zenodo.org/badge/690501188.svg)](https://zenodo.org/doi/10.5281/zenodo.11244236)
![GitHub Release](https://img.shields.io/github/v/release/oeg-upm/ontoripple)


OntoRipple is a tool for propagating ontology changes to declarative mappings in [RML](https://kg-construct.github.io/rml-resources/portal/), and validation shapes in [SHACL](https://www.w3.org/TR/shacl/).  The tool requires as input the updated version of the ontology in OWL, the outdated mappings in RML if there are, the outdated shapes in SHACL if there are, and the change data, that has to be in RDF, and compliant with the [OWL Change Ontology](https://w3id.org/def/och) model.  

# How to run it?

```bash
python3 -m pip install ontoripple
python3 -m ontoripple -c path_to_change_kg.nt -m path_to_old_mapping.rml.ttl -s path_to_old_shapes -o path_to_new_ontology.ttl -nm path_output_mappings.rml.ttl -nsh path_output_shapes.sh
```

Options:
````
-c, --changes_kg_path <arg>        Path to a change KG compliant with OCH
-m, --old_mapping_path <arg>       Path to the old mapping rules (previous version) in RML
-s, --old_shacl_path <arg>         Path to the old validation shapes (previous version) in SHACL
-o, --ontology_path <arg>          Path to the new version of the ontology
-nm, --new_mappings_path <arg>     Path to the output files, updated version of the mapping rules
-nsh, --new_shapes_path <arg>      Path to the output files, updated version of the mapping rules
-y, --yarrrml                      Output mappings will be also translated to YARRRML (RML turtle by default)
````

# How to run the examples.
This software tool is motivated by the Public Procurement Data Space, and the eProcurement Ontology. Within the [PPDS folder](examples/ppds/3.0.0-3.0.1_example/) there is the data corresponding to the changes between the 3.0.0 and 3.0.1 versions of the ontology: the change data, the outdated and updated mappings, and the outdated and updated shapes. The code for generating the updated mappings and shapes is the following:
```bash
python3 -m ontoripple -c ./change_data_3.0.1.nt -m ./ePO_mappings.rml.ttl -s ./ePO_shacl_shapes_3.0.0.rdf -o ./ePO_owl_core_3.0.1.rdf -nm ./updated_mappings.ttl -nsh ./updated_shapes.ttl
```

# Architecture
![OntoRipple Architecture](misc/arqui.jpg?raw=true "OntoRipple Architecture")

# Authors
- Diego Conde Herreros (OEG-UPM) - main contact  diego.conde.herreros at upm.es
- David Chaves-Fraga (CiTIUS-USC)