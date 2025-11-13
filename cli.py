from contact_book import ContactBook
from contact import Contact 
import re
from typing import Tuple



class ContactCLI:
    def __init__(self, data_file: str):
        self.book = ContactBook(data_file)

    def run(self):
        self.book.load()
        while True:
            print("\n===============================") 
            print(f"Contact Book ({self.book.data_file})") 
            print("===============================") 
            print("1. Add Contact") 
            print("2. View All Contacts") 
            print("3. Search Contact by Name") 
            print("4. Edit Contact") 
            print("5. Delete Contact") 
            print("6. Save and Exit")
            choice = input("Choose an option (1-6): ").strip()

            if choice == "1":
                self._add_contact()
            elif choice == "6":
                print("Saving contacts to file...")
                self.book.save()
                print("Data saved. Goodbye!")
                break
            else:
                print("Feature not implemented yet (coming next).")
                
    def check_field(self, field_type: str, value: str) -> Tuple[bool, str]:
        """
        Check if a field (name, phone, or email) is correctly formatted or unique.
        Returns (True, cleaned_value) if valid, otherwise (False, error_message).
        """
        if field_type == "name":
            name_pattern = r"^[A-Za-zÀ-ÖØ-öø-ÿ'-]+\s[A-Za-zÀ-ÖØ-öø-ÿ'-]+$"
            if not value:
                return False, "Error: Name cannot be empty. Example: John Doe"
            if not re.match(name_pattern, value):
                return (False,
                        "Error: Enter a valid full name (first and last, letters only). "
                        "Examples: John Doe, Jean-Luc Picard, O'Connor Smith")
            if any(c.name.lower() == value.lower() for c in self.book._contacts):
                return False, f'Error: Contact "{value}" already exists. Please enter a different name.'
            return True, value

        elif field_type == "phone":
            phone_pattern = r"^[+]?[\d\s\-()]{7,20}$"
            if not value:
                return (False,
                        "Error: Phone number is required. Examples: +123456789, (555) 123-4567, 123 456 7890")
            if not re.match(phone_pattern, value):
                return (False,
                        "Error: Invalid phone number format. Examples: +123456789, (555) 123-4567, 123 456 7890")
            normalized_input = re.sub(r"[^\d+]", "", value)
            if any(re.sub(r"[^\d+]", "", c.phone) == normalized_input for c in self.book._contacts):
                return False, f'Error: Phone number "{value}" is already used by another contact.'
            return True, value

        elif field_type == "email":
            email_pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
            if not value:
                return (False,
                        "Error: Email address is required. Examples: john.doe@email.com, "
                        "alice@company.org, user+test@domain.co.uk")
            if not re.match(email_pattern, value):
                return (False,
                        "Error: Invalid email address format. Examples: john.doe@email.com, "
                        "alice@company.org, user+test@domain.co.uk")
            if any(c.email.lower() == value.lower() for c in self.book._contacts):
                return False, f'Error: Email: "{value}" already exists. Please enter a different Email adress.'
            return True, value

        else:
            return False, "Error: Unknown field type."
        
        

    def _add_contact(self):
        print("\n--- Add New Contact ---")

        # Full name
        while True:
            name_input = input("Enter full name: ").strip()
            valid, message = self.check_field("name", name_input)
            if valid:
                name = message
                break
            print(message)

        # Phone
        while True:
            phone_input = input("Enter phone number: ").strip()
            valid, message = self.check_field("phone", phone_input)
            if valid:
                phone = message
                break
            print(message)

        # Email
        while True:
            email_input = input("Enter email address: ").strip()
            valid, message = self.check_field("email", email_input)
            if valid:
                email = message
                break
            print(message)

        # Add to contact book
        new_contact = Contact(name, phone, email)
        self.book._contacts.append(new_contact)
        self.book.save()
        print(f'Contact "{name}" added successfully!')



