import os
from lxml import etree


def aggregate_xml_data(directory, output_file):
    """
    Take a directory full containing xml files and parse them into a single file
    
    Return the filename of the new xml file that contains the new xml tree from the combined elements
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
                xml_file_path = os.path.join(current_dir, file)
                root = etree.parse(xml_file_path).getroot()
                data_element.append(root)
    
    if len(data_element) < 1:
        raise Exception("Couldn't build the xml tree.\nThere are no xml files in the input folder or sub folders")
    
    return new_tree