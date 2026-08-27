# 📦 Inventory Management System (IMS)

A modern desktop Inventory Management System built with **Python**, **CustomTkinter** (for a sleek dark-themed GUI), and **SQLite3** (for local data persistence). The application offers real-time inventory tracking, input validation, live search, low-stock filtering, automatic branch learning, running total valuation, and CSV data exports.

---

## ✨ Features

- **Full CRUD Operations**: Easily insert new inventory items, update existing records by clicking rows in the table, or delete entries with confirmation prompts.
- **Robust Input Validation**: Inline red error feedback for missing fields, non-numeric inputs, or negative values for quantity and price.
- **Live Search & Filter**: Instant filtering by Product Name or Branch as you type.
- **Low-Stock Alert**: One-click checkbox filter to view low-stock items (`Quantity < 10`).
- **Dynamic Branch Dropdown**: Editable branch selection dropdown that automatically includes new branch names typed into the form.
- **Running Total Valuation**: Computes and displays the true total inventory valuation (`Quantity × Price`) across all stored items in real time.
- **CSV Data Export**: One-click export of all inventory records to a standard `.csv` file format.
- **Modern Dark UI**: Designed with CustomTkinter for a responsive, dark-themed desktop experience paired with styled data tables.

---

## 🛠️ Tech Stack

- **Python 3.x** — Core language
- **CustomTkinter** — Modern dark GUI framework
- **Tkinter & `ttk.Treeview`** — Desktop windowing & tabular data grid
- **SQLite3** — Lightweight, embedded relational database (`inventory.db`)

---

## 📂 Project Structure

```
.
├── IMS/
│   ├── inventary.py     # Main application source code (InventoryDB & InventoryApp)
│   └── inventory.db     # SQLite database generated automatically at runtime
├── requirements.txt     # Dependency file (customtkinter)
└── README.md            # Project documentation
```

---

## 🚀 Getting Started

### Prerequisites

Ensure Python 3.8+ is installed on your system.

### Installation & Execution

1. **Install Dependencies**:
   ```powershell
   pip install -r requirements.txt
   ```

2. **Run the Application**:
   ```powershell
   cd IMS
   py inventary.py
   ```
