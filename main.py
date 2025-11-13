import json
import os
from cli import ContactCLI

DATA_DIR = "Contacts_data"  

if __name__ == "__main__":
    print("===============================")
    print("Welcome to the Contact Book CLI")
    print("===============================")

    os.makedirs(DATA_DIR, exist_ok=True)

    # Ask user for file name
    file_name = input("Enter the name of your data file (e.g., contacts.json): ").strip()

    if not file_name:
        file_name = "contacts.json"


    file_path = os.path.join(DATA_DIR, file_name)

 
    if not os.path.exists(file_path):
        with open(file_path, "w") as f:
            json.dump([], f)
        print(f"Created new data file: {file_path}")
    else:
        print(f"Using existing file: {file_path}")

    
    ContactCLI(file_path).run()