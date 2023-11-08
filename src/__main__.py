import re

from bs4 import BeautifulSoup
import re
import csv

#TODO: David, en las cabeceras de las nuevas clases y clases que se borran aparece el módulo al que pertenecen dentro de la ontología, ¿no es de interés representarlo?
def get_classes(html_doc, search_string):
    classes = []
    for h in html_doc.find_all('h2'):
        if re.match(f".*{search_string}.*", h.get('id')):
            for values in h.parent.find_all("li"):
                classes.append(values.find('p').getText().strip())
    return classes

#TODO: En el documento de cambios está la inserción y borrado de los vocabularios controlados, ¿Es de interés para lo nuestro?
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
    properties = []
    for h in html_doc.find_all('h2'):
        if re.match(f".*changed_classes*", h.get('id')):
            for entries in h.parent.find_all("tr"):
                if entries.find_all("td"):
                    clase = entries.find_all("td")[1].find('p').getText().strip()
                    #Ademas hay condicion para que no tome los atributos.
                    #Caso en el que se modifica property
                    if entries.find_all("td")[2].find('p')!=None and entries.find_all("td")[3].find('p')!=None:
                        if "→" in entries.find_all("td")[2].find('p').getText().strip() and "→" in entries.find_all("td")[3].find('p').getText().strip():
                            addatt = entries.find_all("td")[2].find('p').getText().strip()
                            delatt = entries.find_all("td")[3].find('p').getText().strip()
                            properties.append((clase,addatt,delatt))
                    #Caso en el que se crea la property    
                    elif entries.find_all("td")[2].find('p')!=None and entries.find_all("td")[3].find('p')==None:
                        if "→" in entries.find_all("td")[2].find('p').getText().strip():
                            addatt = entries.find_all("td")[2].find('p').getText().strip()
                            properties.append((clase,addatt,""))
                    #Caso en el que se elimina la property    
                    elif entries.find_all("td")[2].find('p')==None and entries.find_all("td")[3].find('p')!=None:
                        if "→" in entries.find_all("td")[3].find('p').getText().strip():
                            delatt = entries.find_all("td")[3].find('p').getText().strip()
                            properties.append((clase,"",delatt))
    #print(properties)
    return properties


def write_csv(classes, name, metadata):
    with open(name, 'w', newline='', encoding="utf-8") as output_file:
        writer = csv.writer(output_file, quoting=csv.QUOTE_ALL)
        writer.writerow(["name", "reference_version", "target_version"])

        for c in classes:
            writer.writerow([c, metadata["Reference ePO version"], metadata["Target ePO version"]])

def write_csv_attributes(attributes, name, metadata):
    with open(name, 'w', newline='', encoding="utf-8") as output_file:
        writer = csv.writer(output_file, quoting=csv.QUOTE_ALL)
        writer.writerow(["class","added_attributes","deleted_attributes","reference_version", "target_version"])
        for c in attributes:
            writer.writerow([c[0],c[1],c[2], metadata["Reference ePO version"], metadata["Target ePO version"]])

def write_csv_properties(attributes, name, metadata):
    with open(name, 'w', newline='', encoding="utf-8") as output_file:
        writer = csv.writer(output_file, quoting=csv.QUOTE_ALL)
        writer.writerow(["class","added_properties","deleted_properties","reference_version", "target_version"])
        for c in attributes:
            writer.writerow([c[0],c[1],c[2], metadata["Reference ePO version"], metadata["Target ePO version"]])

#TODO: David, de los metadatos que estamos obteniendo realmente solo le damos uso a la versión origen y la de destino pero, ¿no son de interés los autores y fecha?
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
    property_changes = get_properties(html_content)
    write_csv(new_classes, "added_clases.csv", metadata_changes)
    write_csv(deleted_classes, "deleted_sclasses.csv", metadata_changes)
    write_csv_attributes(attribute_changes,"modified_attributes.csv",metadata_changes)
    write_csv_properties(property_changes,"modified_properties.csv",metadata_changes)