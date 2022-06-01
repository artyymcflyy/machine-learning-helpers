import os
from lxml import etree

# TODO: break this out to be more generic
CONTENT_LABEL_MAPPING = {
    "Leaf": "0",
    "Flower": "1",
    "Entire": "2",
    "Other": "4"
}

def aggregate_xml_data(directory, output_file):
    """
    Take a directory full containing xml files and parse them into a single file
    
    Return the filename of the new xml file that contains the new xml tree from the combined elements

    output_file will be added to the input directory
    """
    output = os.path.join(directory, output_file)
    is_file = os.path.isfile(output)

    if is_file:
        # remove file if it exists so data isn't duplicated
        os.remove(output)
    
    new_xml_tree = build_xml_tree(directory)
    new_xml_tree.write(output, pretty_print=True, xml_declaration=True)

    return output

def build_xml_tree(directory):
    """
    Build a single xml tree from any xml files within the directory or sub directories

    Return a new xml tree
    """
    data_element = etree.Element("Data")
    new_tree = etree.ElementTree(data_element)

    for current_dir, _, files in os.walk(directory):
        for file in files:
            if ".xml" in file:
                try:
                    xml_file_path = os.path.join(current_dir, file)
                    root = etree.parse(xml_file_path).getroot()
                    # TODO: break this out to be more generic
                    new_label_text = root.find("Content").text
                    new_label_tag = etree.Element("Content-mapping")
                    new_label_tag.text = CONTENT_LABEL_MAPPING.get(new_label_text, "4")
                    root.append(new_label_tag)
                    data_element.append(root)
                except etree.XMLSyntaxError:
                    pass
    
    if len(data_element) < 1:
        raise Exception("Couldn't build the xml tree.\nThere are no xml files in the input folder or sub folders")
    
    return new_tree