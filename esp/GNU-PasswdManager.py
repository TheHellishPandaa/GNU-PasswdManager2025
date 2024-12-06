import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from cryptography.fernet import Fernet
import json
import os
import random
import string

# Funciones de manejo de contraseñas
def generar_clave():
    return Fernet.generate_key()

def cargar_clave(nombre_archivo='clave.key'):
    if not os.path.exists(nombre_archivo):
        clave = generar_clave()
        with open(nombre_archivo, 'wb') as file:
            file.write(clave)
    else:
        with open(nombre_archivo, 'rb') as file:
            clave = file.read()
    return clave

def cargar_datos(nombre_archivo='usuarios.json'):
    if os.path.exists(nombre_archivo):
        with open(nombre_archivo, 'r') as file:
            return json.load(file)
    else:
        return {}

def guardar_datos(data, nombre_archivo='usuarios.json'):
    with open(nombre_archivo, 'w') as file:
        json.dump(data, file, indent=4)

def cargar_contraseñas(usuario, nombre_archivo='contraseñas.json'):
    if os.path.exists(nombre_archivo):
        with open(nombre_archivo, 'r') as file:
            datos = json.load(file)
            if usuario in datos:
                return datos[usuario]
    return {}

def guardar_contraseñas(usuario, contraseñas, nombre_archivo='contraseñas.json'):
    if os.path.exists(nombre_archivo):
        with open(nombre_archivo, 'r') as file:
            datos = json.load(file)
    else:
        datos = {}
    datos[usuario] = contraseñas
    with open(nombre_archivo, 'w') as file:
        json.dump(datos, file, indent=4)

# Funciones de autenticación
def registrar_usuario():
    usuario = simpledialog.askstring("Registrar Usuario", "Usuario:")
    if usuario in usuarios:
        messagebox.showerror("Error", "El usuario ya existe.")
        return
    contraseña = simpledialog.askstring("Registrar Usuario", "Contraseña:", show='*')
    if usuario and contraseña:
        usuarios[usuario] = {'contraseña': contraseña}
        guardar_datos(usuarios)
        messagebox.showinfo("Éxito", "Usuario registrado con éxito.")
    else:
        messagebox.showerror("Error", "Todos los campos son obligatorios.")

def login_usuario():
    usuario = simpledialog.askstring("Login", "Usuario:")
    if usuario not in usuarios:
        messagebox.showerror("Error", "Usuario no encontrado.")
        return None
    contraseña = simpledialog.askstring("Login", "Contraseña:", show='*')
    if usuarios[usuario]['contraseña'] == contraseña:
        return usuario
    else:
        messagebox.showerror("Error", "Contraseña incorrecta.")
        return None

# Funciones de manejo de contraseñas
def añadir_contraseña(usuario):
    contraseñas = cargar_contraseñas(usuario)
    servicio = simpledialog.askstring("Añadir Contraseña", "Nombre del Servicio (Ej. Gmail, Instagram):")
    usuario_servicio = simpledialog.askstring("Añadir Contraseña", "Usuario del servicio:")
    contraseña = simpledialog.askstring("Añadir Contraseña", "Contraseña:", show='*')

    if servicio and usuario_servicio and contraseña:
        fernet = Fernet(clave)
        id_unico = str(len(contraseñas) + 1)
        contraseñas[id_unico] = {
            'servicio': servicio,
            'usuario': usuario_servicio,
            'contraseña': fernet.encrypt(contraseña.encode()).decode()
        }
        guardar_contraseñas(usuario, contraseñas)
        messagebox.showinfo("Éxito", f"Contraseña añadida con ID: {id_unico}")
    else:
        messagebox.showerror("Error", "Todos los campos son obligatorios.")

def mostrar_contraseñas(usuario):
    contraseñas = cargar_contraseñas(usuario)
    if not contraseñas:
        messagebox.showinfo("Sin Contraseñas", "No tienes contraseñas guardadas.")
        return
    
    ventana_mostrar = tk.Toplevel(root)
    ventana_mostrar.title("Contraseñas Guardadas")

    tree = ttk.Treeview(ventana_mostrar, columns=("ID", "Servicio", "Usuario", "Contraseña"), show='headings')
    tree.heading("ID", text="ID")
    tree.heading("Servicio", text="Servicio")
    tree.heading("Usuario", text="Usuario")
    tree.heading("Contraseña", text="Contraseña")
    
    fernet = Fernet(clave)
    for id_unico, datos_item in contraseñas.items():
        servicio = datos_item['servicio']
        usuario_ = datos_item['usuario']
        contraseña = fernet.decrypt(datos_item['contraseña'].encode()).decode()
        tree.insert("", tk.END, values=(id_unico, servicio, usuario_, contraseña))
    
    tree.pack(expand=True, fill='both')

# Generar una contraseña aleatoria y agregarla
def generar_contraseña(usuario):
    longitud = simpledialog.askinteger("Generar Contraseña", "Longitud de la contraseña:", minvalue=8, maxvalue=32)
    if longitud:
        caracteres = string.ascii_letters + string.digits + string.punctuation
        contraseña = ''.join(random.choice(caracteres) for _ in range(longitud))
        servicio = simpledialog.askstring("Generar Contraseña", "Nombre del Servicio (Ej. Gmail, Instagram):")
        contraseñas = cargar_contraseñas(usuario)
        fernet = Fernet(clave)
        id_unico = str(len(contraseñas) + 1)
        contraseñas[id_unico] = {
            'servicio': servicio,
            'usuario': 'Generada',
            'contraseña': fernet.encrypt(contraseña.encode()).decode()
        }
        guardar_contraseñas(usuario, contraseñas)
        messagebox.showinfo("Contraseña Generada", f"Contraseña generada: {contraseña}\nSe ha añadido a tu lista de contraseñas.")
    else:
        messagebox.showerror("Error", "Longitud no válida.")

# Configurar la interfaz gráfica
clave = cargar_clave()
usuarios = cargar_datos()

root = tk.Tk()
root.title("GNU-PasswdManager")
root.geometry("400x400")

def abrir_login():
    usuario = login_usuario()
    if usuario:
        frame_login.pack_forget()
        mostrar_panel(usuario)

def mostrar_panel(usuario):
    frame_panel = tk.Frame(root)
    frame_panel.pack(pady=20)

    titulo = tk.Label(frame_panel, text="GNU-PasswdManager", font=("Arial", 16, "bold"))
    titulo.pack(pady=10)

    btn_añadir = tk.Button(frame_panel, text="Añadir Contraseña", command=lambda: añadir_contraseña(usuario), width=25)
    btn_añadir.pack(pady=5)

    btn_generar = tk.Button(frame_panel, text="Generar Contraseña", command=lambda: generar_contraseña(usuario), width=25)
    btn_generar.pack(pady=5)

    btn_mostrar = tk.Button(frame_panel, text="Mostrar Contraseñas", command=lambda: mostrar_contraseñas(usuario), width=25)
    btn_mostrar.pack(pady=5)

    btn_salir = tk.Button(frame_panel, text="Cerrar Sesión", command=root.quit, width=25)
    btn_salir.pack(pady=5)

frame_login = tk.Frame(root)
frame_login.pack(pady=20)

btn_login = tk.Button(frame_login, text="Login", command=abrir_login, width=25)
btn_login.pack(pady=5)

btn_registrar = tk.Button(frame_login, text="Registrar Usuario", command=registrar_usuario, width=25)
btn_registrar.pack(pady=5)

root.mainloop()

