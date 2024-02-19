import re

from bs4 import BeautifulSoup
import re
import csv

def get_classes(html_doc, search_string):
    classes = []
    for h in html_doc.find_all('h2'):
        if re.match(f".*{search_string}.*", h.get('id')):
            for values in h.parent.find_all("li"):
                classes.append(values.find('p').getText().strip())
    return classes

def get_attributes(html_doc):
    attributes = []
    for h in html_doc.find_all('h2'):
        if re.match(f".*changed_classes*", h.get('id')):
            for entries in h.parent.find_all("tr"):
                if entries.find_all("td"):
                    clase = entries.find_all("td")[0].find('p').getText().strip()
                    #Ademas hay condicion para que no tome las properties.
                    #Caso en el que se modifica atributo
                    if entries.find_all("td")[1].find('p')!=None and entries.find_all("td")[2].find('p')!=None:
                        if "→" not in entries.find_all("td")[1].find('p').getText() and "→" not in entries.find_all("td")[2].find('p').getText():
                            addatt = entries.find_all("td")[1].find('p').getText().strip()
                            delatt = entries.find_all("td")[2].find('p').getText().strip()
                            attributes.append((clase,addatt,delatt))
                    #Caso en el que se crea el atributo    
                    elif entries.find_all("td")[1].find('p')!=None and entries.find_all("td")[2].find('p')==None:
                        if "→" not in entries.find_all("td")[1].find('p').getText():
                            addatt = entries.find_all("td")[1].find('p').getText().strip()
                            attributes.append((clase,addatt,""))
                    #Caso en el que se elimina el atributo    
                    elif entries.find_all("td")[1].find('p')==None and entries.find_all("td")[2].find('p')!=None:
                        if "→" not in entries.find_all("td")[2].find('p').getText():
                            delatt = entries.find_all("td")[2].find('p').getText().strip()
                            attributes.append((clase,"",delatt))
    return attributes

#Espera de recibir feedback de David de como quiere que lo representemos.
def get_properties(html_doc):
    added_triples = []
    deleted_triples = []
    added_subclass = []
    deleted_subclass = []
    for h in html_doc.find_all('h2'):
        if re.match(f".*changed_classes*", h.get('id')):
            for entries in h.parent.find_all("tr"):
                if entries.find_all("td"):
                    clase = entries.find_all("td")[0].find('p').getText().strip()
                    #Ademas hay condicion para que no tome los atributos.
                    #Caso en el que se modifica property
                    if entries.find_all("td")[1].find('p')!=None and entries.find_all("td")[2].find('p')!=None:
                        if "→" in entries.find_all("td")[1].find('p').getText().strip() and "→" in entries.find_all("td")[2].find('p').getText().strip():
                            if "generalisation" in entries.find_all("td")[1].find('p').getText().strip():                               
                                addtriple = entries.find_all("td")[1].find('p').getText().strip()
                                deltriple = entries.find_all("td")[2].find('p').getText().strip()
                                words_add = addtriple.split(" ")
                                words_del = deltriple.split(" ")
                                added_subclass.append((clase,"rdfs:subClassOf",words_add[2]))
                                deleted_subclass.append((clase, "rdfs:subClassOf",words_del[2]))                            
                            else:
                                addtriple = entries.find_all("td")[1].find('p').getText().strip()
                                deltriple = entries.find_all("td")[2].find('p').getText().strip()
                                words_add = addtriple.split(" ")
                                words_del = deltriple.split(" ")
                                added_triples.append((clase,words_add[0],words_add[2]))
                                deleted_triples.append((clase, words_del[0],words_del[2]))                                             
                    #Caso en el que se crea la property    
                    elif entries.find_all("td")[1].find('p')!=None and entries.find_all("td")[2].find('p')==None:
                        if "→" in entries.find_all("td")[1].find('p').getText().strip():
                            if "generalisation" in entries.find_all("td")[1].find('p').getText().strip():                               
                                addtriple = entries.find_all("td")[1].find('p').getText().strip()
                                words_add = addtriple.split(" ")
                                added_subclass.append((clase,"rdfs:subClassOf",words_add[2]))
                            else:
                                addtriple = entries.find_all("td")[1].find('p').getText().strip()
                                words_add = addtriple.split(" ")
                                added_triples.append((clase,words_add[0],words_add[2]))
                    #Caso en el que se elimina la property    
                    elif entries.find_all("td")[1].find('p')==None and entries.find_all("td")[2].find('p')!=None:
                        if "→" in entries.find_all("td")[2].find('p').getText().strip():
                            if "generalisation" in entries.find_all("td")[2].find('p').getText().strip():                               
                                    deltriple = entries.find_all("td")[2].find('p').getText().strip()
                                    words_del = deltriple.split(" ")
                                    deleted_subclass.append((clase, "rdfs:subClassOf",words_del[2]))                            
                            else:
                                    deltriple = entries.find_all("td")[2].find('p').getText().strip()
                                    words_del = deltriple.split(" ")
                                    deleted_triples.append((clase, words_del[0],words_del[2]))      
    #print(properties)
    return added_triples, deleted_triples, added_subclass, deleted_subclass


def write_csv(classes, name, metadata):
    with open(name, 'w', newline='', encoding="utf-8") as output_file:
        writer = csv.writer(output_file, quoting=csv.QUOTE_ALL)
        writer.writerow(["name","comment","reference_version","target_version"])
        for c in classes:
            clase= parse_full_URI(c.split(" ")[0])
            comment = c[len(c.split(" ")[0])+2:-1]
            writer.writerow([clase,comment,metadata["Reference ePO version"], metadata["Target ePO version"]])

def write_csv_attributes(attributes, name, metadata):
    with open(name, 'w', newline='', encoding="utf-8") as output_file:
        writer = csv.writer(output_file, quoting=csv.QUOTE_ALL)
        writer.writerow(["class","comment","added_attributes","commentaddatt","deleted_attributes","commentdelatt","reference_version", "target_version"])
        for c in attributes:
            clase= parse_full_URI(c[0].split(" ")[0])
            comment = c[0][len(c[0].split(" ")[0])+2:-1]
            added_attribute = parse_full_URI(c[1].split(" ")[0])
            commentaux1 = c[1][len(c[1].split(" ")[0])+2:-1]
            deleted_atrribute = parse_full_URI(c[2].split(" ")[0])
            commentaux2 = c[2][len(c[2].split(" ")[0])+2:-1]
            writer.writerow([clase,comment,added_attribute,commentaux1,deleted_atrribute,commentaux2, metadata["Reference ePO version"], metadata["Target ePO version"]])

def write_csv_properties(triples, name, metadata):
    with open(name, 'w', newline='', encoding="utf-8") as output_file:
        writer = csv.writer(output_file, quoting=csv.QUOTE_ALL)
        writer.writerow(["subject","comment","predicate","commentpred","object","commentobj","reference_version", "target_version"])
        for c in triples:
            clase= parse_full_URI(c[0].split(" ")[0])
            comment = c[0][len(c[0].split(" ")[0])+2:-1]
            predicate = parse_full_URI(c[1].split(" ")[0])
            commentaux1 = c[1][len(c[1].split(" ")[0])+2:-1]
            object = parse_full_URI(c[2].split(" ")[0])
            commentaux2 = c[2][len(c[2].split(" ")[0])+2:-1]
            writer.writerow([clase,comment,predicate,commentaux1,object,commentaux2, metadata["Reference ePO version"], metadata["Target ePO version"]])

def get_metadata(html_doc):
    metadata = {}
    for h in html_doc.find_all('h2'):
        if re.match(".*release_notes.*", h.get('id')):
            for entries in h.parent.find_all("tr"):
                if entries.find_all("td"):
                    key = entries.find_all("td")[0].find('p').getText().strip()
                    value = entries.find_all("td")[1].find('p').getText().strip()
                    metadata[key] = value

    return metadata

def parse_full_URI(term):    
    if term.startswith("epo-cat"):
        return "http://data.europa.eu/a4g/ontology#"+term.split(":")[1]
    elif term.startswith("epo-con"):
        return "http://data.europa.eu/a4g/ontology#"+term.split(":")[1]
    elif term.startswith("epo-ord"):
        return "http://data.europa.eu/a4g/ontology#"+term.split(":")[1]
    elif term.startswith("epo-not"):
        return "http://data.europa.eu/a4g/ontology#"+term.split(":")[1]
    elif term.startswith("epo-ful"):
        return "http://data.europa.eu/a4g/ontology#"+term.split(":")[1]
    elif term.startswith("epo-acc"):
        return "http://data.europa.eu/a4g/ontology#"+term.split(":")[1]
    elif term.startswith("epo-sub"):
        return "http://data.europa.eu/a4g/ontology#"+term.split(":")[1]
    elif term.startswith("epo"):
        return "http://data.europa.eu/a4g/ontology#"+term.split(":")[1]
    elif term.startswith("adms"):
        return "http://www.w3.org/ns/adms#"+term.split(":")[1]
    elif term.startswith("at-voc-new"):
        return "http://publications.europa.eu/resource/authority/new/"+term.split(":")[1]
    elif term.startswith("at-voc"):
        return "http://publications.europa.eu/resource/authority/"+term.split(":")[1]
    elif term.startswith("bibo"):
        return "http://purl.org/ontology/bibo/"+term.split(":")[1]
    elif term.startswith("cc"):
        return "http://creativecommons.org/ns#"+term.split(":")[1]
    elif term.startswith("cccev"):
        return "http://data.europa.eu/m8g/"+term.split(":")[1]
    elif term.startswith("dct"):
        return "http://purl.org/dc/terms/"+term.split(":")[1]
    elif term.startswith("foaf"):
        return "http://xmlns.com/foaf/0.1/"+term.split(":")[1]
    elif term.startswith("locn"):
        return "http://www.w3.org/ns/locn#"+term.split(":")[1]
    elif term.startswith("org"):
        return "http://www.w3.org/ns/org#"+term.split(":")[1]
    elif term.startswith("owl"):
        return "http://www.w3.org/2002/07/owl#"+term.split(":")[1]
    elif term.startswith("person"):
        return "http://www.w3.org/ns/person#"+term.split(":")[1]
    elif term.startswith("rdf"):
        return "http://www.w3.org/1999/02/22-rdf-syntax-ns#"+term.split(":")[1]
    elif term.startswith("rdfs"):
        return "http://www.w3.org/2000/01/rdf-schema#"+term.split(":")[1]
    elif term.startswith("skos"):
        return "http://www.w3.org/2004/02/skos/core#"+term.split(":")[1]
    elif term.startswith("time"):
        return "http://www.w3.org/2006/time#"+term.split(":")[1]
    elif term.startswith("vann"):
        return "http://purl.org/vocab/vann/"+term.split(":")[1]
    elif term.startswith("xsd"):
        return "http://www.w3.org/2001/XMLSchema#"+term.split(":")[1]
    elif term.startswith("cv"):
        return "http://data.europa.eu/m8g/"+term.split(":")[1]
    elif term.startswith("cv"):
        return "http://data.europa.eu/m8g/"+term.split(":")[1]
    elif term.startswith("cpv"):
        return "http://data.europa.eu/m8g/"+term.split(":")[1]
    elif term.startswith("cpv"):
        return "http://data.europa.eu/m8g/"+term.split(":")[1]

if __name__ == "__main__":
    with open("../epo-data/changes_v3.1.0.html",encoding="utf-8") as input_file:
        content = input_file.read()
    html_content = BeautifulSoup(content, "html.parser")
    new_classes = get_classes(html_content, "new_classes")
    deleted_classes = get_classes(html_content, "deleted_classes")
    metadata_changes = get_metadata(html_content)
    write_csv(new_classes, "added_classes3.1.csv", metadata_changes)
    write_csv(deleted_classes, "deleted_classes3.1.csv", metadata_changes)
    attribute_changes = get_attributes(html_content)
    write_csv_attributes(attribute_changes,"modified_attributes3.1.csv",metadata_changes)
    added_triples,deleted_triples,added_subclass,deleted_subclass = get_properties(html_content)
    write_csv_properties(added_triples,"added_triples3.1.csv",metadata_changes)
    write_csv_properties(deleted_triples,"deleted_triples3.1.csv",metadata_changes)
    write_csv_properties(deleted_subclass,"deleted_subclass3.1.csv",metadata_changes)
    write_csv_properties(added_subclass,"added_subclass3.1.csv",metadata_changes)