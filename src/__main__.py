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


# def get_new_attributes():


# def get_modified_classes():

def write_csv(classes, name, metadata):
    with open(name, 'w', newline='') as output_file:
        writer = csv.writer(output_file, quoting=csv.QUOTE_ALL)
        writer.writerow(["name", "reference_version", "target_version"])

        for c in classes:
            writer.writerow([c, metadata["Reference ePO version"], metadata["Target ePO version"]])


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
    with open("../epo-data/changes_v3.0.0.html") as input_file:
        content = input_file.read()
    html_content = BeautifulSoup(content, "html.parser")
    new_classes = get_classes(html_content, "new_classes")
    deleted_classes = get_classes(html_content, "deleted_classes")
    metadata_changes = get_metadata(html_content)
    write_csv(new_classes, "added_classes.csv", metadata_changes)
    write_csv(deleted_classes, "deleted_classes.csv", metadata_changes)
