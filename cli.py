from contact_book import ContactBook
from contact import Contact 
import re,os,time
from typing import Tuple,List



class ContactCLI:
    def __init__(self, data_file: str):
        self.book = ContactBook(data_file)

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
                print("\n--- Search Contact by Name ---")
                search_name = input("Enter name to search: ").strip()
                results = self.search_contact(search_name)
                print(self._format_contacts_for_display(results,f'Search Results for "{search_name}"'))
                input("\nPress Enter")
                
            elif choice == "4":
                self.clear_screen()
                self.edit_contact()
                
                
            elif choice == "5":
                self.clear_screen()
                print("\nDeleting contacts feature coming next.")
                input("\nPress Enter")
            
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
                
    def check_field(self, field_type: str, value: str) -> Tuple[bool, str]:
        
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

        while True:
            name_input = input("Enter full name: ").strip()
            valid, message = self.check_field("name", name_input)
            if valid:
                name = message
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
        
        
    def search_contact(self,name:str) -> List[Contact]:
        name = name.strip().lower()
        return [c for c in self.book._contacts if name in c.name.lower()]

    def _ensure_data_available(self) -> bool:
        if not self.book.get_all_contacts():  
            print("\nNo contacts found. Please add at least one contact first.")
            input("\nPress Enter ")
            return False
        return True
    
    def _select_contact_by_search(self):
        if not self._ensure_data_available():
            return None

        print("\n--- Edit Contact ---")
        query = input("Enter a name to search: ").strip()
        results = self.search_contact(query)

        if not results:
            print(f'\nNo contact found with name containing "{query}".')
            input("\nPress Enter to return to the main menu...")
            return None

        # Show results in a compact list for selection
        print(f'\nFound {len(results)} result{"s" if len(results)!=1 else ""}:')
        for i, c in enumerate(results, start=1):
            print(f"{i}. {c.name} | {c.phone} | {c.email}")

        # Let the user pick
        while True:
            choice = input("\nEnter the number to edit (or 'b' to go back): ").strip().lower()
            if choice == "b":
                return None
            if choice.isdigit():
                idx = int(choice)
                if 1 <= idx <= len(results):
                    return results[idx - 1]
            print("Invalid choice. Please enter a valid number or 'b'.")

    
    def edit_contact(self):
        self.clear_screen()
        contact = self._select_contact_by_search()
        if not contact:
            return None
            
    

        print("\nCurrent contact info:")
        print(f"Name : {contact.name}")
        print(f"Phone: {contact.phone}")
        print(f"Email: {contact.email}")

        print("\nEnter new details (press Enter to keep current):")
        new_name  = input("New name: ").strip()
        new_phone = input("New phone number: ").strip()
        new_email = input("New email address: ").strip()

        if new_name and new_name != contact.name:
            ok, msg = self.check_field("name", new_name)
            if not ok:
                print(msg); input("\nPress Enter"); return

        if new_phone and new_phone != contact.phone:
            ok, msg = self.check_field("phone", new_phone)
            if not ok:
                print(msg); input("\nPress Enter"); return

        if new_email and new_email != contact.email:
            ok, msg = self.check_field("email", new_email)
            if not ok:
                print(msg); input("\nPress Enter"); return

        if new_name:  contact.name  = new_name
        if new_phone: contact.phone = new_phone
        if new_email: contact.email = new_email

        self.book.save()
        print("\nContact updated successfully!")
        input("\nPress Enter")

        