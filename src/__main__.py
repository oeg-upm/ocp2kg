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
                    clase = entries.find_all("td")[1].find('p').getText().strip()
                    #Ademas hay condicion para que no tome las properties.
                    #Caso en el que se modifica atributo
                    if entries.find_all("td")[2].find('p')!=None and entries.find_all("td")[3].find('p')!=None:
                        if "→" not in entries.find_all("td")[2].find('p').getText() and "→" not in entries.find_all("td")[3].find('p').getText():
                            addatt = entries.find_all("td")[2].find('p').getText().strip()
                            delatt = entries.find_all("td")[3].find('p').getText().strip()
                            attributes.append((clase,addatt,delatt))
                    #Caso en el que se crea el atributo    
                    elif entries.find_all("td")[2].find('p')!=None and entries.find_all("td")[3].find('p')==None:
                        if "→" not in entries.find_all("td")[2].find('p').getText():
                            addatt = entries.find_all("td")[2].find('p').getText().strip()
                            attributes.append((clase,addatt,""))
                    #Caso en el que se elimina el atributo    
                    elif entries.find_all("td")[2].find('p')==None and entries.find_all("td")[3].find('p')!=None:
                        if "→" not in entries.find_all("td")[3].find('p').getText():
                            delatt = entries.find_all("td")[3].find('p').getText().strip()
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
                    clase = entries.find_all("td")[1].find('p').getText().strip()
                    #Ademas hay condicion para que no tome los atributos.
                    #Caso en el que se modifica property
                    if entries.find_all("td")[2].find('p')!=None and entries.find_all("td")[3].find('p')!=None:
                        if "→" in entries.find_all("td")[2].find('p').getText().strip() and "→" in entries.find_all("td")[3].find('p').getText().strip():
                            if "generalisation" in entries.find_all("td")[2].find('p').getText().strip():                               
                                addtriple = entries.find_all("td")[2].find('p').getText().strip()
                                deltriple = entries.find_all("td")[3].find('p').getText().strip()
                                words_add = addtriple.split(" ")
                                words_del = deltriple.split(" ")
                                added_subclass.append((clase,"rdfs:subClassOf",words_add[2]))
                                deleted_subclass.append((clase, "rdfs:subClassOf",words_del[2]))                            
                            else:
                                addtriple = entries.find_all("td")[2].find('p').getText().strip()
                                deltriple = entries.find_all("td")[3].find('p').getText().strip()
                                words_add = addtriple.split(" ")
                                words_del = deltriple.split(" ")
                                added_triples.append((clase,words_add[0],words_add[2]))
                                deleted_triples.append((clase, words_del[0],words_del[2]))                                             
                    #Caso en el que se crea la property    
                    elif entries.find_all("td")[2].find('p')!=None and entries.find_all("td")[3].find('p')==None:
                        if "→" in entries.find_all("td")[2].find('p').getText().strip():
                            if "generalisation" in entries.find_all("td")[2].find('p').getText().strip():                               
                                addtriple = entries.find_all("td")[2].find('p').getText().strip()
                                words_add = addtriple.split(" ")
                                added_subclass.append((clase,"rdfs:subClassOf",words_add[2]))
                            else:
                                addtriple = entries.find_all("td")[2].find('p').getText().strip()
                                words_add = addtriple.split(" ")
                                added_triples.append((clase,words_add[0],words_add[2]))
                    #Caso en el que se elimina la property    
                    elif entries.find_all("td")[2].find('p')==None and entries.find_all("td")[3].find('p')!=None:
                        if "→" in entries.find_all("td")[3].find('p').getText().strip():
                            if "generalisation" in entries.find_all("td")[3].find('p').getText().strip():                               
                                    deltriple = entries.find_all("td")[3].find('p').getText().strip()
                                    words_del = deltriple.split(" ")
                                    deleted_subclass.append((clase, "rdfs:subClassOf",words_del[2]))                            
                            else:
                                    deltriple = entries.find_all("td")[3].find('p').getText().strip()
                                    words_del = deltriple.split(" ")
                                    deleted_triples.append((clase, words_del[0],words_del[2]))      
    #print(properties)
    return added_triples, deleted_triples, added_subclass, deleted_subclass


def write_csv(classes, name, metadata):
    with open(name, 'w', newline='', encoding="utf-8") as output_file:
        writer = csv.writer(output_file, quoting=csv.QUOTE_ALL)
        writer.writerow(["name","comment","reference_version","target_version"])

        for c in classes:
            writer.writerow([c.split(" ")[0]," ".join(c.split(" ")[1:]),metadata["Reference ePO version"], metadata["Target ePO version"]])

def write_csv_attributes(attributes, name, metadata):
    with open(name, 'w', newline='', encoding="utf-8") as output_file:
        writer = csv.writer(output_file, quoting=csv.QUOTE_ALL)
        writer.writerow(["class","comment","added_attributes","deleted_attributes","reference_version", "target_version"])
        for c in attributes:
            writer.writerow([c[0].split(" ")[0]," ".join(c[0].split(" ")[1:]),c[1],c[2], metadata["Reference ePO version"], metadata["Target ePO version"]])

def write_csv_properties(triples, name, metadata):
    with open(name, 'w', newline='', encoding="utf-8") as output_file:
        writer = csv.writer(output_file, quoting=csv.QUOTE_ALL)
        writer.writerow(["subject","comment","predicate","object","reference_version", "target_version"])
        for c in triples:
            writer.writerow([c[0].split(" ")[0]," ".join(c[0].split(" ")[1:]),c[1],c[2], metadata["Reference ePO version"], metadata["Target ePO version"]])

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


if __name__ == "__main__":
    with open("../epo-data/changes_v4.0.0.html",encoding="utf-8") as input_file:
        content = input_file.read()
    html_content = BeautifulSoup(content, "html.parser")
    new_classes = get_classes(html_content, "new_classes")
    deleted_classes = get_classes(html_content, "deleted_classes")
    metadata_changes = get_metadata(html_content)
    attribute_changes = get_attributes(html_content)
    added_triples,deleted_triples,added_subclass,deleted_subclass = get_properties(html_content)
    write_csv(new_classes, "added_classes.csv", metadata_changes)
    write_csv(deleted_classes, "deleted_classes.csv", metadata_changes)
    write_csv_attributes(attribute_changes,"modified_attributes.csv",metadata_changes)
    write_csv_properties(added_triples,"added_triples.csv",metadata_changes)
    write_csv_properties(deleted_triples,"deleted_triples.csv",metadata_changes)
    write_csv_properties(deleted_subclass,"deleted_subclass.csv",metadata_changes)
    write_csv_properties(added_subclass,"added_subclass.csv",metadata_changes)