from contact_book import ContactBook
from contact import Contact 
import re,os,questionary,csv
from typing import Tuple,List
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

console = Console()

def banner(title: str):
    console.print(Panel.fit(Text(title, justify="center", style="bold cyan"), border_style="cyan"))







class ContactCLI:
    def __init__(self, data_file: str):
        self.book = ContactBook(data_file)
    
    @staticmethod
    def enable_autofilled(options):
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
            banner(f"Contact Book ({self.book.data_file})")
            choice = questionary.select(
                "What would you like to do?",
                choices=[
                    "Add Contact",
                    "View All Contacts",
                    "Search Contact by Name",
                    "Edit Contact",
                    "Delete Contact",
                    "Export contacts to CSV",
                    "Save and Exit",
                    
                ],
            ).ask()

            if choice == "Add Contact":
                self.clear_screen(); self._add_contact()
            elif choice == "View All Contacts":
                self.clear_screen(); self._view_all_contacts()
            elif choice == "Search Contact by Name":
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
                self.display_contacts(results, f'Search Results for "{search_name}"')
                input("\nPress Enter")
                
            elif choice == "Edit Contact":
                self.clear_screen(); self.edit_contact()
            elif choice == "Delete Contact":
                self.clear_screen(); self.delete_contact()
            elif choice == "Export contacts to CSV":
                self.clear_screen()
                self.export_to_csv()
            
            else:
                self.clear_screen()
                console.print("[green]Saving contacts…[/green]")
                self.book.save()
                console.print("[bold green]Done![/bold green]")
                input("")
                self.clear_screen()
                break

    
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



    def display_contacts(self, contacts: List[Contact], title: str, show_total: bool = True) -> None:
        """Render a styled banner + contacts table using Rich."""
        banner(title)

        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("#", width=4)
        table.add_column("Name", style="bold")
        table.add_column("Phone", style="cyan")
        table.add_column("Email", style="yellow")

        for i, c in enumerate(contacts, start=1):
            table.add_row(str(i), c.name, c.phone, c.email)

        console.print(table)

        if show_total:
            console.print(f"[dim]Total: {len(contacts)} contact{'s' if len(contacts) != 1 else ''}[/dim]")


    
    def _view_all_contacts(self):
        self.clear_screen()
        if not self._ensure_data_available():
            return
        contacts = self.book.get_all_contacts()
        self.display_contacts(contacts, "All Contacts")
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
        
        console.print(Panel.fit(Text("Edit Contact", justify="center", style="bold cyan"),border_style="cyan"))

        results, query = self.search_contact()

        if not results:
            if query:
                console.print(f'\n[bold red]No contact found[/bold red] with name containing "[yellow]{query}[/]".')
            return None
        self.display_contacts(results, "Edit Contact")


        if len(results) == 1:
            return results[0]
        console.print("\n[i]Type the exact contact name to edit, or[/i] [bold]b[/bold] [i]to go back.[/i]")
        name_input = input("Name: ").strip()
        if name_input.lower() == "b":
            return None

        match = next((c for c in results if c.name.lower() == name_input.lower()), None)
        if not match:
            console.print(f'[bold red]No contact found matching[/bold red] "[yellow]{name_input}[/]".')
            return None
        return match
            

    
    def edit_contact(self):
        self.clear_screen()
        contact = self._select_contact_by_search()
        if contact is None:
            return

        print("\nCurrent contact info:\n")
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
        
    def export_to_csv(self):
        if not self._ensure_data_available():
            return

        print("\n--- Export Contacts to CSV ---")

        default_name = os.path.splitext(os.path.basename(self.book.data_file))[0] + "_export.csv"

        file_name = input(f"Enter CSV file name (default: {default_name}): ").strip()
        if not file_name:
            file_name = default_name
        if not file_name.lower().endswith(".csv"):
            file_name += ".csv"

        export_path = os.path.join(os.path.dirname(self.book.data_file), file_name)

        try:
            with open(export_path, mode="w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["Name", "Phone", "Email"])
                for c in self.book._contacts:
                    writer.writerow([c.name, c.phone, c.email])

            print(f'\nContacts successfully exported to: "{export_path}"')
        except Exception as e:
            print(f"\n[Error] Could not export contacts: {e}")

        input("\nPress Enter")
