# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from cryptography.fernet import Fernet
import json
import os
import random
import string

# Funciones de manejo de contraseñas
def generate_key():
    return Fernet.generate_key()

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

# Funciones de autenticacion
def register_user():
    user = simpledialog.askstring("Registrar Usuario", "Nombre de usuario:")
    if user in users:
        messagebox.showerror("Error", "El usuario ya existe.")
        return
    password = simpledialog.askstring("Registrar Usuario", "Contrasena:", show='*')
    if user and password:
        users[user] = {'password': password}
        save_data(users)
        messagebox.showinfo("Exito", "Usuario registrado con exito.")
    else:
        messagebox.showerror("Error", "Todos los campos son obligatorios.")

def login_user():
    user = simpledialog.askstring("Iniciar Sesion", "Nombre de usuario:")
    if user not in users:
        messagebox.showerror("Error", "Usuario no encontrado.")
        return None
    password = simpledialog.askstring("Iniciar Sesion", "Contrasena:", show='*')
    if users[user]['password'] == password:
        return user
    else:
        messagebox.showerror("Error", "Contrasena incorrecta.")
        return None

# Funciones de manejo de contraseñas
def add_password(user):
    passwords = load_passwords(user)
    service = simpledialog.askstring("Agregar Contrasena", "Servicio (e.g., Gmail, Instagram):")
    service_user = simpledialog.askstring("Agregar Contrasena", "Nombre de Usuario del Servicio:")
    password = simpledialog.askstring("Agregar Contrasena", "Contrasena:", show='*')

    if service and service_user and password:
        fernet = Fernet(key)
        unique_id = str(len(passwords) + 1)
        passwords[unique_id] = {
            'service': service,
            'username': service_user,
            'password': fernet.encrypt(password.encode()).decode()
        }
        save_passwords(user, passwords)
        messagebox.showinfo("Exito", f"Contrasena agregada con ID: {unique_id}")
    else:
        messagebox.showerror("Error", "Todos los campos son obligatorios.")

def show_passwords(user):
    passwords = load_passwords(user)
    if not passwords:
        messagebox.showinfo("Sin Contrasenas", "No tienes contrasenas guardadas.")
        return
    
    show_window = tk.Toplevel(root)
    show_window.title("Contrasenas Guardadas")
    show_window.geometry("600x400")

    tree = ttk.Treeview(show_window, columns=("ID", "Servicio", "Usuario", "Contrasena"), show='headings')
    tree.heading("ID", text="ID")
    tree.heading("Servicio", text="Servicio")
    tree.heading("Usuario", text="Usuario")
    tree.heading("Contrasena", text="Contrasena")
    tree.pack(expand=True, fill='both')

    fernet = Fernet(key)
    for unique_id, item_data in passwords.items():
        service = item_data['service']
        username = item_data['username']
        password = fernet.decrypt(item_data['password'].encode()).decode()
        tree.insert("", tk.END, values=(unique_id, service, username, password))

    # Agregar menu contextual al Treeview
    tree.bind("<Button-3>", lambda event: show_context_menu(event, tree))

# Generar contraseña y agregarla
def generate_password(user):
    length = simpledialog.askinteger("Generar Contrasena", "Longitud de la contrasena:", minvalue=8, maxvalue=32)
    if length:
        characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choice(characters) for _ in range(length))
        service = simpledialog.askstring("Generar Contrasena", "Servicio (e.g., Gmail, Instagram):")
        passwords = load_passwords(user)
        fernet = Fernet(key)
        unique_id = str(len(passwords) + 1)
        passwords[unique_id] = {
            'service': service,
            'username': 'Generado',
            'password': fernet.encrypt(password.encode()).decode()
        }
        save_passwords(user, passwords)
        messagebox.showinfo("Contrasena Generada", f"Contrasena generada: {password}\nSe ha agregado a tu lista.")
    else:
        messagebox.showerror("Error", "Longitud no valida.")

# Menu contextual para Treeview
def show_context_menu(event, tree):
    menu = tk.Menu(root, tearoff=0)
    menu.add_command(label="Copiar", command=lambda: copy_selected_item(tree))
    menu.tk_popup(event.x_root, event.y_root)

def copy_selected_item(tree):
    try:
        selected_item = tree.focus()
        item_values = tree.item(selected_item, "values")
        if item_values:
            password = item_values[3]  # Copiar la contrasena
            root.clipboard_clear()
            root.clipboard_append(password)
            messagebox.showinfo("Copiado", "Contrasena copiada al portapapeles.")
    except IndexError:
        messagebox.showerror("Error", "No se selecciono ningun elemento.")

# Configuracion de la GUI
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

    add_button = tk.Button(panel_frame, text="Agregar Contrasena", command=lambda: add_password(user), width=25)
    add_button.pack(pady=5)

    generate_button = tk.Button(panel_frame, text="Generar Contrasena", command=lambda: generate_password(user), width=25)
    generate_button.pack(pady=5)

    show_button = tk.Button(panel_frame, text="Mostrar Contrasenas", command=lambda: show_passwords(user), width=25)
    show_button.pack(pady=5)

    exit_button = tk.Button(panel_frame, text="Cerrar Sesion", command=root.quit, width=25)
    exit_button.pack(pady=5)

login_frame = tk.Frame(root)
login_frame.pack(pady=20)

login_button = tk.Button(login_frame, text="Iniciar Sesion", command=open_login, width=25)
login_button.pack(pady=5)

register_button = tk.Button(login_frame, text="Registrar Usuario", command=register_user, width=25)
register_button.pack(pady=5)

root.mainloop()

