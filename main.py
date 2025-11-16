import json,os
import os
from cli import ContactCLI
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

console = Console()

DATA_DIR = "Contacts_data"




def banner(title: str):
    console.print(Panel.fit(Text(title, justify="center", style="bold cyan"), border_style="cyan"))



def ensure_json_name(name: str) -> str:
    name = name.strip()
    if not name:
        return "contacts.json"
    if not name.lower().endswith(".json"):
        name += ".json"
    return name




if __name__ == "__main__":
    banner("Welcome to the Contact Book CLI")

    os.makedirs(DATA_DIR, exist_ok=True)

    existing = sorted([f for f in os.listdir(DATA_DIR) if f.lower().endswith(".json")])

    if existing:
        console.print("[bold green]\nAvailable contact data files:[/bold green]\n")

        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("#", width=4)
        table.add_column("File Name", style="bold")
        for i, fname in enumerate(existing, start=1):
            table.add_row(str(i), fname)
        console.print(table)

        console.print("\n[i]Press [bold]Tab[/bold] to auto-complete a file name or type a new one.[/i]\n")
    else:
        console.print(Panel.fit(Text("No data files found yet. You can create one now.", style="yellow"), border_style="yellow"))

    # Enable filename autocompletion
    ContactCLI.enable_autofilled(existing)

    file_name = input("Enter the name of your data file (e.g., contacts.json): ").strip()
    file_name = ensure_json_name(file_name)

    file_path = os.path.join(DATA_DIR, file_name)

    if not os.path.exists(file_path):
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump([], f)
        console.print(Panel.fit(Text(f"Created new data file:\n{file_path}", style="bold green"), border_style="green"))
    else:
        console.print(Panel.fit(Text(f"Using existing file:\n{file_path}", style="bold cyan"), border_style="cyan"))

    ContactCLI(file_path).run()