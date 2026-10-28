import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector

# Database Connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Winlog@1211",  # Replace with your MySQL root password
        database="password_manager"
    )

def add_password():
    platform = entry_platform.get()
    username = entry_username.get()
    password = entry_password.get()

    if not platform or not username or not password:
        messagebox.showerror("Error", "All fields are required!")
        return

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO passwords (platform, username, password) VALUES (%s, %s, %s)", 
                       (platform, username, password))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Password saved successfully!")
        clear_fields()
        load_data()
    except Exception as e:
        messagebox.showerror("Database Error", str(e))

def update_password():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "Please select a record to update!")
        return

    record_id = tree.item(selected_item)['values'][0]
    platform = entry_platform.get()
    username = entry_username.get()
    password = entry_password.get()

    if not platform or not username or not password:
        messagebox.showerror("Error", "All fields are required!")
        return

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE passwords SET platform=%s, username=%s, password=%s WHERE id=%s", 
                       (platform, username, password, record_id))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Password updated successfully!")
        clear_fields()
        load_data()
    except Exception as e:
        messagebox.showerror("Database Error", str(e))

def delete_password():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "Please select a record to delete!")
        return

    record_id = tree.item(selected_item)['values'][0]

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM passwords WHERE id=%s", (record_id,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Password deleted successfully!")
        clear_fields()
        load_data()
    except Exception as e:
        messagebox.showerror("Database Error", str(e))

def load_data():
    for row in tree.get_children():
        tree.delete(row)
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM passwords")
        for row in cursor.fetchall():
            tree.insert("", "end", values=row)
        conn.close()
    except Exception as e:
        messagebox.showerror("Database Error", str(e))

def select_record(event):
    selected_item = tree.selection()
    if selected_item:
        row_data = tree.item(selected_item)['values']
        clear_fields()
        entry_platform.insert(0, row_data[1])
        entry_username.insert(0, row_data[2])
        entry_password.insert(0, row_data[3])

def clear_fields():
    entry_platform.delete(0, tk.END)
    entry_username.delete(0, tk.END)
    entry_password.delete(0, tk.END)

# GUI Setup
root = tk.Tk()
root.title("Password Manager - Python & MySQL Project")
root.geometry("650x480")

# Form Frame
frame = tk.LabelFrame(root, text="Password Details", font=("Arial", 10, "bold"))
frame.pack(fill="x", padx=15, pady=15)

tk.Label(frame, text="Platform:").grid(row=0, column=0, padx=10, pady=8, sticky="w")
entry_platform = tk.Entry(frame, width=30)
entry_platform.grid(row=0, column=1, padx=10, pady=8)

tk.Label(frame, text="Username/Email:").grid(row=1, column=0, padx=10, pady=8, sticky="w")
entry_username = tk.Entry(frame, width=30)
entry_username.grid(row=1, column=1, padx=10, pady=8)

tk.Label(frame, text="Password:").grid(row=2, column=0, padx=10, pady=8, sticky="w")
entry_password = tk.Entry(frame, width=30)
entry_password.grid(row=2, column=1, padx=10, pady=8)

# Buttons Frame
btn_frame = tk.Frame(root)
btn_frame.pack(pady=5)

tk.Button(btn_frame, text="Add", command=add_password, bg="#4CAF50", fg="white", width=10).grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="Update", command=update_password, bg="#FF9800", fg="white", width=10).grid(row=0, column=1, padx=5)
tk.Button(btn_frame, text="Delete", command=delete_password, bg="#F44336", fg="white", width=10).grid(row=0, column=2, padx=5)
tk.Button(btn_frame, text="Clear", command=clear_fields, bg="#9E9E9E", fg="white", width=10).grid(row=0, column=3, padx=5)

# Table View
columns = ("ID", "Platform", "Username", "Password")
tree = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=140)
tree.pack(fill="both", expand=True, padx=15, pady=15)
tree.bind("<ButtonRelease-1>", select_record)

load_data()
root.mainloop()