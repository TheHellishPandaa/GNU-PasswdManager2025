# Password Mangaer for save, generate, show saves password and manage password
# Date: 22/12/2024
# Jaime Galvez Martinez

# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from cryptography.fernet import Fernet
import json
import os
import random
import string


# Password management functions 
# Generate key function

def generate_key():
    return Fernet.generate_key()
# load key function

def load_key(filename='key.key'):
    if not os.path.exists(filename):
        key = generate_key()
        with open(filename, 'wb') as file:
            file.write(key)
    else:
        with open(filename, 'rb') as file:
            key = file.read()
    return key

def load_data(filename='users.json'):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            return json.load(file)
    else:
        return {}

def save_data(data, filename='users.json'):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

def load_passwords(user, filename='passwords.json'):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            data = json.load(file)
            if user in data:
                return data[user]
    return {}

def save_passwords(user, passwords, filename='passwords.json'):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            data = json.load(file)
    else:
        data = {}
    data[user] = passwords
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

# Authentication functions
def register_user():
    user = simpledialog.askstring("Register User", "Username:")
    if user in users:
        messagebox.showerror("Error", "The user already exists.")
        return
    password = simpledialog.askstring("Register User", "Password:", show='*')
    if user and password:
        users[user] = {'password': password}
        save_data(users)
        messagebox.showinfo("Success", "User successfully registered.")
    else:
        messagebox.showerror("Error", "All fields are required.")

def login_user():
    user = simpledialog.askstring("Login", "Username:")
    if user not in users:
        messagebox.showerror("Error", "User not found.")
        return None
    password = simpledialog.askstring("Login", "Password:", show='*')
    if users[user]['password'] == password:
        return user
    else:
        messagebox.showerror("Error", "Incorrect password.")
        return None

# Password management functions
def add_password(user):
    passwords = load_passwords(user)
    service = simpledialog.askstring("Add Password", "Service (e.g., Gmail, Instagram):")
    service_user = simpledialog.askstring("Add Password", "Service Username:")
    password = simpledialog.askstring("Add Password", "Password:", show='*')

    if service and service_user and password:
        fernet = Fernet(key)
        unique_id = str(len(passwords) + 1)
        passwords[unique_id] = {
            'service': service,
            'username': service_user,
            'password': fernet.encrypt(password.encode()).decode()
        }
        save_passwords(user, passwords)
        messagebox.showinfo("Success", f"Password added with ID: {unique_id}")
    else:
        messagebox.showerror("Error", "All fields are required.")

def show_passwords(user):
    passwords = load_passwords(user)
    if not passwords:
        messagebox.showinfo("No Passwords", "You have no saved passwords.")
        return
    
    show_window = tk.Toplevel(root)
    show_window.title("Saved Passwords")
    show_window.geometry("800x800")

    tree = ttk.Treeview(show_window, columns=("ID", "Service", "Username", "Password"), show='headings')
    tree.heading("ID", text="ID")
    tree.heading("Service", text="Service")
    tree.heading("Username", text="Username")
    tree.heading("Password", text="Password")
    tree.pack(expand=True, fill='both')

    fernet = Fernet(key)
    for unique_id, item_data in passwords.items():
        service = item_data['service']
        username = item_data['username']
        password = fernet.decrypt(item_data['password'].encode()).decode()
        tree.insert("", tk.END, values=(unique_id, service, username, password))

    # Add context menu to Treeview
    tree.bind("<Button-3>", lambda event: show_context_menu(event, tree))

# Generate password and add it
def generate_password(user):
    length = simpledialog.askinteger("Generate Password", "Password length:", minvalue=8, maxvalue=32)
    if length:
        characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choice(characters) for _ in range(length))
        service = simpledialog.askstring("Generate Password", "Service (e.g., Gmail, Instagram):")
        passwords = load_passwords(user)
        fernet = Fernet(key)
        unique_id = str(len(passwords) + 1)
        passwords[unique_id] = {
            'service': service,
            'username': 'Generated',
            'password': fernet.encrypt(password.encode()).decode()
        }
        save_passwords(user, passwords)
        messagebox.showinfo("Password Generated", f"Generated password: {password}\nIt has been added to your list.")
    else:
        messagebox.showerror("Error", "Invalid length.")

# Context menu for Treeview
def show_context_menu(event, tree):
    menu = tk.Menu(root, tearoff=0)
    menu.add_command(label="Copy", command=lambda: copy_selected_item(tree))
    menu.tk_popup(event.x_root, event.y_root)

def copy_selected_item(tree):
    try:
        selected_item = tree.focus()
        item_values = tree.item(selected_item, "values")
        if item_values:
            password = item_values[3]  # Copy the password
            root.clipboard_clear()
            root.clipboard_append(password)
            messagebox.showinfo("Copied", "Password copied to clipboard.")
    except IndexError:
        messagebox.showerror("Error", "No item selected.")

# GUI configuration
key = load_key()
users = load_data()

root = tk.Tk()
root.title("GNU-PasswdManager")
root.geometry("400x400")

def open_login():
    user = login_user()
    if user:
        login_frame.pack_forget()
        show_panel(user)

def show_panel(user):
    panel_frame = tk.Frame(root)
    panel_frame.pack(pady=20)

    title = tk.Label(panel_frame, text="GNU-PasswdManager", font=("Arial", 16, "bold"))
    title.pack(pady=10)

    add_button = tk.Button(panel_frame, text="Add Password", command=lambda: add_password(user), width=25)
    add_button.pack(pady=6)

    generate_button = tk.Button(panel_frame, text="Generate Secure Password", command=lambda: generate_password(user), width=25)
    generate_button.pack(pady=6)

    show_button = tk.Button(panel_frame, text="Show Passwords", command=lambda: show_passwords(user), width=25)
    show_button.pack(pady=6)

    exit_button = tk.Button(panel_frame, text="Logout", command=root.quit, width=25)
    exit_button.pack(pady=5)

login_frame = tk.Frame(root)
login_frame.pack(pady=20)

login_button = tk.Button(login_frame, text="Login", command=open_login, width=25)
login_button.pack(pady=5)

register_button = tk.Button(login_frame, text="Register User", command=register_user, width=25)
register_button.pack(pady=5)

root.mainloop()
