import json
from datetime import datetime, date
import inspect
import xml.etree.ElementTree as ET
from xml.dom import minidom
from user import User
from message import Message
from chat import Chat
from attachment import Attachment
from Contacts import ContactList

class Admin:

    def __init__(self, json_path, xml_path):
        self.json_path = json_path
        self.xml_path = xml_path
        self.data = []




        self.class_map = {
            "User": User,
            "Message": Message,
            "Chat": Chat,
            "Attachment": Attachment,
            "ContactList": ContactList
        }


    def add(self, obj):
        print(f"[ADD] {obj.__class__.__name__}")
        self.data.append(obj)

    def update(self, obj, **kwargs):
        try:
            obj.update(**kwargs)
            self.save_json()
            self.save_xml()
            return True
        except AttributeError:
            return False

    def save_json(self):
        print("saving to json")

        def encode(obj):
            if hasattr(obj, "__dict__"):
                result_dict = {}
                for attribute_name, attribute_value in obj.__dict__.items():
                    converted_value = encode(attribute_value)
                    result_dict[attribute_name] = converted_value
                return result_dict

            elif isinstance(obj, list):
                result_list = []
                for item in obj:
                    converted_item = encode(item)
                    result_list.append(converted_item)
                return result_list

            elif isinstance(obj, (datetime, date)):
                iso_string = obj.isoformat()
                return iso_string

            else:
                return obj

        data = []
        for obj in self.data:
            class_name = obj.__class__.__name__
            encoded_object = encode(obj)
            item = {class_name: encoded_object}
            data.append(item)

        with open(self.json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    def load_json(self):
        print("[LOAD] JSON")
        result = []

        with open(self.json_path, "r", encoding="utf-8") as f:
            raw = json.load(f)

        def decode(cls, data):
            sig = inspect.signature(cls.__init__)
            args = {}

            for key, value in data.items():

                if key not in sig.parameters:
                    continue

                if isinstance(value, str):
                    try:
                        if len(value) >= 10 and value[4] == "-" and value[7] == "-":
                            value = datetime.fromisoformat(value)
                    except:
                        pass

                args[key] = value

            obj = cls(**args)

            for k, v in data.items():
                setattr(obj, k, v)

            return obj

        for item in raw:
            class_name = next(iter(item))
            data = item[class_name]

            if class_name in self.class_map:
                cls = self.class_map[class_name]
                obj = decode(cls, data)
                result.append(obj)

        return result

    def save_xml(self):
        print("[SAVE] XML")
        root = ET.Element("root")

        def build_xml(parent, obj):
            for key, value in obj.__dict__.items():

                if isinstance(value, (datetime, date)):
                    ET.SubElement(parent, key).text = value.isoformat()

                elif hasattr(value, "__dict__"):
                    elem = ET.SubElement(parent, key, attrib={"type": value.__class__.__name__})
                    build_xml(elem, value)

                elif isinstance(value, list):
                    arr = ET.SubElement(parent, key)
                    for item in value:
                        if hasattr(item, "__dict__"):
                            elem = ET.SubElement(arr, "item", attrib={"type": item.__class__.__name__})
                            build_xml(elem, item)
                        else:
                            ET.SubElement(arr, "item").text = str(item)

                else:
                    ET.SubElement(parent, key).text = str(value)

        for obj in self.data:
            elem = ET.SubElement(root, obj.__class__.__name__)
            build_xml(elem, obj)

        rough_string = ET.tostring(root, "utf-8")
        reparsed = minidom.parseString(rough_string)
        root = reparsed.toprettyxml(indent="    ")

        with open(self.xml_path, "w", encoding="utf-8") as f:
            f.write(root)


    def load_xml(self):
        print("LOAD XML")
        tree = ET.parse(self.xml_path)
        root = tree.getroot()
        result = []

        def parse_obj(elem):
            class_name = elem.tag
            cls = self.class_map.get(class_name)
            if not cls:
                return None

            kwargs = {}
            extra = {}

            for child in elem:
                if list(child):
                    arr = []
                    for item in child:
                        if "type" in item.attrib:
                            arr.append(parse_obj(item))
                        else:
                            arr.append(item.text)
                    extra[child.tag] = arr


                elif "type" in child.attrib:
                    extra[child.tag] = parse_obj(child)


                else:
                    text = child.text
                    # даты
                    try:
                        text = datetime.fromisoformat(text)
                    except:
                        pass

                    kwargs[child.tag] = text

            obj = cls(**{k: v for k, v in kwargs.items()
                         if k in inspect.signature(cls.__init__).parameters})

            for k, v in extra.items():
                setattr(obj, k, v)

            return obj

        for elem in root:
            obj = parse_obj(elem)
            if obj:
                result.append(obj)

        return result

