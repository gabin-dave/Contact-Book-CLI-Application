from contact_book import ContactBook
from contact import Contact 
import re,os,readline
from typing import Tuple,List





class ContactCLI:
    def __init__(self, data_file: str):
        self.book = ContactBook(data_file)
    
    @staticmethod
    def enable_autofilled(options):
        """Enable tab-completion for a list of options (e.g., filenames)."""
        try:
            import readline
        except Exception:
            return

        def completer(text, state):
            matches = [o for o in options if o.startswith(text)]
            return matches[state] if state < len(matches) else None

        readline.set_completer_delims(" \t\n")
        readline.set_completer(completer)
        readline.parse_and_bind("tab: complete")
        
    def run(self):
        self.book.load()
        while True:
            self.clear_screen()
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
                self.clear_screen()
                self._add_contact()
            elif choice == "2":
                self.clear_screen()
                self._view_all_contacts()
                
            elif choice == "3":
                self.clear_screen()
                if not self._ensure_data_available():
                    continue

                print("\n--- Search Contact by Name ---")
                results, search_name = self.search_contact()

                if not results:
                    if search_name:
                        print(f'\nNo contact found with name containing "{search_name}".')
                    input("\nPress Enter")
                    continue
                print(self._format_contacts_for_display(results, f'Search Results for \"{search_name}\"'))
                input("\nPress Enter")
                
            elif choice == "4":
                self.clear_screen()
                self.edit_contact()
                
                
            elif choice == "5":
                self.clear_screen()
                self.delete_contact()
            
            elif choice == "6":
                self.clear_screen()
                print("\nSaving contacts to file...\n")
                self.book.save()
                print("Data saved")
                input("")
                self.clear_screen()
                
                break
            else:
                print("Feature not implemented yet.")
    
    def clear_screen(self):
        ### For Windows or MacOs/Linux###
        os.system('cls' if os.name == 'nt' else 'clear')
                
    def check_field(self, field_type: str, value: str,exclude: Contact = None) -> Tuple[bool, str]:
        
        if field_type == "name":
            name_pattern = r"^[A-Za-zÀ-ÖØ-öø-ÿ'-]+\s[A-Za-zÀ-ÖØ-öø-ÿ'-]+$"
            if not value:
                return False, "Error: Name cannot be empty. Example: John Doe"
            if not re.match(name_pattern, value):
                return (False,
                        "Error: Enter a valid full name (first and last, letters only). "
                        "Examples: John Doe, Jean-Luc Picard, O'Connor Smith")
            if any((c is not exclude) and (c.name.lower() == value.lower()) for c in self.book._contacts):
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
            if any((c is not exclude) and (re.sub(r"[^\d+]", "", c.phone)) == normalized_input for c in self.book._contacts):
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
            if any((c is not exclude) and (c.email.lower() == value.lower()) for c in self.book._contacts):
                return False, f'Error: Email: "{value}" already exists. Please enter a different Email adress.'
            return True, value

        else:
            return False, "Error: Unknown field type."
        
        

    def _add_contact(self):
        print("\n--- Add New Contact ---")

        while True:
            name_input = input("Enter full name: ").strip()
            valid, message = self.check_field("name", name_input)
            if valid:
                name = message.title()
                break
            print(message)

        while True:
            phone_input = input("Enter phone number: ").strip()
            valid, message = self.check_field("phone", phone_input)
            if valid:
                phone = message
                break
            print(message)

        while True:
            email_input = input("Enter email address: ").strip()
            valid, message = self.check_field("email", email_input)
            if valid:
                email = message
                break
            print(message)

        new_contact = Contact(name, phone, email)
        self.book._contacts.append(new_contact)
        self.book.save()
        print(f'Contact "{name}" added successfully!')
        input("\nPress Enter")



    def _format_contacts_for_display(self, contacts: List[Contact],Value) -> str:
        if not contacts:
            return "No contacts found."
        lines = [f"\n\n==== {Value} ===="]
        for i, c in enumerate(contacts, start=1):
            lines.append(f"{i}. {c.name} | {c.phone} | {c.email}")
        lines.append("=======================\n\n")
        lines.append(f"Total: {len(contacts)} contacts")
        return "\n".join(lines)

    
    def _view_all_contacts(self):
        self.clear_screen()
        if not self._ensure_data_available():
            return
        contacts = self.book.get_all_contacts()
        print(self._format_contacts_for_display(contacts,"All Contacts"))
        input("\nPress Enter")
        
        
    def search_contact(self) -> Tuple[List[Contact],str]:
        if not self._ensure_data_available():
            return [], ""

        names = sorted({c.name for c in self.book._contacts if c.name})
        if names:
            print("\n(Press TAB to auto-complete a contact name.)")

        ContactCLI.enable_autofilled(names)

        query = input("Enter name to search (or 'b' to go back): ").strip()
        if query.lower() == "b":
            return [], ""

        q = query.lower()

        exact = [c for c in self.book._contacts if c.name.lower() == q]
        if exact:
            return exact, query

        results = [c for c in self.book._contacts if q in c.name.lower()]
        self.clear_screen()
        return results, query

    def _ensure_data_available(self) -> bool:
        if not self.book.get_all_contacts():  
            print("\nNo contacts found. Please add at least one contact first.")
            input("\nPress Enter ")
            return False
        return True
    
    def _select_contact_by_search(self):

        print("\n--- Edit Contact ---")
        results, query = self.search_contact()

        if not results:
            if query:
                print(f'\nNo contact found with name containing "{query}".')
            return None

        print(f'\nFound {len(results)} result{"s" if len(results) != 1 else ""}:')
        for i, c in enumerate(results, start=1):
            print(f"{i}. {c.name} | {c.phone} | {c.email}")

        if len(results) == 1:
            return results[0]

        name_input = input("\nEnter the exact contact name to edit (or 'b' to go back): ").strip()
        if name_input.lower() == "b":
            return None

        match = next((c for c in results if c.name.lower() == name_input.lower()), None)
        if not match:
            print(f'No contact found matching "{name_input}".')
            return None

        return match

    
    def edit_contact(self):
        self.clear_screen()
        contact = self._select_contact_by_search()
        if contact is None:
            return

        print("\nCurrent contact info:")
        print(f"Name : {contact.name}")
        print(f"Phone: {contact.phone}")
        print(f"Email: {contact.email}")

        print("\nEnter new details. Press Enter to keep the current value.")

        # --- Name loop ---
        while True:
            raw = input(f"New name [{contact.name}]: ").strip()
            if raw == "":
                new_name = contact.name  # keep current
                break
            ok, msg = self.check_field("name", raw, exclude=contact)
            if ok:
                new_name = msg.title()
                break
            print(msg)

        while True:
            raw = input(f"New phone number [{contact.phone}]: ").strip()
            if raw == "":
                new_phone = contact.phone
                break
            ok, msg = self.check_field("phone", raw, exclude=contact)
            if ok:
                new_phone = msg
                break
            print(msg)

        while True:
            raw = input(f"New email address [{contact.email}]: ").strip()
            if raw == "":
                new_email = contact.email
                break
            ok, msg = self.check_field("email", raw, exclude=contact)
            if ok:
                new_email = msg
                break
            print(msg)

        contact.name = new_name
        contact.phone = new_phone
        contact.email = new_email

        self.book.save()
        print("\nContact updated successfully!")
        input("\nPress Enter")

        
    def delete_contact(self):
        if not self._ensure_data_available():
            return

        print("\n--- Delete Contact ---")

        # Build autocomplete options from all names
        names = sorted({c.name for c in self.book._contacts if c.name})
        if names:
            print("\n(Press TAB to auto-complete a contact name.)")

        # Use your existing static method
        ContactCLI.enable_autofilled(names)

        name_input = input("Enter the name of the contact to delete (or 'b' to go back): ").strip()
        if name_input.lower() == "b":
            return

        # Case-insensitive exact match (unique names assumed)
        contact = next((c for c in self.book._contacts if c.name.lower() == name_input.lower()), None)
        if not contact:
            print(f'No contact found matching "{name_input}".')
            input("\nPress Enter")
            return

        # Show summary & confirm (per project spec)
        print("\nSelected contact:")
        print(f"Name : {contact.name}")
        print(f"Phone: {contact.phone}")
        print(f"Email: {contact.email}")

        confirm = input(f'\nAre you sure you want to delete "{contact.name}"? (yes/no): ').strip().lower()
        if confirm not in ("y", "yes"):
            print("Deletion cancelled.")
            input("\nPress Enter")
            return

        self.book._contacts.remove(contact)
        self.book.save()
        print("Contact deleted!")
        input("\nPress Enter")
