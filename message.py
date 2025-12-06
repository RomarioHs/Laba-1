from uuid import uuid1
from user import User
from datetime import datetime
class Message:


    def __init__(self, sender: User, text: str, attachment=None):
        self.id = str(uuid1())
        self.sender = sender
        self.text = text
        self.attachment = attachment
        self.timestamp = datetime.now()

    def info(self):
        return f"[{self.timestamp}] {self.sender.username}: {self.text}"