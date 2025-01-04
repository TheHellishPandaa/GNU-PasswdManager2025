# AUTHOR: JAIME GALVEZ MARTINEZ
# DATE: 31/12/2024
# VERSION: 0.3
# For User Manual, please read the `readme` file
# This project is released under GNU (General Public License). All rights reserved.
# Password Manager written 100% in Python

# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from cryptography.fernet import Fernet
import json
import os
import sys
import random
import string


# Password management functions
def generate_key():
    return Fernet.generate_key()


def load_key(filename='key.key'):
    """
    Loads or generates a Fernet key for encryption/decryption.

    Args:
        filename (str): The filename to save or load the key.

    Returns:
        bytes: The encryption key.
    """
    # Check if the key file exists
    if not os.path.exists(filename):
        # If not, generate a new key
        key = generate_key()
        # Save the new key to the file
        with open(filename, 'wb') as file:
            file.write(key)
    else:
        # If the file exists, load the key
        with open(filename, 'rb') as file:
            key = file.read()
    return key


# Create users.json that have all users loggued in the program (only is read by the user 'sudo')
def load_data(filename='users.json'):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            return json.load(file)
    else:
        return {}

def save_data(data, filename='users.json'):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)


# Ensure `users.json` exists with proper permissions
def setup_users_file(filename='users.json'):
    if not os.path.exists(filename):
        with open(filename, 'w') as file:
            json.dump({}, file, indent=4)  # Create an empty JSON object
        os.chmod(filename, 0o600)
        try:
            os.chown(filename, 0, 0)  # Requires sudo
        except AttributeError:
            messagebox.showwarning("Warning", "os.chown is not supported on this system.")


# Check for superuser privileges
def ensure_superuser():
    if os.name != "nt" and os.geteuid() != 0:
        print("This script must be run with superuser privileges (sudo).")
        sys.exit(1)


# Generate a random password
def generate_password(user):
    length = simpledialog.askinteger("Generate Password", "Password length (8-32):", minvalue=8, maxvalue=32)
    if length:
        characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choice(characters) for _ in range(length))
        
        service = simpledialog.askstring("Generate Password", "Service Name (e.g., Gmail, Instagram):")
        if service:
            passwords = load_passwords(user)
            fernet = Fernet(key)
            unique_id = str(len(passwords) + 1)
            passwords[unique_id] = {
                'service': service,
                'username': 'Generated',
                'password': fernet.encrypt(password.encode()).decode()
            }
            save_passwords(user, passwords)
            messagebox.showinfo("Password Generated", f"Generated password: {password}\nIt has been saved to your password list.")
        else:
            messagebox.showerror("Error", "Service name is required.")
    else:
        messagebox.showerror("Error", "Invalid password length.")

def load_passwords(user, filename='passwords.json'):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            data = json.load(file)
            if user in data:
                return data[user]
    return {}
    
def add_password(user):
    passwords = load_passwords(user)
    service = simpledialog.askstring("Add Password", "Service Name (e.g., Gmail, Instagram):")
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

def save_passwords(user, passwords, filename='passwords.json'):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            data = json.load(file)
    else:
        data = {}
    data[user] = passwords
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

def show_passwords(user):
    passwords = load_passwords(user)
    if not passwords:
        messagebox.showinfo("No Passwords", "You have no saved passwords.")
        return
    
    def copy_to_clipboard():
        selected_item = tree.focus()
        if not selected_item:
            messagebox.showerror("Error", "No password selected.")
            return
        values = tree.item(selected_item, "values")
        if len(values) >= 4:
            clipboard_password = values[3]
            root.clipboard_clear()
            root.clipboard_append(clipboard_password)
            root.update()  # Keep the clipboard data
            messagebox.showinfo("Copied", "Password copied to clipboard.")

    show_window = tk.Toplevel(root)
    show_window.title("Saved Passwords")
    show_window.geometry("600x800")
    show_window.configure(bg='#f0f0f0')

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

    copy_button = tk.Button(show_window, text="Copy Password", command=copy_to_clipboard)
    copy_button.pack(pady=10)

# Authentication functions
def register_user():
    user = simpledialog.askstring("Register User", "Username:")
    if user in users:
        messagebox.showerror("Error", "User already exists.")
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

# GUI configuration
ensure_superuser()
setup_users_file()

key = load_key()
users = load_data()

root = tk.Tk()
root.title("GNU-PasswdManager")
root.geometry("1200x800")
root.configure(bg='#f0f0f0')

def open_login():
    user = login_user()
    if user:
        login_frame.pack_forget()
        show_panel(user)

def show_panel(user):
    panel_frame = tk.Frame(root, bg='#f0f0f0')
    panel_frame.pack(pady=20)

    title = tk.Label(panel_frame, text="GNU-PasswdManager", font=("Arial Black", 32, "bold"), bg='#f0f0f0')
    title.pack(pady=10)

    add_button = tk.Button(panel_frame, text="Add Password", command=lambda: add_password(user), width=25)
    add_button.pack(pady=5)

    generate_button = tk.Button(panel_frame, text="Generate Password", command=lambda: generate_password(user), width=25)
    generate_button.pack(pady=5)

    show_button = tk.Button(panel_frame, text="Show Passwords", command=lambda: show_passwords(user), width=25)
    show_button.pack(pady=5)

    exit_button = tk.Button(panel_frame, text="Logout", command=root.quit, width=25)
    exit_button.pack(pady=5)

login_frame = tk.Frame(root, bg='#f0f0f0')
login_frame.pack(pady=20)

login_button = tk.Button(login_frame, text="Login", command=open_login, width=25)
login_button.pack(pady=5)

register_button = tk.Button(login_frame, text="Register User", command=register_user, width=25)
register_button.pack(pady=5)

root.mainloop()
