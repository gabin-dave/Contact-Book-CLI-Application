# contact.py
class Contact:
    def __init__(self, name: str, phone: str, email: str):
        self.name = name.strip()
        self.phone = phone.strip()
        self.email = email.strip()

    def to_dict(self):
        return {"name": self.name, "phone": self.phone, "email": self.email}

    @staticmethod
    def from_dict(d):
        return Contact(d.get("name", ""), d.get("phone", ""), d.get("email", ""))
