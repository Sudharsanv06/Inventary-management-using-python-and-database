import tkinter as tk
from tkinter import ttk
import sqlite3
from tkinter import messagebox

# Declare entry widgets globally
entry_name = None
entry_quantity = None
entry_price = None
entry_branch = None

def create_database():
    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS INVENTORY ("
                   "ITEM_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,"
                   "PRODUCT_NAME TEXT,"
                   "QUANTITY INTEGER,"
                   "PRICE REAL,"
                   "BRANCH TEXT)"
                   )
    conn.commit()
    conn.close()

def insert_record():
    global entry_name, entry_quantity, entry_price, entry_branch
    product_name = entry_name.get()
    quantity = entry_quantity.get()
    price = entry_price.get()
    branch = entry_branch.get()

    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO INVENTORY (PRODUCT_NAME, QUANTITY, PRICE, BRANCH) "
                   "VALUES (?, ?, ?, ?)",
                   (product_name, quantity, price, branch)
                   )
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Inventory record added successfully!")

def display_table():
    # Retrieve data from the database and display it in a Treeview widget
    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM INVENTORY")
    data = cursor.fetchall()
    conn.close()

    top = tk.Toplevel()
    top.title("Inventory Records")

    tree = ttk.Treeview(top, columns=("Item ID", "Product Name", "Quantity", "Price", "Branch"))
    tree.heading("#1", text="Item ID")
    tree.heading("#2", text="Product Name")
    tree.heading("#3", text="Quantity")
    tree.heading("#4", text="Price")
    tree.heading("#5", text="Branch")

    for row in data:
        tree.insert("", "end", values=row)

    tree.pack()

def create_gui():
    global entry_name, entry_quantity, entry_price, entry_branch
    display_screen = tk.Tk()
    display_screen.geometry("800x400")
    display_screen.title("Inventory Management System")

    label_name = ttk.Label(display_screen, text="Product Name:")
    label_name.pack()
    entry_name = ttk.Entry(display_screen)
    entry_name.pack()

    label_quantity = ttk.Label(display_screen, text="Quantity:")
    label_quantity.pack()
    entry_quantity = ttk.Entry(display_screen)
    entry_quantity.pack()

    label_price = ttk.Label(display_screen, text="Price:")
    label_price.pack()
    entry_price = ttk.Entry(display_screen)
    entry_price.pack()

    label_branch = ttk.Label(display_screen, text="Branch:")
    label_branch.pack()
    entry_branch = ttk.Entry(display_screen)
    entry_branch.pack()

    btn_insert = ttk.Button(display_screen, text="Insert Record", command=insert_record)
    btn_insert.pack()

    btn_display = ttk.Button(display_screen, text="Display Table", command=display_table)
    btn_display.pack()

create_database()  # Create the database and table

create_gui()  # Create the GUI and run the application
