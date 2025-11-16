# 📘 Contact Book CLI Application

## 🧠 Overview
The **Contact Book CLI** is a Python command-line application that helps you manage your contacts easily and efficiently.  
It supports **adding, viewing, searching, editing, deleting, and exporting contacts**, all through a clean, colorful interface built with **Rich** and **Questionary**.  
The app also provides **Tab-based autocompletion** for quick file and contact selection.

## ✨ Features

### ✅ Core
- **Add Contact** — Create contacts with validation for name, phone, and email.  
- **View All Contacts** — Display all contacts in a Rich-styled table.  
- **Search Contact by Name** — Partial search + Tab autocompletion.  
- **Edit Contact** — Update fields; press **Enter** to keep current value.  
- **Delete Contact** — Confirmed deletion with autocompletion of names.  
- **Export to CSV** — Export the full contact list to a `.csv` file.  
- **Save & Exit** — Persist changes to the selected JSON file.  

---

### 💡 Extra
- **Rich UI:** Banners, panels, and color-coded tables for an enhanced terminal experience.  
- **Questionary Menus:** Interactive, user-friendly selection for all main actions.  
- **Centralized Display Helpers:** Ensure consistent Rich-styled formatting across views.  
- **Cross-Platform Support:** Compatible with Windows, macOS, and Linux.  

---

### ⌨️ Autocompletion
The CLI uses the **`readline`** library (or **`pyreadline3`** on Windows) to enable **Tab-based autocompletion**.

---

## 🚀 Getting Started

### 🧩 1. Requirements
- **Python** 3.9+ (recommended 3.10 or newer)
- Works on **macOS**, **Linux**, and **Windows**

---

### 🧰 2. Installation
Clone the repository and install dependencies:

```bash
git clone https://github.com/gabin-dave/Contact-Book-CLI-Application.git
cd Contact-Book-CLI-Application
pip install rich questionary
pip install pyreadline3
python3 main.py

