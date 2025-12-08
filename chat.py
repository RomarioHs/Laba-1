from uuid import uuid1
from message import Message
class Chat:


    def __init__(self, name: str, members: list):
        self.id = str(uuid1())
        self.name = name
        self.members = members
        self.messages = []

    def send_message(self, sender, text, attachment=None):
        msg = Message(sender, text, attachment)
        self.messages.append(msg)
        return msg
