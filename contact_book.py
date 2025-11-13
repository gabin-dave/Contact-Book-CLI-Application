import json
import os
from typing import List
from contact import Contact

class ContactBook:
    def __init__(self, data_file: str):
        self.data_file = data_file
        self._contacts: List[Contact] = []

    def load(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, "r") as f:
                raw = json.load(f)
            self._contacts = [Contact.from_dict(item) for item in raw]
        else:
            self._contacts = []

    def save(self):
        with open(self.data_file, "w") as f:
            json.dump([c.to_dict() for c in self._contacts], f, indent=4)

    def add_contact(self, name: str, phone: str, email: str) -> bool:
        if any(c.name.lower() == name.lower() for c in self._contacts):
            return False
        self._contacts.append(Contact(name, phone, email))
        return True
    
    def get_all_contacts(self) -> List[Contact]:
        return sorted(self._contacts, key=lambda c: c.name.lower())