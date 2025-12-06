from user import User

class ContactList:

    def __init__(self, owner: User):
        self.owner = owner
        self.contacts = []

    def add(self, contact: User):
        if contact not in self.contacts:
            self.contacts.append(contact)

    def remove(self, contact: User):
        if contact in self.contacts:
            self.contacts.remove(contact)