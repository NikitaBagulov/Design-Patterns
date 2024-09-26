from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom.minidom import parseString
from src.core.abstract_report import abstract_report
from src.core.format_reporting import format_reporting
from src.utils.validator import Validator

class xml_report(abstract_report):
    
    def __init__(self) -> None:
        super().__init__()
        self.__format = format_reporting.XML

    def create(self, data: list):
        Validator.validate_type(data, list, "data")
        
        root = Element('Report')
        
        for row in data:
            row_element = SubElement(root, 'Row')
            self.serialize_object(row, row_element)
        
        xml_string = tostring(root, encoding="unicode")
        pretty_xml = parseString(xml_string).toprettyxml(indent="  ")
        self.result = pretty_xml

    def serialize_object(self, obj, xml_element):
        fields = list(filter(lambda x: not x.startswith("_") and not callable(getattr(obj.__class__, x)), dir(obj)))
        for field in fields:
            value = getattr(obj, field)
            if isinstance(value, list):
                for item in value:
                    item_element = SubElement(xml_element, field)
                    self.serialize_object(item, item_element)
            elif hasattr(value, '__dict__'):
                nested_element = SubElement(xml_element, field)
                self.serialize_object(value, nested_element)
            else:
                field_element = SubElement(xml_element, field)
                field_element.text = str(value)
