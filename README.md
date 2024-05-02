# OCP2KG: Ontology Change Propagation to Knowledge Graphs
![GitHub](https://img.shields.io/github/license/oeg-dataintegration/ocp2kg?style=flat)

OCP2KG is a tool for propagating ontology changes to declarative mappings. 
The tool requires as input the updated 
version of the ontology in OWL, the outdated mappings in RML, and the change data, that has to be in 
RDF following the [OWL Change Ontology Extension](https://github.com/DiegoCondeHerreros/OWLChangeExtension) model.  

# How to run it?

```bash
python3 -m pip install -r requirements
python3 evol_kg.py -c path_to_change_kg.nt -m path_to_old_mapping.rml.ttl -o path_to_new_ontology.ttl -n path_output_mappings.rml.ttl
```

Options:
````
-c, --changes_kg_path <arg>        Path to a change KG compliant with OCH
-m, --old_mapping_path <arg>       Path to the old mapping rules (previous version) in RML
-o, --ontology_path <arg>          Path to the new version of the ontology
-n, --new_mappings_path <arg>      Path to the output files, updated version of the mapping rules
````

# Architecture
![OCP2KG Architecture](figures/arqui.jpg?raw=true "OCP2KG Architecture")

## Cite this work:
If you used OCP2KG in your work, please cite it as:

```bib
@inproceedings{herreros2024propagating,
    title={{Propagating Ontology Changes to Declarative Mappings in Construction of Knowledge Graphs}},
    author={Diego Conde Herreros and Lise Stork and Romana Pernisch and Mar{\'\i}a Poveda-Villal{\'o}n and Oscar Corcho and David Chaves-Fraga},
    booktitle={Fifth International Workshop on Knowledge Graph Construction@ESWC2024},
    year={2024},
    url={https://openreview.net/forum?id=ONL4LGlHNu}
}
```

# Authors
- Diego Conde Herreros (OEG-UPM) - diego.conde.herreros at upm.es
- David Chaves-Fraga (CiTIUS-USC) - david.chaves at usc.es