# working with XML files in python
import xml.etree.ElementTree as ET
from xml.dom import minidom
from typing import Optional, List, Dict, Any
from pathlib import Path

def write_xml(filename: str, root_tag: str, data: Dict[str, Any]) -> bool:
    """write dictionary data to XML file."""
    try:
        root = ET.Element(root_tag)
        
        def _dict_to_xml(parent: ET.Element, data: Any):
            if isinstance(data, dict):
                for key, value in data.items():
                    child = ET.SubElement(parent, key)
                    _dict_to_xml(child, value)
            elif isinstance(data, list):
                for item in data:
                    child = ET.SubElement(parent, "item")
                    _dict_to_xml(child, item)
            else:
                parent.text = str(data)
        
        _dict_to_xml(root, data)
        
        # pretty print XML
        xml_str = minidom.parseString(ET.tostring(root)).toprettyxml(indent="  ")
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(xml_str)
        return True
    except Exception as e:
        print(f"error writing XML: {e}")
        return False

def read_xml(filename: str) -> Optional[Dict[str, Any]]:
    """read XML file into dictionary."""
    try:
        tree = ET.parse(filename)
        root = tree.getroot()
        
        def _xml_to_dict(element: ET.Element) -> Any:
            if len(element) == 0:
                return element.text
            
            result = {}
            list_tags = set()
            
            for child in element:
                child_data = _xml_to_dict(child)
                
                if child.tag in result:
                    if child.tag not in list_tags:
                        result[child.tag] = [result[child.tag]]
                        list_tags.add(child.tag)
                    result[child.tag].append(child_data)
                else:
                    result[child.tag] = child_data
            
            return result
        
        return {root.tag: _xml_to_dict(root)}
    except Exception as e:
        print(f"error reading XML: {e}")
        return None

def validate_xml_schema(xml_file: str, schema_file: str) -> bool:
    """validate XML file against XSD schema."""
    try:
        from lxml import etree
        
        schema_doc = etree.parse(schema_file)
        schema = etree.XMLSchema(schema_doc)
        
        xml_doc = etree.parse(xml_file)
        return schema.validate(xml_doc)
    except Exception as e:
        print(f"validation error: {e}")
        return False

def search_xml(filename: str, tag: str) -> List[str]:
    """search for all elements with specific tag."""
    try:
        tree = ET.parse(filename)
        root = tree.getroot()
        return [elem.text for elem in root.findall(f".//{tag}") if elem.text]
    except Exception as e:
        print(f"error searching XML: {e}")
        return []

def modify_xml(filename: str, xpath: str, new_value: str) -> bool:
    """modify XML element using XPath."""
    try:
        tree = ET.parse(filename)
        root = tree.getroot()
        
        for elem in root.findall(xpath):
            elem.text = new_value
        
        tree.write(filename, encoding='utf-8', xml_declaration=True)
        return True
    except Exception as e:
        print(f"error modifying XML: {e}")
        return False

def create_xml_with_attributes(filename: str, data: Dict[str, Any]) -> bool:
    """create XML with attributes and elements."""
    try:
        root = ET.Element("root")
        
        def _add_element(parent: ET.Element, key: str, value: Any):
            if isinstance(value, dict):
                elem = ET.SubElement(parent, key)
                attrs = value.get('_attributes', {})
                for attr_key, attr_value in attrs.items():
                    elem.set(attr_key, str(attr_value))
                
                for k, v in value.items():
                    if not k.startswith('_'):
                        _add_element(elem, k, v)
            elif isinstance(value, list):
                for item in value:
                    _add_element(parent, key, item)
            else:
                elem = ET.SubElement(parent, key)
                elem.text = str(value)
        
        for key, value in data.items():
            _add_element(root, key, value)
        
        # pretty print XML
        xml_str = minidom.parseString(ET.tostring(root)).toprettyxml(indent="  ")
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(xml_str)
        return True
    except Exception as e:
        print(f"error creating XML: {e}")
        return False

# example usage
def main():
    """demonstrate XML file operations."""
    # sample data
    data = {
        "person": {
            "name": "John Doe",
            "age": 30,
            "address": {
                "street": "123 Main St",
                "city": "New York",
                "country": "USA"
            },
            "hobbies": [
                "reading",
                "hiking",
                "photography"
            ]
        }
    }
    
    # write XML file
    filename = "person.xml"
    print("writing XML file...")
    write_xml(filename, "root", data)
    
    # read XML file
    print("\nreading XML file:")
    loaded_data = read_xml(filename)
    print(f"loaded data: {loaded_data}")
    
    # search XML
    print("\nsearching for 'city':")
    cities = search_xml(filename, "city")
    print(f"found cities: {cities}")
    
    # modify XML
    print("\nmodifying XML...")
    modify_xml(filename, ".//age", "31")
    
    # XML with attributes
    attr_data = {
        "person": {
            "_attributes": {
                "id": "123",
                "type": "employee"
            },
            "name": "Jane Doe",
            "department": {
                "_attributes": {
                    "code": "IT01"
                },
                "name": "Information Technology"
            }
        }
    }
    
    attr_filename = "person_with_attrs.xml"
    print("\ncreating XML with attributes...")
    create_xml_with_attributes(attr_filename, attr_data)
    
    # cleanup
    for file in [filename, attr_filename]:
        Path(file).unlink()

if __name__ == "__main__":
    main()

# practice exercises:
# 1. create a program that:
#    - reads an XML configuration file
#    - validates against XSD schema
#    - applies transformations using XSLT
#    - generates formatted output

# 2. create a program that:
#    - implements an XML-based data storage
#    - supports CRUD operations
#    - handles namespaces
#    - maintains data integrity

# 3. create a program that:
#    - converts between XML and other formats
#    - preserves data structure
#    - handles complex nested elements
#    - supports custom data types 