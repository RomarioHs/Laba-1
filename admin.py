import json
from datetime import datetime, date
import inspect
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
            json.dump(data, f)

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

                # восстановление дат
                if isinstance(value, str):
                    try:
                        if len(value) >= 10 and value[4] == "-" and value[7] == "-":
                            value = datetime.fromisoformat(value)
                    except:
                        pass

                args[key] = value

            obj = cls(**args)

            # восстанавливаем остальные атрибуты
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

