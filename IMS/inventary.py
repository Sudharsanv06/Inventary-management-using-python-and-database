import csv
import sqlite3
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

LOW_STOCK_THRESHOLD = 10


class InventoryDB:
    """Handles all SQLite database operations for the Inventory System."""

    def __init__(self, db_name="inventory.db"):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self._create_table()

    def _create_table(self):
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS INVENTORY ("
            "ITEM_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,"
            "PRODUCT_NAME TEXT,"
            "QUANTITY INTEGER,"
            "PRICE REAL,"
            "BRANCH TEXT)"
        )
        self.conn.commit()

    def insert(self, name, qty, price, branch):
        self.cursor.execute(
            "INSERT INTO INVENTORY (PRODUCT_NAME, QUANTITY, PRICE, BRANCH) "
            "VALUES (?, ?, ?, ?)",
            (name, qty, price, branch),
        )
        self.conn.commit()

    def update(self, item_id, name, qty, price, branch):
        self.cursor.execute(
            "UPDATE INVENTORY SET PRODUCT_NAME=?, QUANTITY=?, PRICE=?, BRANCH=? "
            "WHERE ITEM_ID=?",
            (name, qty, price, branch, item_id),
        )
        self.conn.commit()

    def delete(self, item_id):
        self.cursor.execute("DELETE FROM INVENTORY WHERE ITEM_ID=?", (item_id,))
        self.conn.commit()

    def distinct_branches(self):
        self.cursor.execute("SELECT DISTINCT BRANCH FROM INVENTORY")
        rows = self.cursor.fetchall()
        db_branches = {row[0] for row in rows if row[0]}
        defaults = {"Chennai", "Bangalore", "Mumbai", "Delhi", "Hyderabad"}
        return sorted(list(defaults.union(db_branches)))

    def search(self, keyword):
        pattern = f"%{keyword}%"
        self.cursor.execute(
            "SELECT * FROM INVENTORY WHERE PRODUCT_NAME LIKE ? OR BRANCH LIKE ? ORDER BY ITEM_ID",
            (pattern, pattern),
        )
        return self.cursor.fetchall()

    def low_stock(self, threshold=LOW_STOCK_THRESHOLD):
        self.cursor.execute(
            "SELECT * FROM INVENTORY WHERE QUANTITY < ? ORDER BY ITEM_ID", (threshold,)
        )
        return self.cursor.fetchall()

    def total_value(self):
        self.cursor.execute("SELECT SUM(QUANTITY * PRICE) FROM INVENTORY")
        val = self.cursor.fetchone()[0]
        return float(val) if val is not None else 0.0

    def fetch_all(self):
        self.cursor.execute("SELECT * FROM INVENTORY ORDER BY ITEM_ID")
        return self.cursor.fetchall()

    def close(self):
        if self.conn:
            self.conn.close()


class InventoryApp(ctk.CTk):
    """GUI Application for Inventory Management System."""

    def __init__(self):
        super().__init__()
        self.title("Inventory Management System")
        self.geometry("800x400")

        self.selected_item_id = None
        self.tree = None
        self.total_label = None
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", self.on_search)
        self.low_stock_var = tk.BooleanVar(value=False)

        self.db = InventoryDB()
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self._build_widgets()

    def _build_widgets(self):
        label_name = ctk.CTkLabel(self, text="Product Name:")
        label_name.pack(pady=(10, 0))
        self.entry_name = ctk.CTkEntry(self)
        self.entry_name.pack(pady=2)

        label_quantity = ctk.CTkLabel(self, text="Quantity:")
        label_quantity.pack(pady=(5, 0))
        self.entry_quantity = ctk.CTkEntry(self)
        self.entry_quantity.pack(pady=2)

        label_price = ctk.CTkLabel(self, text="Price:")
        label_price.pack(pady=(5, 0))
        self.entry_price = ctk.CTkEntry(self)
        self.entry_price.pack(pady=2)

        label_branch = ctk.CTkLabel(self, text="Branch:")
        label_branch.pack(pady=(5, 0))
        self.branch_var = tk.StringVar()
        self.combo_branch = ctk.CTkComboBox(
            self, variable=self.branch_var, values=self.db.distinct_branches()
        )
        self.combo_branch.pack(pady=2)

        self.error_label = ctk.CTkLabel(self, text="", text_color="#ff6b6b")
        self.error_label.pack(pady=2)

        btn_insert = ctk.CTkButton(self, text="Insert Record", command=self.insert_record)
        btn_insert.pack(pady=3)

        btn_update = ctk.CTkButton(self, text="Update Selected", command=self.update_record)
        btn_update.pack(pady=3)

        btn_delete = ctk.CTkButton(self, text="Delete Selected", command=self.delete_record)
        btn_delete.pack(pady=3)

        btn_display = ctk.CTkButton(self, text="Display Table", command=self.display_table)
        btn_display.pack(pady=3)

    def _read_and_validate(self):
        name = self.entry_name.get().strip()
        qty_str = self.entry_quantity.get().strip()
        price_str = self.entry_price.get().strip()
        branch = self.branch_var.get().strip()

        if not name:
            return None, "Product name cannot be empty."

        if not branch:
            return None, "Branch cannot be empty."

        try:
            qty = int(qty_str)
            if qty < 0:
                raise ValueError
        except ValueError:
            return None, "Quantity must be a whole number \u2265 0."

        try:
            price = float(price_str)
            if price < 0:
                raise ValueError
        except ValueError:
            return None, "Price must be a number \u2265 0."

        return (name, qty, price, branch), None

    def _refresh_branch_list(self):
        self.combo_branch.configure(values=self.db.distinct_branches())

    def insert_record(self):
        data, error = self._read_and_validate()
        if error:
            self.error_label.configure(text=error)
            return

        self.error_label.configure(text="")
        name, qty, price, branch = data

        self.db.insert(name, qty, price, branch)
        messagebox.showinfo("Success", "Inventory record added successfully!")
        self.clear_fields()
        self.refresh_table()
        self._refresh_branch_list()

    def update_record(self):
        if self.selected_item_id is None:
            messagebox.showwarning("Warning", "Please select a row from the inventory table first.")
            return

        data, error = self._read_and_validate()
        if error:
            self.error_label.configure(text=error)
            return

        self.error_label.configure(text="")
        name, qty, price, branch = data

        self.db.update(self.selected_item_id, name, qty, price, branch)
        messagebox.showinfo("Success", "Inventory record updated successfully!")
        self.clear_fields()
        self.refresh_table()
        self._refresh_branch_list()

    def delete_record(self):
        if self.selected_item_id is None:
            messagebox.showwarning("Warning", "Please select a row from the inventory table first.")
            return

        confirm = messagebox.askyesno(
            "Confirm Delete", "Delete the selected record? This cannot be undone."
        )
        if confirm:
            self.db.delete(self.selected_item_id)
            self.clear_fields()
            self.refresh_table()

    def export_csv(self):
        data = self.db.fetch_all()
        if not data:
            messagebox.showwarning("No Data", "There are no records to export.")
            return

        filepath = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            initialfile="inventory_export.csv",
        )
        if not filepath:
            return

        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Item ID", "Product Name", "Quantity", "Price", "Branch"])
            writer.writerows(data)

        messagebox.showinfo("Success", f"Inventory records exported successfully to:\n{filepath}")

    def display_table(self):
        self.search_var.set("")
        self.low_stock_var.set(False)
        data = self.db.fetch_all()

        top = ctk.CTkToplevel(self)
        top.title("Inventory Records")

        search_frame = ctk.CTkFrame(top)
        search_frame.pack(fill="x", padx=5, pady=5)

        search_label = ctk.CTkLabel(search_frame, text="Search:")
        search_label.pack(side="left", padx=(5, 5))

        search_entry = ctk.CTkEntry(search_frame, textvariable=self.search_var)
        search_entry.pack(side="left", fill="x", expand=True, padx=5)

        chk_low_stock = ctk.CTkCheckBox(
            search_frame,
            text=f"Low stock only (< {LOW_STOCK_THRESHOLD})",
            variable=self.low_stock_var,
            command=self.on_search,
        )
        chk_low_stock.pack(side="left", padx=(10, 5))

        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Treeview",
            background="#2b2b2b",
            fieldbackground="#2b2b2b",
            foreground="white",
            rowheight=26,
            borderwidth=0,
        )
        style.configure(
            "Treeview.Heading",
            background="#1f1f1f",
            foreground="white",
            font=("Segoe UI", 10, "bold"),
        )
        style.map("Treeview", background=[("selected", "#1f6aa5")])

        self.tree = ttk.Treeview(
            top, columns=("Item ID", "Product Name", "Quantity", "Price", "Branch")
        )
        self.tree.heading("#1", text="Item ID")
        self.tree.heading("#2", text="Product Name")
        self.tree.heading("#3", text="Quantity")
        self.tree.heading("#4", text="Price")
        self.tree.heading("#5", text="Branch")

        for row in data:
            self.tree.insert("", "end", values=row)

        self.tree.bind("<<TreeviewSelect>>", self.on_row_select)
        self.tree.pack(fill="both", expand=True, padx=5, pady=5)

        bottom_frame = ctk.CTkFrame(top)
        bottom_frame.pack(fill="x", padx=5, pady=5)

        val = self.db.total_value()
        self.total_label = ctk.CTkLabel(
            bottom_frame, text=f"Total Inventory Value: {val:.2f}"
        )
        self.total_label.pack(side="left", padx=5)

        btn_export = ctk.CTkButton(
            bottom_frame, text="Export CSV", command=self.export_csv
        )
        btn_export.pack(side="right", padx=5)

    def refresh_table(self, rows=None):
        if self.tree and self.tree.winfo_exists():
            for item in self.tree.get_children():
                self.tree.delete(item)
            data = rows if rows is not None else self.db.fetch_all()
            for row in data:
                self.tree.insert("", "end", values=row)
            if self.total_label and self.total_label.winfo_exists():
                val = self.db.total_value()
                self.total_label.configure(text=f"Total Inventory Value: {val:.2f}")

    def on_search(self, *args):
        keyword = self.search_var.get().strip().lower()
        is_low_stock = self.low_stock_var.get()

        if is_low_stock:
            rows = self.db.low_stock(LOW_STOCK_THRESHOLD)
            if keyword:
                rows = [
                    r for r in rows
                    if keyword in str(r[1]).lower() or keyword in str(r[4]).lower()
                ]
        elif keyword:
            rows = self.db.search(keyword)
        else:
            rows = None

        self.refresh_table(rows=rows)

    def on_row_select(self, event):
        if not self.tree:
            return
        selected = self.tree.selection()
        if not selected:
            return

        item = self.tree.item(selected[0])
        values = item.get("values", [])
        if values:
            self.selected_item_id = values[0]

            self.entry_name.delete(0, tk.END)
            self.entry_name.insert(0, values[1])

            self.entry_quantity.delete(0, tk.END)
            self.entry_quantity.insert(0, values[2])

            self.entry_price.delete(0, tk.END)
            self.entry_price.insert(0, values[3])

            self.branch_var.set(values[4])

    def clear_fields(self):
        self.entry_name.delete(0, tk.END)
        self.entry_quantity.delete(0, tk.END)
        self.entry_price.delete(0, tk.END)
        self.branch_var.set("")
        self.error_label.configure(text="")
        self.selected_item_id = None

    def on_close(self):
        self.db.close()
        self.destroy()


if __name__ == "__main__":
    app = InventoryApp()
    app.mainloop()
