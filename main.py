import json,os
import os
from cli import ContactCLI
DATA_DIR = "Contacts_data"







def ensure_json_name(name: str) -> str:
    name = name.strip()
    if not name:
        return "contacts.json"
    if not name.lower().endswith(".json"):
        name += ".json"
    return name


if __name__ == "__main__":
    print("===============================")
    print("Welcome to the Contact Book CLI")
    print("===============================")

    os.makedirs(DATA_DIR, exist_ok=True)

    existing = sorted(
        [f for f in os.listdir(DATA_DIR) if f.lower().endswith(".json")]
    )

    if existing:
        print("\nAvailable contact data files:")
        for fname in existing:
            print(f"  - {fname}")
        print("\n(Press TAB to auto-complete a file name or type a new one.)")
    else:
        print("\nNo data files found yet. You can create one now.")

    ContactCLI.enable_autofilled(existing)

    file_name = input("Enter the name of your data file (e.g., contacts.json): ").strip()
    file_name = ensure_json_name(file_name)

    file_path = os.path.join(DATA_DIR, file_name)

    if not os.path.exists(file_path):
        with open(file_path, "w") as f:
            json.dump([], f)
        print(f"Created new data file: {file_path}")
    else:
        print(f"Using existing file: {file_path}")

    ContactCLI(file_path).run()
    
    